from random_watch.entities.common.errors import EntityNotFoundError


class MovieNotFoundError(EntityNotFoundError):
    def __init__(self, message: str = "No movie found") -> None:
        super().__init__(message)
