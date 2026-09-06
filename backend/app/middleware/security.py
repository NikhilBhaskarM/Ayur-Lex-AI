"""
Ayurvedic IPR & Regulatory AI Assistant — Security Hardening Middleware
DevSecOps Module:
1. SecurityHeadersMiddleware: Injects OWASP recommended security headers.
2. PayloadLimitMiddleware: Prevents memory exhaustion attacks (HTTP 413 on >5MB).
3. PromptInjectionSanitizerMiddleware: Neutralizes adversarial jailbreaks and prompt injections.
4. RateLimitMiddleware: Sliding-window in-memory rate limiter protecting endpoints against denial-of-wallet.
"""

import time
import re
import json
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
import structlog

logger = structlog.get_logger(__name__)

# -----------------------------------------------------------------------------
# 1. Security Headers Middleware
# -----------------------------------------------------------------------------
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Applies standard OWASP-recommended HTTP response security headers.
    Protects against MIME sniffing, clickjacking, referrer leakage, and XSS.
    """
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Standard defense-in-depth headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        return response


# -----------------------------------------------------------------------------
# 2. Payload Size Limiter Middleware (Default: 5MB)
# -----------------------------------------------------------------------------
DEFAULT_MAX_PAYLOAD_SIZE = 5 * 1024 * 1024  # 5 Megabytes

class PayloadLimitMiddleware(BaseHTTPMiddleware):
    """
    Rejects request bodies exceeding the maximum permitted size with HTTP 413.
    Protects against memory exhaustion and large buffer overflow denial-of-service attacks.
    """
    def __init__(self, app, max_size_bytes: int = DEFAULT_MAX_PAYLOAD_SIZE):
        super().__init__(app)
        self.max_size_bytes = max_size_bytes

    async def dispatch(self, request: Request, call_next):
        # Only check requests that carry a body (POST, PUT, PATCH)
        if request.method in ("POST", "PUT", "PATCH"):
            # Check declared Content-Length header if present
            content_length = request.headers.get("content-length")
            if content_length and content_length.isdigit():
                if int(content_length) > self.max_size_bytes:
                    logger.warning(
                        "payload_size_exceeded_header",
                        size=int(content_length),
                        max_allowed=self.max_size_bytes,
                        client=request.client.host if request.client else "unknown",
                        path=request.url.path,
                    )
                    return JSONResponse(
                        status_code=413,
                        content={
                            "detail": f"Payload Too Large. Maximum allowed size is {self.max_size_bytes // (1024 * 1024)}MB.",
                            "status": "rejected",
                            "code": "PAYLOAD_TOO_LARGE",
                        },
                    )

            # Safeguard chunked / streaming requests by reading cached body
            try:
                body = await request.body()
                if len(body) > self.max_size_bytes:
                    logger.warning(
                        "payload_size_exceeded_stream",
                        size=len(body),
                        max_allowed=self.max_size_bytes,
                        client=request.client.host if request.client else "unknown",
                        path=request.url.path,
                    )
                    return JSONResponse(
                        status_code=413,
                        content={
                            "detail": f"Payload Too Large. Maximum allowed size is {self.max_size_bytes // (1024 * 1024)}MB.",
                            "status": "rejected",
                            "code": "PAYLOAD_TOO_LARGE",
                        },
                    )
            except Exception as e:
                logger.error("payload_read_error", error=str(e), path=request.url.path)

        return await call_next(request)


# -----------------------------------------------------------------------------
# 3. Prompt Injection & Adversarial Jailbreak Sanitizer
# -----------------------------------------------------------------------------
JAILBREAK_PATTERNS = [
    # Instruction overriders
    re.compile(r"(?i)\bignore\s+(all\s+)?(previous|prior|above)\s+instructions\b"),
    re.compile(r"(?i)\bdisregard\s+(all\s+)?(previous|prior|above|existing)\s+(instructions|rules|guidelines|prompts)\b"),
    re.compile(r"(?i)\bsystem\s*(prompt)?\s*override\b"),
    re.compile(r"(?i)\byou\s+are\s+now\s+(a\s+)?(dan|jailbreak|unfiltered|anarchist|godmode)\b"),
    re.compile(r"(?i)\b(?:do\s+anything\s+now|DAN\s+mode)\b"),
    re.compile(r"(?i)\bdeveloper\s+mode\s+(enabled|activated|engaged)\b"),
    # LLM special tokens / delimiter injections
    re.compile(r"<\s*\|\s*im_start\s*\|>"),
    re.compile(r"<\s*\|\s*im_end\s*\|>"),
    re.compile(r"\[INST\]\s*<<SYS>>"),
    re.compile(r"<<SYS>>\s*\[/INST\]"),
    re.compile(r"(?i)\boutput\s+your\s+(initial|original|system)\s+instructions\b"),
    re.compile(r"(?i)\brepeat\s+the\s+(system\s+prompt|text\s+above)\b"),
]

# Sensitive keys commonly holding freeform text in API requests
PROMPT_KEYS = {
    "prompt", "query", "message", "content", "claim_text",
    "formulation_text", "notes", "description", "raw_text"
}

def sanitize_prompt_text(text: str) -> Tuple[str, bool]:
    """
    Scans a string for prompt injection / jailbreak markers.
    Neutralizes detected jailbreak markers while preserving legitimate statutory text.
    Returns (sanitized_text, was_modified).
    """
    if not isinstance(text, str) or not text:
        return text, False

    modified = False
    sanitized = text

    for pattern in JAILBREAK_PATTERNS:
        if pattern.search(sanitized):
            sanitized = pattern.sub("[NEUTRALIZED_SECURITY_MARKER]", sanitized)
            modified = True

    return sanitized, modified

def _sanitize_dict_recursive(data: Any) -> Tuple[Any, bool]:
    """Recursively walks nested JSON data structures and sanitizes prompt fields."""
    any_modified = False
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k.lower() in PROMPT_KEYS and isinstance(v, str):
                cleaned, mod = sanitize_prompt_text(v)
                new_dict[k] = cleaned
                if mod:
                    any_modified = True
            elif isinstance(v, (dict, list)):
                cleaned_v, mod = _sanitize_dict_recursive(v)
                new_dict[k] = cleaned_v
                if mod:
                    any_modified = True
            else:
                new_dict[k] = v
        return new_dict, any_modified
    elif isinstance(data, list):
        new_list = []
        for item in data:
            cleaned_item, mod = _sanitize_dict_recursive(item)
            new_list.append(cleaned_item)
            if mod:
                any_modified = True
        return new_list, any_modified
    return data, False


class PromptInjectionSanitizerMiddleware(BaseHTTPMiddleware):
    """
    Intercepts JSON bodies submitted to AI and debate endpoints.
    Neutralizes adversarial jailbreak sequences without breaking legitimate
    Ayurvedic and patent research queries.
    """
    async def dispatch(self, request: Request, call_next):
        # Only inspect mutating HTTP requests targeting API endpoints
        if request.method in ("POST", "PUT", "PATCH") and request.url.path.startswith("/api/"):
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    body_bytes = await request.body()
                    if body_bytes:
                        raw_json = json.loads(body_bytes.decode("utf-8"))
                        cleaned_json, was_modified = _sanitize_dict_recursive(raw_json)

                        if was_modified:
                            logger.warning(
                                "prompt_injection_neutralized",
                                path=request.url.path,
                                client=request.client.host if request.client else "unknown",
                            )
                            # Re-encode body with sanitized contents
                            new_body_bytes = json.dumps(cleaned_json).encode("utf-8")

                            # Starlette cached body replacement
                            request._body = new_body_bytes

                            async def receive():
                                return {"type": "http.request", "body": new_body_bytes, "more_body": False}

                            request._receive = receive
                except Exception as e:
                    # Non-fatal: if JSON parsing fails, allow standard downstream validation to handle it
                    logger.debug("sanitizer_parse_skip", error=str(e), path=request.url.path)

        return await call_next(request)


# -----------------------------------------------------------------------------
# 4. Lightweight In-Memory Sliding-Window Rate Limiter
# -----------------------------------------------------------------------------
class InMemoryRateLimiter:
    """
    Sliding-window IP rate limiter.
    Stores timestamps in-memory, requiring no external Redis dependency for basic DoS protection.
    Generous defaults protect LLM wallet while allowing seamless user testing.
    """
    def __init__(self, requests_per_minute: int = 120):
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60.0
        self.requests_map: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> Tuple[bool, int, int]:
        """
        Determines whether client_ip is within the allowed request rate.
        Returns:
            (is_allowed: bool, remaining_requests: int, retry_after_seconds: int)
        """
        now = time.time()
        window_start = now - self.window_seconds

        # Prune outdated timestamps for this IP
        timestamps = [t for t in self.requests_map[client_ip] if t > window_start]
        self.requests_map[client_ip] = timestamps

        if len(timestamps) >= self.requests_per_minute:
            oldest = timestamps[0]
            retry_after = max(1, int(self.window_seconds - (now - oldest)))
            return False, 0, retry_after

        # Record current request
        self.requests_map[client_ip].append(now)
        remaining = self.requests_per_minute - len(self.requests_map[client_ip])
        return True, remaining, 0

    def cleanup(self):
        """Cleans up inactive IPs to prevent memory bloat."""
        now = time.time()
        window_start = now - self.window_seconds
        stale_ips = [ip for ip, ts in self.requests_map.items() if not ts or ts[-1] < window_start]
        for ip in stale_ips:
            del self.requests_map[ip]


# Singleton instance
global_rate_limiter = InMemoryRateLimiter(requests_per_minute=120)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware protecting inference and API routes.
    Bypasses static assets, documentation, health probes, and WebSocket endpoints.
    """
    def __init__(self, app, limiter: Optional[InMemoryRateLimiter] = None):
        super().__init__(app)
        self.limiter = limiter or global_rate_limiter

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Whitelist non-expensive / static routes
        if not path.startswith("/api/"):
            return await call_next(request)

        # Whitelist health checks, docs, and OpenAPI schemas
        if path in ("/api/v1/health", "/docs", "/redoc", "/openapi.json"):
            return await call_next(request)

        # Whitelist WebSocket upgrade endpoints (handled separately by ws protocol)
        if "upgrade" in request.headers.get("connection", "").lower() or request.headers.get("upgrade", "").lower() == "websocket":
            return await call_next(request)

        # Extract client IP
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "127.0.0.1"

        allowed, remaining, retry_after = self.limiter.is_allowed(client_ip)

        if not allowed:
            logger.warning(
                "rate_limit_exceeded",
                client_ip=client_ip,
                path=path,
                retry_after=retry_after,
            )
            return JSONResponse(
                status_code=429,
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.limiter.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                },
                content={
                    "detail": "Too many requests. Please slow down to preserve AI compute capacity.",
                    "status": "rate_limited",
                    "code": "TOO_MANY_REQUESTS",
                    "retry_after_seconds": retry_after,
                },
            )

        response: Response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
