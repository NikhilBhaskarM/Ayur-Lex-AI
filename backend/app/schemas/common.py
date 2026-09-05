from pydantic import BaseModel, AnyUrl
from typing import TypeVar, Generic, Optional, List
from enum import Enum
from datetime import datetime

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

class SuccessResponse(BaseModel):
    message: str

class JurisdictionEnum(str, Enum):
    INDIA = "INDIA"
    INTERNATIONAL = "INTERNATIONAL"

class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Citation(BaseModel):
    source_title: str
    authority: str
    section: Optional[str] = None
    rule: Optional[str] = None
    article: Optional[str] = None
    version_date: Optional[datetime] = None
    official_url: Optional[AnyUrl] = None
    retrieved_at: datetime
    relevant_passage: str

class DisclaimerResponse(BaseModel):
    disclaimer: str = "This information is provided for general guidance only and does not constitute legal advice."
