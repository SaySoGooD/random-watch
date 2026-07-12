from dataclasses import dataclass
from typing import ClassVar, Literal

from src.application.tmdb.filter_dto.base_filter_dto import BaseFilterDTO, param


@dataclass
class MovieFilterDTO(BaseFilterDTO):
    contentType: ClassVar[Literal["movie"]] = "movie"

    primary_release_date_gte: str | None = param("primary_release_date.gte")
    primary_release_date_lte: str | None = param("primary_release_date.lte")
    primary_release_year: int | None = None

    certification_country: str | None = None
    certification: str | None = None

    with_release_type: str | None = None
    include_video: bool | None = None
