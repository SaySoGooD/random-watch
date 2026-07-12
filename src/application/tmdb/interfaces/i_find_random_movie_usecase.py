from abc import ABC, abstractmethod

from src.application.tmdb.result_dto.movie_dto import MovieDTO
from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO


class IGetRandomMovieUseCase(ABC):
    @abstractmethod
    async def __call__(
        self,
        filter_dto: MovieFilterDTO,
    ) -> list[MovieDTO]:
        ...