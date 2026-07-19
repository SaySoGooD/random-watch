from dataclasses import dataclass, field, fields

from random_watch.application.find_random_video.filter_dto.filter_settings_dto import RandomDTO

_EXCLUDED_FROM_PARAMS = frozenset({"random"})


def param(key: str, default=None):
    """Declare a DTO field whose TMDB query key may differ from the attribute name."""
    return field(default=default, metadata={"param": key})


def api_params(dto: object) -> dict[str, object]:
    """
    Build TMDB query params from a filter DTO.

    Reads field values as-is; only maps attribute names to query keys via metadata.
    """
    result: dict[str, object] = {}

    for dto_field in fields(dto):
        if dto_field.name in _EXCLUDED_FROM_PARAMS:
            continue

        value = getattr(dto, dto_field.name)
        if value is None:
            continue

        key = dto_field.metadata.get("param", dto_field.name)
        result[key] = value

    return result


def base_filter_values(source: object) -> dict[str, object]:
    """Copy shared BaseFilterDTO field values from *source*."""
    return {
        dto_field.name: getattr(source, dto_field.name)
        for dto_field in fields(BaseFilterDTO)
    }


@dataclass
class BaseFilterDTO:
    """
    Shared TMDB /discover query params.

    Values are stored in API-ready form. Use api_params() to get the query dict.
    """

    language: str | None = None
    region: str | None = None
    include_adult: bool | None = None

    with_genres: str | None = None
    without_genres: str | None = None

    vote_average_gte: float | None = param("vote_average.gte")
    vote_average_lte: float | None = param("vote_average.lte")

    vote_count_gte: float | None = param("vote_count.gte")
    vote_count_lte: float | None = param("vote_count.lte")

    popularity_gte: float | None = param("popularity.gte")
    popularity_lte: float | None = param("popularity.lte")

    with_runtime_gte: int | None = param("with_runtime.gte")
    with_runtime_lte: int | None = param("with_runtime.lte")

    with_original_language: str | None = None
    with_origin_country: str | None = None
    with_companies: str | None = None
    with_keywords: str | None = None

    sort_by: str | None = None

    random: RandomDTO | None = None
