from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from random_watch.application.common.errors import EntityNotFoundError
from random_watch.application.find_random_video.exceptions import (
    APIConnectionError, APINotFoundError, APIRateLimitError, APIServerError,
    APIUnauthorizedError)


async def _rate_limit_handler(request: Request, exc: APIRateLimitError) -> JSONResponse:
    return JSONResponse(status_code=429, content={"detail": str(exc)})


async def _connection_handler(
    request: Request, exc: APIConnectionError
) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": str(exc)})


async def _unauthorized_handler(
    request: Request, exc: APIUnauthorizedError
) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


async def _server_error_handler(request: Request, exc: APIServerError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


async def _not_found_handler(request: Request, exc: APINotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def _entity_not_found_handler(
    request: Request, exc: EntityNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


def map_exc_handlers(app: FastAPI, /) -> None:
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_exception_handler(APIRateLimitError, _rate_limit_handler)
    app.add_exception_handler(APIConnectionError, _connection_handler)
    app.add_exception_handler(APIUnauthorizedError, _unauthorized_handler)
    app.add_exception_handler(APIServerError, _server_error_handler)
    app.add_exception_handler(APINotFoundError, _not_found_handler)
    app.add_exception_handler(EntityNotFoundError, _entity_not_found_handler)
