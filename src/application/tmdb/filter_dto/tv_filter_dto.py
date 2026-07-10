# tv_filter_dto.py
from dataclasses import dataclass
from typing import ClassVar, Literal

from src.application.tmdb.filter_dto.base_filter_dto import BaseFilterDTO
from src.application.tmdb.filter_dto.filter_settings_dto import (
    AirDateDTO, NetworkDTO, ContentRatingsDTO,
)


@dataclass
class TvFilterDTO(BaseFilterDTO):
    contentType: ClassVar[Literal["tv"]] = "tv"

    airDate: AirDateDTO | None = None
    status: list[str] | None = None
    networks: list[NetworkDTO] | None = None
    contentRatings: ContentRatingsDTO | None = None
    spokenLanguages: list[str] | None = None
    originCountries: list[str] | None = None