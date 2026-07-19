from abc import ABC, abstractmethod

from random_watch.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from random_watch.entities.movie import Movie


class IGetRandomMovieUseCase(ABC):
    @abstractmethod
    async def __call__(
        self,
        filter_dto: MovieFilterDTO,
    ) -> Movie:
        ...
