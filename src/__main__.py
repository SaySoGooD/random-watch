import uvicorn

from src.main.dependency_injection import container

if __name__ == "__main__":
    _config = container.config()
    uvicorn.run(
        "src.infrastructure.api:app",
        host=_config.API_HOST,
        port=_config.API_PORT,
        reload=True,
    )