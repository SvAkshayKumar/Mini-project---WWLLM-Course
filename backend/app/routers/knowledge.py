from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Any
from app.schemas.models import KnowledgeQueryRequest, KnowledgeQueryResponse, DocumentInfo
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge Base & RAG"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_doc.txt"
    content_bytes = await file.read()
    
    # Extract text based on file format
    text_content = ""
    file_type = "txt"
    if filename.endswith(".pdf"):
        file_type = "pdf"
        try:
            import pypdf
            import io
            reader = pypdf.PdfReader(io.BytesIO(content_bytes))
            for page in reader.pages:
                text_content += (page.extract_text() or "") + "\n"
        except Exception as e:
            # Fallback text decode
            text_content = content_bytes.decode("utf-8", errors="ignore")
    elif filename.endswith(".docx"):
        file_type = "docx"
        try:
            import docx
            import io
            doc = docx.Document(io.BytesIO(content_bytes))
            text_content = "\n".join([p.text for p in doc.paragraphs if p.text])
        except Exception as e:
            text_content = content_bytes.decode("utf-8", errors="ignore")
    else:
        text_content = content_bytes.decode("utf-8", errors="ignore")

    if not text_content.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from the uploaded document.")

    doc_info = rag_service.ingest_text(filename, text_content, file_type=file_type)
    return {
        "success": True,
        "message": f"Successfully indexed '{filename}' into FAISS vector database.",
        "document": doc_info
    }

@router.get("/documents")
async def get_documents():
    docs = rag_service.list_documents()
    return {"success": True, "documents": docs, "total": len(docs)}

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    success = rag_service.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Document with ID '{doc_id}' not found.")
    return {"success": True, "message": f"Document '{doc_id}' removed and FAISS index rebuilt."}

@router.post("/reindex")
async def reindex_knowledge():
    rag_service.rebuild_index()
    return {
        "success": True,
        "message": "FAISS vector index successfully reconstructed from metadata.",
        "vector_count": rag_service.faiss_manager.count()
    }

@router.post("/query", response_model=KnowledgeQueryResponse)
async def query_knowledge(req: KnowledgeQueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    res = rag_service.query(req.query, top_k=req.top_k)
    return KnowledgeQueryResponse(
        success=True,
        query=req.query,
        answer=res.get("answer", ""),
        citations=res.get("citations", []),
        provider_used=res.get("provider_used", "IndicWrite RAG")
    )
