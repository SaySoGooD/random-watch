import asyncio
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class GlobalRateLimitMiddleware(BaseHTTPMiddleware):
    """Limit the total number of requests across all clients."""

    def __init__(self, app, max_requests: int, window_seconds: int) -> None:
        super().__init__(app)
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._requests: list[float] = []
        self._lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next):
        async with self._lock:
            now = time.monotonic()
            self._requests = [t for t in self._requests if now - t < self._window_seconds]
            if len(self._requests) >= self._max_requests:
                return JSONResponse(status_code=429, content={"detail": "Global rate limit exceeded."})
            self._requests.append(now)
        return await call_next(request)