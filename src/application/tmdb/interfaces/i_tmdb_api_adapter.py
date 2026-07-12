from abc import ABC, abstractmethod

from src.application.tmdb.filter_dto.filter_settings_dto import GenreDTO
from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.tmdb.result_dto.movie_dto import MovieDTO
from src.application.tmdb.result_dto.tv_dto import TvDTO


class ITMDBAPIAdapter(ABC):
    """Interface for TMDB API adapter."""

    @abstractmethod
    async def fetch_random_movies(
        self,
        filter_dto: MovieFilterDTO,
    ) -> list[MovieDTO]:
        ...

    @abstractmethod
    async def fetch_random_tv(
        self,
        filter_dto: TvFilterDTO,
    ) -> list[TvDTO]:
        ...

    @abstractmethod
    async def fetch_movie_genres(
        self,
        language: str | None = None,
    ) -> list[GenreDTO]:
        ...

    @abstractmethod
    async def fetch_tv_genres(
        self,
        language: str | None = None,
    ) -> list[GenreDTO]:
        ...