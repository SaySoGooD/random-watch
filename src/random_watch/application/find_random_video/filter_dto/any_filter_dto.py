from dataclasses import dataclass
from typing import ClassVar, Literal

from random_watch.application.find_random_video.filter_dto.base_filter_dto import (
    BaseFilterDTO, base_filter_values)
from random_watch.application.find_random_video.filter_dto.movie_filter_dto import \
    MovieFilterDTO
from random_watch.application.find_random_video.filter_dto.tv_filter_dto import \
    TvFilterDTO


@dataclass
class AnyFilterDTO(BaseFilterDTO):
    """
    Filter for searching across both movies and TV shows simultaneously.
    Contains only fields supported by both content types.
    Use split() to get individual filters for parallel requests.
    """

    contentType: ClassVar[Literal["any"]] = "any"

    def split(self) -> tuple[MovieFilterDTO, TvFilterDTO]:
        """Split into two filters for parallel movie and TV requests."""
        shared = base_filter_values(self)
        return MovieFilterDTO(**shared), TvFilterDTO(**shared)
