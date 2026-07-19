import random

from random_watch.application.common.errors import MovieNotFoundError
from random_watch.application.find_random_video.filter_dto.movie_filter_dto import \
    MovieFilterDTO
from random_watch.application.find_random_video.interfaces.gateways import \
    MovieGateway
from random_watch.application.find_random_video.interfaces.i_find_random_movie_usecase import \
    IGetRandomMovieUseCase
from random_watch.entities.movie import Movie


class GetRandomMovieUseCase(IGetRandomMovieUseCase):
    """
    Returns one random movie matching the filter.
    """

    def __init__(self, gateway: MovieGateway) -> None:
        self._gateway = gateway

    async def __call__(self, filter_dto: MovieFilterDTO) -> Movie:
        movies = await self._gateway.fetch_random_movies(filter_dto)

        if not movies:
            raise MovieNotFoundError()

        return random.choice(movies)
