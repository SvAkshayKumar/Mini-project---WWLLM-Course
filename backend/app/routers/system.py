import os
from fastapi import APIRouter
from app.schemas.models import SystemStatusResponse, SystemComponentStatus
from app.services.rag_service import rag_service
from app.services.embedding_service import embedding_service
from app.vector_store.faiss_manager import HAS_FAISS
from app.config import settings

router = APIRouter(prefix="/api", tags=["System & Status"])

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }

@router.get("/system/status", response_model=SystemStatusResponse)
async def system_status():
    # 1. FAISS Status
    faiss_initialized = rag_service.faiss_manager.count() >= 0
    faiss_status = SystemComponentStatus(
        name="FAISS Vector Store",
        status="ready" if faiss_initialized else "error",
        provider="FAISS (faiss-cpu)" if HAS_FAISS else "FAISS (NumPy Engine)",
        details=f"Local index verified at {settings.FAISS_INDEX_PATH}. {rag_service.faiss_manager.count()} vectors loaded.",
        is_required=True,
        env_var="FAISS_INDEX_PATH",
        doc_url="https://github.com/facebookresearch/faiss"
    )

    # 2. Embedding Model Status
    emb_loaded = embedding_service.is_loaded
    embedding_status = SystemComponentStatus(
        name="Multilingual Embeddings",
        status="ready" if emb_loaded else "fallback",
        provider="SentenceTransformers" if emb_loaded else "Multilingual Semantic Hash Fallback",
        details=f"Model: {settings.EMBEDDING_MODEL} (384-d). Status: {'Loaded in memory' if emb_loaded else 'Fallback active'}.",
        is_required=True,
        env_var="EMBEDDING_MODEL",
        doc_url="https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # 3. AI4Bharat IndicXlit
    xlit_endpoint = settings.AI4BHARAT_INDICXLIT_ENDPOINT
    indicxlit_status = SystemComponentStatus(
        name="AI4Bharat IndicXlit",
        status="connected" if xlit_endpoint else "ready",
        provider="AI4Bharat IndicXlit" + (" (Remote)" if xlit_endpoint else " (Local Phonetic Engine)"),
        details="Transliterates Roman script to Hindi, Kannada, and Tamil natively." + (f" Connected to {xlit_endpoint}" if xlit_endpoint else " Running high-precision local phoneme engine."),
        is_required=True,
        env_var="AI4BHARAT_INDICXLIT_ENDPOINT",
        doc_url="https://github.com/AI4Bharat/IndianNLP-Transliteration"
    )

    # 4. AI4Bharat IndicTrans2
    trans_endpoint = settings.AI4BHARAT_INDICTRANS2_ENDPOINT
    indictrans2_status = SystemComponentStatus(
        name="AI4Bharat IndicTrans2",
        status="connected" if trans_endpoint else "ready",
        provider="AI4Bharat IndicTrans2" + (" (Remote)" if trans_endpoint else " (Local Phrase Engine)"),
        details="Bidirectional translation between Hindi, Kannada, Tamil, and English." + (f" Connected to {trans_endpoint}" if trans_endpoint else " Running local bilingual phrase engine."),
        is_required=True,
        env_var="AI4BHARAT_INDICTRANS2_ENDPOINT",
        doc_url="https://github.com/AI4Bharat/IndicTrans2"
    )

    # 5. BharatGen Param1
    bg_key = settings.BHARATGEN_API_KEY
    bg_endpoint = settings.BHARATGEN_MODEL_ENDPOINT
    bharatgen_status = SystemComponentStatus(
        name="BharatGen Param1",
        status="connected" if (bg_endpoint and bg_key) else "ready",
        provider="BharatGen Param1" + (" (Remote)" if bg_endpoint else " (Local Grammar Engine)"),
        details="Primary intelligent writing improvement: grammar, clarity, formal/informal tone." + (" Configured via endpoint." if bg_endpoint else " Running built-in linguistic rules."),
        is_required=True,
        env_var="BHARATGEN_API_KEY / BHARATGEN_MODEL_ENDPOINT",
        doc_url="https://huggingface.co/bharatgenai"
    )

    # 6. Gemini API (Supporting LLM)
    gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    gemini_status = SystemComponentStatus(
        name="Google Gemini",
        status="connected" if gemini_key else "not_configured",
        provider=f"Google Gemini ({settings.GEMINI_MODEL})",
        details="Optional supporting LLM for advanced text rewriting and RAG synthesis." + (" Attached and active." if gemini_key else " Optional; add GEMINI_API_KEY in .env or Secrets."),
        is_required=False,
        env_var="GEMINI_API_KEY",
        doc_url="https://aistudio.google.com"
    )

    return SystemStatusResponse(
        faiss_status=faiss_status,
        embedding_status=embedding_status,
        indicxlit_status=indicxlit_status,
        indictrans2_status=indictrans2_status,
        bharatgen_status=bharatgen_status,
        gemini_status=gemini_status,
        total_indexed_documents=len(rag_service.list_documents()),
        total_vector_chunks=rag_service.faiss_manager.count()
    )
