import random

from random_watch.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from random_watch.application.find_random_video.interfaces.i_find_random_movie_usecase import (
    IGetRandomMovieUseCase,
)
from random_watch.application.find_random_video.interfaces.i_tmdb_api_adapter import (
    ITMDBAPIAdapter,
)
from random_watch.entities.movie import Movie, MovieNotFoundError


class GetRandomMovieUseCase(IGetRandomMovieUseCase):
    """
    Returns one random movie matching the filter.
    """

    def __init__(self, adapter: ITMDBAPIAdapter) -> None:
        self._adapter = adapter

    async def __call__(self, filter_dto: MovieFilterDTO) -> Movie:
        movies = await self._adapter.fetch_random_movies(filter_dto)

        if not movies:
            raise MovieNotFoundError()

        return random.choice(movies)
