from dataclasses import replace
from random import random

from src.application.tmdb.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.tmdb.interfaces.i_tmdb_api_adapter import ITMDBAPIAdapter
from src.application.tmdb.result_dto.tv_dto import TvDTO
from src.application.tmdb.interfaces.i_find_random_tv_usecase import IGetRandomTvUseCase


class GetRandomTvUseCase(IGetRandomTvUseCase):
    """
    Returns one random tv matching the filter.
    """

    def __init__(self, adapter: ITMDBAPIAdapter) -> None:
        self._adapter = adapter

    async def __call__(self, filter_dto: TvFilterDTO) -> TvDTO | None:
        first_page = await self._adapter.fetch_random_movies(
            replace(filter_dto, page=1),
        )

        if not first_page.results:
            return None

        return random.choice(first_page.results)