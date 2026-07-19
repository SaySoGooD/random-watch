from abc import ABC, abstractmethod

from random_watch.entities.genre import Genre
from random_watch.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from random_watch.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from random_watch.entities.movie import Movie
from random_watch.entities.tv import Tv


class ITMDBAPIAdapter(ABC):
    """Interface for TMDB API adapter."""

    @abstractmethod
    async def fetch_random_movies(
        self,
        filter_dto: MovieFilterDTO,
    ) -> list[Movie]: 
        ...

    @abstractmethod
    async def fetch_random_tv(
        self,
        filter_dto: TvFilterDTO,
    ) -> list[Tv]: 
        ...

    @abstractmethod
    async def fetch_movie_genres(
        self,
        language: str | None = None,
    ) -> list[Genre]: 
        ...

    @abstractmethod
    async def fetch_tv_genres(
        self,
        language: str | None = None,
    ) -> list[Genre]: 
        ...
