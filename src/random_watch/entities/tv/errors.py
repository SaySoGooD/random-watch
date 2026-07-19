from random_watch.entities.common.errors import EntityNotFoundError


class TvNotFoundError(EntityNotFoundError):
    def __init__(self, message: str = "No TV show found") -> None:
        super().__init__(message)
