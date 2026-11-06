from fastapi import APIRouter, HTTPException
from app.schemas.models import TransliterateRequest, TransliterateResponse, ProcessPipelineRequest, ProcessPipelineResponse
from app.services.transliteration_service import transliteration_service
from app.services.improvement_service import improvement_service
from app.services.translation_service import translation_service

router = APIRouter(prefix="/api", tags=["Transliteration"])

@router.post("/transliterate", response_model=TransliterateResponse)
async def transliterate(req: TransliterateRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    out, provider = transliteration_service.transliterate(req.text, req.target_language)
    return TransliterateResponse(
        success=True,
        source_text=req.text,
        target_language=req.target_language,
        transliterated_text=out,
        provider=provider,
        details={"char_count": len(out), "word_count": len(out.split())}
    )

@router.post("/process", response_model=ProcessPipelineResponse)
async def process_pipeline(req: ProcessPipelineRequest):
    """
    Combined multi-stage pipeline: Transliterate -> Improve -> Translate
    """
    steps = []
    
    # Stage 1: Transliterate
    transliterated, t_provider = transliteration_service.transliterate(req.text, req.transliterate_lang)
    steps.append({"stage": "transliteration", "provider": t_provider, "output": transliterated})
    
    current_text = transliterated
    improved = None
    if req.improve_mode:
        imp_res = improvement_service.improve_text(current_text, mode=req.improve_mode, language=req.transliterate_lang)
        improved = imp_res.get("improved_text")
        steps.append({"stage": "improvement", "provider": imp_res.get("provider_used"), "output": improved})
        current_text = improved

    translated = None
    if req.translate_to and req.translate_to != req.transliterate_lang:
        trans_out, tr_provider = translation_service.translate(current_text, req.transliterate_lang, req.translate_to)
        translated = trans_out
        steps.append({"stage": "translation", "provider": tr_provider, "output": translated})

    return ProcessPipelineResponse(
        success=True,
        original_input=req.text,
        transliterated=transliterated,
        improved=improved,
        translated=translated,
        steps=steps
    )
