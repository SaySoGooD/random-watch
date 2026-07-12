import asyncio
import random

from src.application.tmdb.interfaces.i_tmdb_api_adapter import ITMDBAPIAdapter
from src.application.tmdb.result_dto.movie_dto import MovieDTO
from src.application.tmdb.result_dto.tv_dto import TvDTO
from src.application.tmdb.filter_dto.any_filter_dto import AnyFilterDTO
from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.filter_dto.tv_filter_dto import TvFilterDTO


class GetRandomCollectionUseCase:
    def __init__(self, adapter: ITMDBAPIAdapter) -> None:
        self._adapter = adapter

    async def __call__(
        self,
        filter_dto: AnyFilterDTO,
        count: int = 5,
    ) -> list[MovieDTO | TvDTO]:

        movie_filter, tv_filter = filter_dto.split()

        movie_task = self._adapter.fetch_random_movies(movie_filter)
        tv_task = self._adapter.fetch_random_tv(tv_filter)

        movies, tvs = await asyncio.gather(
            movie_task,
            tv_task,
        )

        result: list[MovieDTO | TvDTO] = [
            *movies.results,
            *tvs.results,
        ]

        random.shuffle(result)

        return result[:count]