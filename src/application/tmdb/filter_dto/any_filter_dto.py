from dataclasses import dataclass, fields
from typing import ClassVar, Literal

from src.application.tmdb.filter_dto.base_filter_dto import BaseFilterDTO
from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.filter_dto.tv_filter_dto import TvFilterDTO


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
        shared = {
            field.name: getattr(self, field.name)
            for field in fields(BaseFilterDTO)
        }
        return MovieFilterDTO(**shared), TvFilterDTO(**shared)