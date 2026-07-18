from typing import Any

from fastapi import HTTPException

from src.main.dependency_injection import container


def get_container() -> Any:
    """Return the application-level DI container.

    Raises:
        HTTPException: 500 if the container cannot be resolved.
    """
    if container is None:
        raise HTTPException(
            status_code=500,
            detail="Dependency injection container could not be initialized.",
        )
    return container