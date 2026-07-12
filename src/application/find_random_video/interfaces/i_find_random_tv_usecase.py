from abc import ABC, abstractmethod

from src.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.find_random_video.result_dto.tv_dto import TvDTO


class IGetRandomTvUseCase(ABC):
    @abstractmethod
    async def __call__(
        self,
        filter_dto: TvFilterDTO,
    ) -> TvDTO | None: ...
