from fastapi import APIRouter
from app.schemas.translation import TranslationRequest, TranslationResponse
from app.services.bhashini_service import BhashiniService

router = APIRouter(tags=["translation"])
bhashini_service = BhashiniService()

@router.post("", response_model=TranslationResponse)
@router.post("/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Translate text between Indian languages and English via Bhashini NMT or Ayurvedic legal domain fallback."""
    source_lang = request.source_language
    if not source_lang or source_lang == "auto":
        source_lang = bhashini_service.detect_language(request.text)

    translated, provider = await bhashini_service.translate_text(
        text=request.text,
        source_lang=source_lang,
        target_lang=request.target_language
    )

    return TranslationResponse(
        translated_text=translated,
        source_language=source_lang,
        target_language=request.target_language,
        provider=provider
    )
