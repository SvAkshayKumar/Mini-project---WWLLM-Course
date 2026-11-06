from fastapi import APIRouter, HTTPException
from app.schemas.models import ImproveRequest, ImproveResponse
from app.services.improvement_service import improvement_service

router = APIRouter(prefix="/api", tags=["Text Improvement"])

@router.post("/improve", response_model=ImproveResponse)
async def improve_text(req: ImproveRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    res = improvement_service.improve_text(
        text=req.text,
        mode=req.mode,
        language=req.language or "hi",
        provider_preference=req.provider_preference or "bharatgen"
    )
    return ImproveResponse(
        success=True,
        original_text=req.text,
        improved_text=res.get("improved_text", req.text),
        mode=req.mode,
        provider_used=res.get("provider_used", "BharatGen Param1"),
        explanation=res.get("explanation", ""),
        changes=res.get("changes", [])
    )
