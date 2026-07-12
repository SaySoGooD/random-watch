from dataclasses import replace
from random import random

from src.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.find_random_video.interfaces.i_find_random_tv_usecase import (
    IGetRandomTvUseCase,
)
from src.application.find_random_video.interfaces.i_tmdb_api_adapter import (
    ITMDBAPIAdapter,
)
from src.application.find_random_video.result_dto.tv_dto import TvDTO


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
