from fastapi import FastAPI

from src.infrastructure.api.routers import router

app = FastAPI(title="Random Watch API", version="0.1.0")
app.include_router(router)

__all__ = ["app"]