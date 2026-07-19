from abc import ABC, abstractmethod

from random_watch.application.find_random_video.filter_dto.any_filter_dto import AnyFilterDTO
from random_watch.entities.movie import Movie
from random_watch.entities.tv import Tv


class IGetRandomCollectionUseCase(ABC):
    @abstractmethod
    async def __call__(
        self,
        filter_dto: AnyFilterDTO,
        count: int = 5,
    ) -> list[Movie | Tv]: 
        ...
