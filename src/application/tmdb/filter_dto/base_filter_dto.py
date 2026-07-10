from dataclasses import dataclass

from src.application.tmdb.filter_dto.filter_settings_dto import (
    GenresDTO, RangeDTO, CompanyDTO, KeywordDTO,
    SortDTO, RandomDTO, PaginationDTO, RuntimeDTO,
)


@dataclass
class BaseFilterDTO:
    language: str | None = None
    region: str | None = None
    genres: GenresDTO | None = None
    rating: RangeDTO | None = None
    votes: RangeDTO | None = None
    popularity: RangeDTO | None = None
    runtime: RuntimeDTO | None = None
    originalLanguage: list[str] | None = None
    countries: list[str] | None = None
    companies: list[CompanyDTO] | None = None
    keywords: list[KeywordDTO] | None = None
    adult: bool | None = None
    sort: SortDTO | None = None
    random: RandomDTO | None = None
    pagination: PaginationDTO | None = None