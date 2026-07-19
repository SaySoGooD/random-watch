import asyncio
import random

from random_watch.application.find_random_video.filter_dto.any_filter_dto import AnyFilterDTO
from random_watch.application.find_random_video.interfaces.i_tmdb_api_adapter import (
    ITMDBAPIAdapter,
)
from random_watch.entities.movie import Movie
from random_watch.entities.tv import Tv


class GetRandomCollectionUseCase:
    def __init__(self, adapter: ITMDBAPIAdapter) -> None:
        self._adapter = adapter

    async def __call__(
        self,
        filter_dto: AnyFilterDTO,
        count: int = 5,
    ) -> list[Movie | Tv]:
        movie_filter, tv_filter = filter_dto.split()

        movie_task = self._adapter.fetch_random_movies(movie_filter)
        tv_task = self._adapter.fetch_random_tv(tv_filter)

        movies, tvs = await asyncio.gather(
            movie_task,
            tv_task,
        )

        result: list[Movie | Tv] = [
            *movies,
            *tvs,
        ]

        random.shuffle(result)

        return result[:count]
