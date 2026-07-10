# movie_filter_dto.py
from dataclasses import dataclass
from typing import ClassVar, Literal

from src.application.tmdb.filter_dto.base_filter_dto import BaseFilterDTO
from src.application.tmdb.filter_dto.filter_settings_dto import (
    ReleaseDateDTO, CertificationDTO,
)


@dataclass
class MovieFilterDTO(BaseFilterDTO):
    contentType: ClassVar[Literal["movie"]] = "movie"

    releaseDate: ReleaseDateDTO | None = None
    certification: CertificationDTO | None = None
    releaseTypes: list[int] | None = None
    video: bool | None = None