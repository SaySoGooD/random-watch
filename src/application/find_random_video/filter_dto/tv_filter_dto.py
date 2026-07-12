from dataclasses import dataclass
from typing import ClassVar, Literal

from src.application.find_random_video.filter_dto.base_filter_dto import (
    BaseFilterDTO,
    param,
)


@dataclass
class TvFilterDTO(BaseFilterDTO):
    contentType: ClassVar[Literal["tv"]] = "tv"

    air_date_gte: str | None = param("air_date.gte")
    air_date_lte: str | None = param("air_date.lte")
    first_air_date_year: int | None = None

    certification_country: str | None = None
    certification: str | None = None

    with_networks: str | None = None
    with_status: str | None = None
    with_spoken_languages: str | None = None
