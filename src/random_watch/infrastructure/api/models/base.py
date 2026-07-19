from pydantic import BaseModel, ConfigDict, Field


class BaseSearchQuery(BaseModel):
    """Common discover filter parameters shared across all media types."""

    language: str | None = Field(
        default=None, description="ISO 639-1 language code, e.g. 'en'"
    )
    region: str | None = Field(
        default=None, description="ISO 3166-1 country code, e.g. 'US'"
    )
    include_adult: bool | None = Field(
        default=None, description="Include adult content"
    )
    with_genres: str | None = Field(
        default=None, description="Comma-separated genre IDs to include, e.g. '28,12'"
    )
    without_genres: str | None = Field(
        default=None, description="Comma-separated genre IDs to exclude"
    )
    vote_average_gte: float | None = Field(
        default=None, description="Minimum average vote score"
    )
    vote_average_lte: float | None = Field(
        default=None, description="Maximum average vote score"
    )
    vote_count_gte: float | None = Field(
        default=None, description="Minimum number of votes"
    )
    vote_count_lte: float | None = Field(
        default=None, description="Maximum number of votes"
    )
    popularity_gte: float | None = Field(
        default=None, description="Minimum popularity score"
    )
    popularity_lte: float | None = Field(
        default=None, description="Maximum popularity score"
    )
    with_runtime_gte: int | None = Field(
        default=None, description="Minimum runtime in minutes"
    )
    with_runtime_lte: int | None = Field(
        default=None, description="Maximum runtime in minutes"
    )
    with_original_language: str | None = Field(
        default=None, description="ISO 639-1 original language code, e.g. 'en'"
    )
    with_origin_country: str | None = Field(
        default=None, description="ISO 3166-1 origin country code, e.g. 'US'"
    )
    with_companies: str | None = Field(
        default=None, description="Comma-separated production company IDs"
    )
    with_keywords: str | None = Field(
        default=None, description="Comma-separated keyword IDs"
    )


class BaseMediaResponse(BaseModel):
    """Common response fields shared by movie and TV response models."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="TMDB item ID")
    overview: str | None = Field(default=None, description="Plot summary")
    poster_path: str | None = Field(
        default=None,
        description="Poster image path, append to 'https://image.tmdb.org/t/p/w500'",
    )
    backdrop_path: str | None = Field(
        default=None,
        description="Backdrop image path, append to 'https://image.tmdb.org/t/p/original'",
    )
    vote_average: float | None = Field(
        default=None, description="Average vote score (0–10)"
    )
    vote_count: int | None = Field(default=None, description="Total number of votes")
    popularity: float | None = Field(default=None, description="TMDB popularity score")
    adult: bool | None = Field(
        default=None, description="Whether the item is adult content"
    )
    genre_ids: list[int] = Field(default_factory=list, description="List of genre IDs")
    original_language: str | None = Field(
        default=None, description="ISO 639-1 original language code, e.g. 'en'"
    )
