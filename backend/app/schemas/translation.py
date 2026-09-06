from pydantic import BaseModel, ConfigDict
from typing import Optional

class TranslationRequest(BaseModel):
    text: str
    source_language: Optional[str] = "auto"
    target_language: str = "hi"

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    provider: str

    model_config = ConfigDict(from_attributes=True)
