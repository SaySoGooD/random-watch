import random
from dataclasses import replace

from src.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.find_random_video.interfaces.i_find_random_movie_usecase import (
    IGetRandomMovieUseCase,
)
from src.application.find_random_video.interfaces.i_tmdb_api_adapter import (
    ITMDBAPIAdapter,
)
from src.application.find_random_video.result_dto.movie_dto import MovieDTO


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

        if not first_page:
            return None

        return random.choice(first_page)
