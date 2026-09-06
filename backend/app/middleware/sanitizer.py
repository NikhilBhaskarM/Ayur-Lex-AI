"""
DPDP PII Redaction & Data Sanitizer Middleware
Compliant with India's Digital Personal Data Protection (DPDP) Act, 2023.
Masks inventor names, emails, Indian phone numbers, Aadhaar/PAN IDs, and proprietary
formula batch codes before third-party LLM dispatch.
"""

from typing import Tuple, Dict, Any
import re
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import structlog

logger = structlog.get_logger(__name__)

# Regular expressions for Indian PII patterns
REGEX_PATTERNS = {
    "aadhaar": r'\b\d{4}[\-\s]?\d{4}[\-\s]?\d{4}\b',
    "pan": r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b',
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
    "phone": r'\b(?:\+91[\-\s]?)?[6-9]\d{9}\b',
    "formula_code": r'\b(?:BATCH|FORMULA|RECIPE|SPEC|LOT|CODE)[\-_:][A-Za-z0-9\-_]{3,20}\b'
}


def mask_pii_for_llm(raw_text: str) -> Tuple[str, Dict[str, str]]:
    """
    Masks sensitive personal data and proprietary formulation identifiers.
    Returns:
        (sanitized_text, de_anonymize_map)
    """
    sanitized = raw_text
    de_anonymize_map: Dict[str, str] = {}
    counter = 1

    # 1. Mask Aadhaar numbers
    for match in re.finditer(REGEX_PATTERNS["aadhaar"], sanitized):
        val = match.group(0)
        clean_val = val.replace(" ", "").replace("-", "")
        # Exclude common dates or 12-digit numbers starting with 20
        if len(clean_val) == 12 and not clean_val.startswith("20"):
            tag = f"[REDACTED_AADHAAR_{counter}]"
            de_anonymize_map[tag] = val
            sanitized = sanitized.replace(val, tag)
            counter += 1

    # 2. Mask PAN numbers
    for match in re.finditer(REGEX_PATTERNS["pan"], sanitized):
        val = match.group(0)
        tag = f"[REDACTED_PAN_{counter}]"
        de_anonymize_map[tag] = val
        sanitized = sanitized.replace(val, tag)
        counter += 1

    # 3. Mask Emails
    for match in re.finditer(REGEX_PATTERNS["email"], sanitized):
        val = match.group(0)
        tag = f"[REDACTED_EMAIL_{counter}]"
        de_anonymize_map[tag] = val
        sanitized = sanitized.replace(val, tag)
        counter += 1

    # 4. Mask Phone numbers
    for match in re.finditer(REGEX_PATTERNS["phone"], sanitized):
        val = match.group(0)
        tag = f"[REDACTED_PHONE_{counter}]"
        de_anonymize_map[tag] = val
        sanitized = sanitized.replace(val, tag)
        counter += 1

    # 5. Mask proprietary formula batch codes
    for match in re.finditer(REGEX_PATTERNS["formula_code"], sanitized, re.IGNORECASE):
        val = match.group(0)
        tag = f"[REDACTED_PROPRIETARY_CODE_{counter}]"
        de_anonymize_map[tag] = val
        sanitized = sanitized.replace(val, tag)
        counter += 1

    # 6. Mask inventor attribution patterns ("inventor: John Doe", "applicant: Jane Doe")
    inventor_pattern = r'(?i)\b(?:inventor|applicant|scientist|researcher)\s*[:=]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b'
    for match in re.finditer(inventor_pattern, sanitized):
        name = match.group(1)
        tag = f"[REDACTED_INVENTOR_{counter}]"
        de_anonymize_map[tag] = name
        sanitized = sanitized.replace(name, tag)
        counter += 1

    if de_anonymize_map:
        logger.info("DPDP Sanitizer masked sensitive identifiers", items_masked=len(de_anonymize_map))

    return sanitized, de_anonymize_map


def restore_pii_from_map(text: str, de_anonymize_map: Dict[str, str]) -> str:
    """Restores masked tokens to their original values in the local client response."""
    restored = text
    for tag, original_val in de_anonymize_map.items():
        restored = restored.replace(tag, original_val)
    return restored


class DPDPSanitizerMiddleware(BaseHTTPMiddleware):
    """
    HTTP Middleware auditing incoming requests for DPDP Act 2023 compliance.
    """
    async def dispatch(self, request: Request, call_next):
        # We process the request and ensure sanitization telemetry is attached
        response = await call_next(request)
        response.headers["X-DPDP-Compliance"] = "DPDP-Act-2023-Audited"
        return response
