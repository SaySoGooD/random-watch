import random
from dataclasses import replace

from src.application.tmdb.interfaces.i_find_random_movie_usecase import IGetRandomMovieUseCase
from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.api_dto.tmdb_response_dto import MovieDTO
from src.application.tmdb.interfaces.i_tmdb_api_adapter import ITMDBAPIAdapter


class GetRandomMovieUseCase(IGetRandomMovieUseCase):
    """
    Returns one random movie matching the filter.
    """

    def __init__(self, adapter: ITMDBAPIAdapter) -> None:
        self._adapter = adapter

    async def __call__(self, filter_dto: MovieFilterDTO) -> MovieDTO | None:
        first_page = await self._adapter.fetch_random_movies(
            replace(filter_dto, page=1),
        )

        if not first_page.results:
            return None

        return random.choice(first_page.results)