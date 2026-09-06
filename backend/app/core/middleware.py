from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import uuid
import time
import structlog

logger = structlog.get_logger()

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        logger.info(
            "request_audit",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration=duration,
            request_id=getattr(request.state, "request_id", None)
        )
        return response
