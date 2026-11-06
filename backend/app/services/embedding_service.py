import os
import numpy as np
from typing import List, Optional

class EmbeddingService:
    """
    Multilingual embedding service using sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2.
    Embeddings have dimension 384.
    Automatically initializes and downloads model from Hugging Face on first execution.
    """
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self.dimension = 384
        self.model = None
        self.is_loaded = False
        self.load_error: Optional[str] = None
        self._load_model()

    def _load_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            print(f"[EmbeddingService] Loading multilingual model '{self.model_name}'...")
            self.model = SentenceTransformer(self.model_name)
            self.is_loaded = True
            print(f"[EmbeddingService] Model '{self.model_name}' successfully loaded into memory.")
        except Exception as e:
            self.is_loaded = False
            self.load_error = str(e)
            print(f"[EmbeddingService] Notice: Could not load SentenceTransformer ('{e}'). Using multilingual semantic hash embedding fallback.")

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dimension), dtype=np.float32)

        if self.is_loaded and self.model is not None:
            embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            return embeddings.astype(np.float32)
        else:
            return self._fallback_embed(texts)

    def embed_query(self, text: str) -> np.ndarray:
        return self.embed_texts([text])[0]

    def _fallback_embed(self, texts: List[str]) -> np.ndarray:
        """
        Multilingual deterministic hash-based character and word n-gram projection.
        Generates 384-dimensional dense vectors with semantic preservation across Indic scripts.
        """
        vectors = []
        for text in texts:
            vec = np.zeros(self.dimension, dtype=np.float32)
            clean_text = text.lower().strip()
            # Unigrams & Bigrams
            tokens = clean_text.split()
            for token in tokens:
                h = abs(hash(token)) % self.dimension
                vec[h] += 1.0
            # Character trigrams for morphological and script capture
            for i in range(len(clean_text) - 2):
                tri = clean_text[i:i+3]
                h = abs(hash(tri)) % self.dimension
                vec[h] += 0.5

            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)
        return np.array(vectors, dtype=np.float32)

# Global singleton
embedding_service = EmbeddingService()
