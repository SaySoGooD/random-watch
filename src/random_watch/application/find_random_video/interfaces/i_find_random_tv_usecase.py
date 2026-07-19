from abc import ABC, abstractmethod

from random_watch.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from random_watch.entities.tv import Tv


class IGetRandomTvUseCase(ABC):
    @abstractmethod
    async def __call__(
        self,
        filter_dto: TvFilterDTO,
    ) -> Tv:
        ...
