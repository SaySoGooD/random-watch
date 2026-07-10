from dataclasses import dataclass
from typing import Literal


@dataclass
class GenreDTO:
    id: int
    name: str


@dataclass
class CompanyDTO:
    id: int
    name: str


@dataclass
class KeywordDTO:
    id: int
    name: str


@dataclass
class RangeDTO:
    min: float
    max: float


@dataclass
class DateRangeDTO:
    from_: str
    to: str


@dataclass
class YearRangeDTO:
    from_: int
    to: int


@dataclass
class ReleaseDateDTO:
    year: YearRangeDTO
    date: DateRangeDTO


@dataclass
class GenresDTO:
    include: list[GenreDTO]
    exclude: list[GenreDTO]


@dataclass
class CertificationDTO:
    country: str
    allowed: list[str]


@dataclass
class SortDTO:
    field: str
    direction: Literal["asc", "desc"]


@dataclass
class RandomDTO:
    enabled: bool
    seed: int | None


@dataclass
class PaginationDTO:
    page: int | None
    limit: int

@dataclass
class AirDateDTO:
    year: "YearRangeDTO"
    date: "DateRangeDTO"


@dataclass
class YearRangeDTO:
    from_: int
    to: int


@dataclass
class DateRangeDTO:
    from_: str
    to: str


@dataclass
class RuntimeDTO:
    min: int
    max: int


@dataclass
class SeasonsDTO:
    min: int
    max: int


@dataclass
class EpisodesDTO:
    min: int
    max: int


@dataclass
class NetworkDTO:
    id: int
    name: str


@dataclass
class ContentRatingsDTO:
    country: str
    allowed: list[str]
