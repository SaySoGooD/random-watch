from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from random_watch.dependency_injection import Container
from random_watch.infrastructure.api.exc_handlers import map_exc_handlers
from random_watch.infrastructure.api.ratelimit_middleware import \
    GlobalRateLimitMiddleware
from random_watch.infrastructure.api.routers import router
from random_watch.infrastructure.config import Config


def setup_configs() -> Config:
    return Config()


def setup_container() -> Container:
    container = Container()
    container.wire(modules=["random_watch.infrastructure.api.routers"])
    return container


def setup_routes(app: FastAPI, /) -> None:
    app.include_router(router)


def setup_middlewares(app: FastAPI, /, config: Config) -> None:
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[
            f"{config.API_RATE_LIMIT_PER_CLIENT}/{config.API_RATE_LIMIT_WINDOW}seconds"
        ],
    )
    app.state.limiter = limiter

    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(
        GlobalRateLimitMiddleware,
        max_requests=config.API_RATE_LIMIT_GLOBAL,
        window_seconds=config.API_RATE_LIMIT_WINDOW,
    )


def setup_exc_handlers(app: FastAPI, /) -> None:
    map_exc_handlers(app)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Release long-lived resources on shutdown."""
    yield
    await app.state.container.tmdb_client().close()


def bootstrap() -> FastAPI:
    """Assemble the application: config, DI container, FastAPI app."""
    config = setup_configs()
    container = setup_container()

    app = FastAPI(title=config.API_TITLE, version=config.API_VERSION, lifespan=lifespan)
    app.state.container = container

    setup_middlewares(app, config)
    setup_exc_handlers(app)
    setup_routes(app)

    return app


def run() -> None:
    """Start the API server."""
    config = setup_configs()
    uvicorn.run(
        "random_watch.bootstrap:bootstrap",
        factory=True,
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
    )
