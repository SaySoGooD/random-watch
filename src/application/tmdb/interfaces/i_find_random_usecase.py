from abc import ABC, abstractmethod

from src.application.tmdb.result_dto.movie_dto import MovieDTO
from src.application.tmdb.filter_dto.any_filter_dto import AnyFilterDTO
from src.application.tmdb.result_dto.tv_dto import TvDTO


class IGetRandomCollectionUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        filter_dto: AnyFilterDTO,
        count: int = 5,
    ) -> list[MovieDTO | TvDTO]:
        ...