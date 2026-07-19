from dataclasses import dataclass
from typing import ClassVar, Literal

from random_watch.application.find_random_video.filter_dto.base_filter_dto import \
    BaseFilterDTO


@dataclass
class MovieFilterDTO(BaseFilterDTO):
    contentType: ClassVar[Literal["movie"]] = "movie"

    primary_release_date_gte: str | None = None
    primary_release_date_lte: str | None = None
    primary_release_year: int | None = None

    certification_country: str | None = None
    certification: str | None = None

    with_release_type: str | None = None
    include_video: bool | None = None
