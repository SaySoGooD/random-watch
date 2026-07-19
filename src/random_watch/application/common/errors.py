class ApplicationError(Exception):
    """Base error for the application layer."""


class EntityNotFoundError(ApplicationError):
    """Raised when a requested entity cannot be found."""


class MovieNotFoundError(EntityNotFoundError):
    def __init__(self, message: str = "No movie found") -> None:
        super().__init__(message)


class TvNotFoundError(EntityNotFoundError):
    def __init__(self, message: str = "No TV show found") -> None:
        super().__init__(message)


class GenreNotFoundError(EntityNotFoundError):
    def __init__(self, message: str = "No genre found") -> None:
        super().__init__(message)
