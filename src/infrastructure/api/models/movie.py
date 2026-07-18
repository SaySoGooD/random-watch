from pydantic import BaseModel, Field

from src.infrastructure.api.models.base import BaseMediaResponse, BaseSearchQuery
from src.infrastructure.api.models.enums import MovieSortBy, ReleaseType


class MovieResponseModel(BaseMediaResponse):
    """Response schema for a single movie entry."""

    title: str = Field(description="Movie title in the requested language")
    original_title: str | None = Field(default=None, description="Movie title in the original language")
    release_date: str | None = Field(default=None, description="Primary release date, e.g. '2023-07-19'")


class MovieSearchQuery(BaseSearchQuery):
    """Query parameters unique to movie discovery."""

    sort_by: MovieSortBy | None = Field(default=None, description="Sort results by the given field")
    primary_release_date_gte: str | None = Field(default=None, description="Minimum primary release date, e.g. '2020-01-01'")
    primary_release_date_lte: str | None = Field(default=None, description="Maximum primary release date, e.g. '2024-12-31'")
    primary_release_year: int | None = Field(default=None, description="Filter by primary release year, e.g. 2023")
    certification_country: str | None = Field(default=None, description="ISO 3166-1 country code for certification, e.g. 'US'")
    certification: str | None = Field(default=None, description="Certification rating, e.g. 'PG-13'")
    with_release_type: ReleaseType | None = Field(default=None, description="Filter by release type")
    include_video: bool | None = Field(default=None, description="Include video releases")


class RandomMovieResponseModel(BaseModel):
    """Envelope wrapping a single randomly selected movie."""

    movie: MovieResponseModel