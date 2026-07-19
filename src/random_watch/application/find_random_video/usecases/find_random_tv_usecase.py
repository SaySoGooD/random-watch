import random

from random_watch.application.common.errors import TvNotFoundError
from random_watch.application.find_random_video.filter_dto.tv_filter_dto import \
    TvFilterDTO
from random_watch.application.find_random_video.interfaces.gateways import \
    TvGateway
from random_watch.application.find_random_video.interfaces.i_find_random_tv_usecase import \
    IGetRandomTvUseCase
from random_watch.entities.tv import Tv


class GetRandomTvUseCase(IGetRandomTvUseCase):
    """
    Returns one random tv matching the filter.
    """

    def __init__(self, gateway: TvGateway) -> None:
        self._gateway = gateway

    async def __call__(self, filter_dto: TvFilterDTO) -> Tv:
        tv_shows = await self._gateway.fetch_random_tv(filter_dto)

        if not tv_shows:
            raise TvNotFoundError()

        return random.choice(tv_shows)
