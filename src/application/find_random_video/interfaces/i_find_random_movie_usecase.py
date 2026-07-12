from abc import ABC, abstractmethod

from src.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.find_random_video.result_dto.movie_dto import MovieDTO


class IGetRandomMovieUseCase(ABC):
    @abstractmethod
    async def __call__(
        self,
        filter_dto: MovieFilterDTO,
    ) -> list[MovieDTO]: ...
