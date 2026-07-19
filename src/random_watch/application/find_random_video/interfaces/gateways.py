from typing import Protocol

from random_watch.application.find_random_video.filter_dto.movie_filter_dto import \
    MovieFilterDTO
from random_watch.application.find_random_video.filter_dto.tv_filter_dto import \
    TvFilterDTO
from random_watch.entities.genre import Genre
from random_watch.entities.movie import Movie
from random_watch.entities.tv import Tv


class MovieGateway(Protocol):
    async def fetch_random_movies(self, filter_dto: MovieFilterDTO) -> list[Movie]: ...


class TvGateway(Protocol):
    async def fetch_random_tv(self, filter_dto: TvFilterDTO) -> list[Tv]: ...


class GenreGateway(Protocol):
    async def fetch_movie_genres(self, language: str | None = None) -> list[Genre]: ...

    async def fetch_tv_genres(self, language: str | None = None) -> list[Genre]: ...
