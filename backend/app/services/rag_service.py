import os
import uuid
import datetime
from typing import List, Dict, Any, Optional

from app.vector_store.faiss_manager import FAISSManager
from app.vector_store.metadata_manager import MetadataManager
from app.services.embedding_service import embedding_service
from app.config import settings

class RAGService:
    """
    RAG-powered multilingual knowledge base using local FAISS and SentenceTransformers.
    Supports ingestion of TXT, PDF, and DOCX files.
    """
    def __init__(self):
        self.faiss_manager = FAISSManager(index_path=settings.FAISS_INDEX_PATH, dimension=384)
        self.metadata_manager = MetadataManager(metadata_path=settings.FAISS_METADATA_PATH)
        self._seed_default_knowledge_if_empty()

    def _seed_default_knowledge_if_empty(self):
        """
        Seeds default writing guides and grammar references if index is empty.
        """
        if len(self.metadata_manager.list_documents()) == 0:
            default_docs = [
                {
                    "title": "Hindi_Grammar_and_Honorific_Guide.txt",
                    "content": (
                        "Hindi Honorifics Guide:\n"
                        "1. Use 'आप' (Aap) for formal address with plural verb endings such as 'हैं' (hain) or 'करते हैं' (karte hain).\n"
                        "2. Use 'तुम' (Tum) only for informal peer-level conversations with 'हो' (ho).\n"
                        "3. Past tense transitive verbs require the ergative postposition 'ने' (ne), such as 'उसने कहा' (usne kaha) instead of 'वह बोला'.\n"
                        "4. Transliteration convention: 'Namaste, aap kaise hain?' translates to 'नमस्ते, आप कैसे हैं?'."
                    )
                },
                {
                    "title": "Kannada_Writing_and_Vocabulary.txt",
                    "content": (
                        "Kannada Language Reference:\n"
                        "1. Formal address uses 'ನೀವು' (Neevu) meaning you (respectful/plural), while 'ನೀನು' (Neenu) is informal singular.\n"
                        "2. Common greetings: 'ನಮಸ್ಕಾರ' (Namaskara) and 'ಹೇಗಿದ್ದೀರಿ?' (Hegiddiri? - How are you?).\n"
                        "3. Affirmation: 'ಚೆನ್ನಾಗಿದ್ದೇನೆ' (Chennagiddene) means 'I am doing well'.\n"
                        "4. The Kannada script has 49 characters categorized into Swaras (vowels) and Vyanjanas (consonants)."
                    )
                },
                {
                    "title": "Tamil_Grammar_and_Style_Rules.txt",
                    "content": (
                        "Tamil Writing Style Guide:\n"
                        "1. Formal greeting: 'வணக்கம்' (Vanakkam), meaning welcome/respectful greetings.\n"
                        "2. Politeness levels: 'நீங்கள்' (Neengal) is formal, whereas 'நீ' (Nee) is informal.\n"
                        "3. Expressions: 'எப்படி இருக்கிறீர்கள்?' (Eppadi irukkireergal?) means 'How are you?' in standard polite Tamil.\n"
                        "4. Gratitude: 'நன்றி' (Nandri) means Thank You, and 'மிக்க நன்றி' (Mikka Nandri) means Thank you very much."
                    )
                }
            ]

            for doc in default_docs:
                self.ingest_text(
                    filename=doc["title"],
                    text_content=doc["content"],
                    file_type="txt"
                )

    def chunk_text(self, text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
        """
        Splits text into sliding window chunks respecting paragraph and sentence boundaries.
        """
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        chunks = []

        current_chunk = ""
        for p in paragraphs:
            if len(current_chunk) + len(p) < chunk_size:
                current_chunk += (" " if current_chunk else "") + p
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = p

        if current_chunk:
            chunks.append(current_chunk)

        # Fallback if no paragraphs or very long
        if not chunks:
            start = 0
            while start < len(text):
                end = min(start + chunk_size, len(text))
                chunks.append(text[start:end])
                start += (chunk_size - overlap)

        return chunks

    def ingest_text(self, filename: str, text_content: str, file_type: str = "txt") -> Dict[str, Any]:
        """
        Ingests document text into FAISS index and local metadata store.
        """
        doc_id = str(uuid.uuid4())[:8]
        chunks = self.chunk_text(text_content)
        if not chunks:
            raise ValueError("Document contains no readable text content.")

        embeddings = embedding_service.embed_texts(chunks)
        vector_ids = self.faiss_manager.add_vectors(embeddings)

        # Register metadata
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doc_info = {
            "id": doc_id,
            "name": filename,
            "file_type": file_type,
            "total_chunks": len(chunks),
            "uploaded_at": now_str,
            "size_bytes": len(text_content.encode("utf-8"))
        }
        self.metadata_manager.add_document(doc_id, doc_info)

        for vid, chunk_str in zip(vector_ids, chunks):
            chunk_id = f"{doc_id}_{vid}"
            chunk_meta = {
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "doc_name": filename,
                "chunk_index": vid,
                "text": chunk_str,
                "char_count": len(chunk_str)
            }
            self.metadata_manager.register_chunk(vid, chunk_id, chunk_meta)

        return doc_info

    def list_documents(self) -> List[Dict[str, Any]]:
        return self.metadata_manager.list_documents()

    def delete_document(self, doc_id: str) -> bool:
        doc = self.metadata_manager.get_document(doc_id)
        if not doc:
            return False
        # Remove from metadata and rebuild FAISS index
        self.metadata_manager.remove_document(doc_id)
        self.rebuild_index()
        return True

    def rebuild_index(self):
        """
        Re-indexes all remaining document chunks in the metadata store into a fresh FAISS index.
        """
        all_chunks = list(self.metadata_manager.data["chunks"].values())
        self.faiss_manager.reset()
        self.metadata_manager.data["id_to_chunk"] = {}

        if not all_chunks:
            self.metadata_manager.save()
            return

        texts = [c["text"] for c in all_chunks]
        embeddings = embedding_service.embed_texts(texts)
        vector_ids = self.faiss_manager.add_vectors(embeddings)

        for vid, chunk in zip(vector_ids, all_chunks):
            self.metadata_manager.data["id_to_chunk"][str(vid)] = chunk["chunk_id"]

        self.metadata_manager.save()
        print(f"[RAGService] Rebuilt FAISS index with {len(vector_ids)} vectors.")

    def query(self, query_str: str, top_k: int = 3, threshold: float = 0.25) -> Dict[str, Any]:
        """
        Executes semantic search over FAISS index and synthesizes context-aware answer.
        """
        clean_query = query_str.strip()
        if not clean_query:
            return {
                "answer": "Please ask a question about your multilingual writing knowledge base.",
                "citations": [],
                "provider_used": "IndicWrite RAG"
            }

        q_vec = embedding_service.embed_query(clean_query)
        matches = self.faiss_manager.search(q_vec, top_k=top_k)

        citations = []
        retrieved_contexts = []

        for vid, score in matches:
            if score >= threshold:
                chunk = self.metadata_manager.get_chunk_by_vector_id(vid)
                if chunk:
                    retrieved_contexts.append(chunk["text"])
                    citations.append({
                        "doc_name": chunk.get("doc_name", "Unknown"),
                        "chunk_index": chunk.get("chunk_index", vid),
                        "similarity_score": round(float(score), 4),
                        "snippet": chunk.get("text", "")[:180] + ("..." if len(chunk.get("text", "")) > 180 else "")
                    })

        if not citations:
            return {
                "answer": "No directly relevant context was found in the indexed knowledge base documents. Try uploading language grammar references, vocabulary sheets, or specific style guides.",
                "citations": [],
                "provider_used": "IndicWrite RAG (FAISS)"
            }

        # Check Gemini API for grounded generation
        gemini_key = os.getenv("GEMINI_API_KEY", None)
        if gemini_key:
            try:
                from google import genai
                client = genai.Client(
                    api_key=gemini_key,
                    http_options={"headers": {"User-Agent": "aistudio-build"}}
                )
                context_block = "\n\n---\n\n".join(retrieved_contexts)
                prompt = (
                    f"You are the IndicWrite AI writing knowledge assistant.\n"
                    f"Answer the user query based strictly on the retrieved context below.\n"
                    f"Do not hallucinate facts outside the provided context.\n\n"
                    f"Context:\n{context_block}\n\n"
                    f"User Query: {clean_query}\n\n"
                    f"Answer clearly and cite the language guidance."
                )
                resp = client.models.generateContent(
                    model=settings.GEMINI_MODEL,
                    contents=prompt
                )
                return {
                    "answer": resp.text.strip(),
                    "citations": citations,
                    "provider_used": f"Google Gemini + FAISS ({len(citations)} citations)"
                }
            except Exception as e:
                print(f"[RAGService] Gemini generation error: {e}. Falling back to local synthesizer.")

        # Local synthesis fallback
        summary = "Based on your indexed writing guides:\n\n" + "\n\n".join(retrieved_contexts[:2])
        return {
            "answer": summary,
            "citations": citations,
            "provider_used": f"IndicWrite Local RAG Engine ({len(citations)} FAISS vectors matched)"
        }

rag_service = RAGService()
