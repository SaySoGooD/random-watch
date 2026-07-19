from dataclasses import dataclass, fields

from random_watch.application.find_random_video.filter_dto.filter_settings_dto import \
    RandomDTO


def base_filter_values(source: object) -> dict[str, object]:
    """Copy shared BaseFilterDTO field values from *source*."""
    return {
        dto_field.name: getattr(source, dto_field.name)
        for dto_field in fields(BaseFilterDTO)
    }


@dataclass
class BaseFilterDTO:
    """Shared discover filter fields for all media types."""

    language: str | None = None
    region: str | None = None
    include_adult: bool | None = None

    with_genres: str | None = None
    without_genres: str | None = None

    vote_average_gte: float | None = None
    vote_average_lte: float | None = None

    vote_count_gte: float | None = None
    vote_count_lte: float | None = None

    popularity_gte: float | None = None
    popularity_lte: float | None = None

    with_runtime_gte: int | None = None
    with_runtime_lte: int | None = None

    with_original_language: str | None = None
    with_origin_country: str | None = None
    with_companies: str | None = None
    with_keywords: str | None = None

    sort_by: str | None = None

    random: RandomDTO | None = None
