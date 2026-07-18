from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.application.find_random_video.exceptions import (
    APIConnectionError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
    APIUnauthorizedError,
)
from src.infrastructure.api.routers import router

app = FastAPI(title="Random Watch API", version="0.1.0")
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