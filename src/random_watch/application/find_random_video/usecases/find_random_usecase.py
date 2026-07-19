import asyncio
import random

from random_watch.application.find_random_video.filter_dto.any_filter_dto import \
    AnyFilterDTO
from random_watch.application.find_random_video.interfaces.gateways import (
    MovieGateway, TvGateway)
from random_watch.entities.movie import Movie
from random_watch.entities.tv import Tv


class GetRandomCollectionUseCase:
    def __init__(self, movie_gateway: MovieGateway, tv_gateway: TvGateway) -> None:
        self._movie_gateway = movie_gateway
        self._tv_gateway = tv_gateway

    async def __call__(
        self,
        filter_dto: AnyFilterDTO,
        count: int = 5,
    ) -> list[Movie | Tv]:
        movie_filter, tv_filter = filter_dto.split()

        movie_task = self._movie_gateway.fetch_random_movies(movie_filter)
        tv_task = self._tv_gateway.fetch_random_tv(tv_filter)

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
