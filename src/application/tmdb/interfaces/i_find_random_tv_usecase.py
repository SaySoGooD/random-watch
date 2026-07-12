from abc import ABC, abstractmethod

from src.application.tmdb.result_dto.tv_dto import TvDTO
from src.application.tmdb.filter_dto.tv_filter_dto import TvFilterDTO


class IGetRandomTvUseCase(ABC):
    @abstractmethod
    async def __call__(
        self,
        filter_dto: TvFilterDTO,
    ) -> TvDTO | None:
        ...