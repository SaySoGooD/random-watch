from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.application.find_random_video.exceptions import (
    APIConnectionError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
    APIUnauthorizedError,
)
from src.infrastructure.api.routers import router
from src.infrastructure.api.ratelimit_middleware import GlobalRateLimitMiddleware

limiter = Limiter(key_func=get_remote_address, default_limits=["35/10seconds"])

app = FastAPI(title="Random Watch API", version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(GlobalRateLimitMiddleware, max_requests=35, window_seconds=10)
app.include_router(router)


@app.exception_handler(APIRateLimitError)
async def rate_limit_handler(request: Request, exc: APIRateLimitError) -> JSONResponse:
    return JSONResponse(status_code=429, content={"detail": str(exc)})


@app.exception_handler(APIConnectionError)
async def connection_handler(request: Request, exc: APIConnectionError) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": str(exc)})


@app.exception_handler(APIUnauthorizedError)
async def unauthorized_handler(request: Request, exc: APIUnauthorizedError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(APIServerError)
async def server_error_handler(request: Request, exc: APIServerError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(APINotFoundError)
async def not_found_handler(request: Request, exc: APINotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

__all__ = ["app"]