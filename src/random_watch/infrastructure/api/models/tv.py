from pydantic import BaseModel, Field

from random_watch.infrastructure.api.models.base import BaseMediaResponse, BaseSearchQuery
from random_watch.infrastructure.api.models.enums import TvSortBy, TvStatus


class TvResponseModel(BaseMediaResponse):
    """Response schema for a single TV show entry."""

    name: str = Field(description="TV show title in the requested language")
    original_name: str | None = Field(default=None, description="TV show title in the original language")
    first_air_date: str | None = Field(default=None, description="First air date, e.g. '2023-07-19'")
    origin_country: list[str] = Field(default_factory=list, description="List of ISO 3166-1 origin country codes, e.g. ['US']")


class TvSearchQuery(BaseSearchQuery):
    """Query parameters unique to TV show discovery."""

    sort_by: TvSortBy | None = Field(default=None, description="Sort results by the given field")
    air_date_gte: str | None = Field(default=None, description="Minimum air date, e.g. '2020-01-01'")
    air_date_lte: str | None = Field(default=None, description="Maximum air date, e.g. '2024-12-31'")
    first_air_date_year: int | None = Field(default=None, description="Filter by first air date year, e.g. 2023")
    certification_country: str | None = Field(default=None, description="ISO 3166-1 country code for certification, e.g. 'US'")
    certification: str | None = Field(default=None, description="Certification rating, e.g. 'TV-MA'")
    with_networks: str | None = Field(default=None, description="Comma-separated network IDs, e.g. '213' for Netflix")
    with_status: TvStatus | None = Field(default=None, description="Filter by series status")
    with_spoken_languages: str | None = Field(default=None, description="ISO 639-1 spoken language code, e.g. 'en'")


class RandomTvResponseModel(BaseModel):
    """Envelope wrapping a single randomly selected TV show."""

    tv: TvResponseModel