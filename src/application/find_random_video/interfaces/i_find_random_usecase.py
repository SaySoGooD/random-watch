from abc import ABC, abstractmethod

from src.application.find_random_video.filter_dto.any_filter_dto import AnyFilterDTO
from src.application.find_random_video.result_dto.movie_dto import MovieDTO
from src.application.find_random_video.result_dto.tv_dto import TvDTO


class IGetRandomCollectionUseCase(ABC):
    @abstractmethod
    async def __call__(
        self,
        filter_dto: AnyFilterDTO,
        count: int = 5,
    ) -> list[MovieDTO | TvDTO]: ...
