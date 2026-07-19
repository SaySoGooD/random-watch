from random_watch.entities.common.errors import EntityNotFoundError


class GenreNotFoundError(EntityNotFoundError):
    def __init__(self, message: str = "No genre found") -> None:
        super().__init__(message)
