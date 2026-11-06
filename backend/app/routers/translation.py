from fastapi import APIRouter, HTTPException
from app.schemas.models import TranslateRequest, TranslateResponse
from app.services.translation_service import translation_service

router = APIRouter(prefix="/api", tags=["Translation"])

@router.post("/translate", response_model=TranslateResponse)
async def translate(req: TranslateRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    out, provider = translation_service.translate(req.text, req.source_language, req.target_language)
    return TranslateResponse(
        success=True,
        source_text=req.text,
        source_language=req.source_language,
        target_language=req.target_language,
        translated_text=out,
        provider=provider
    )
