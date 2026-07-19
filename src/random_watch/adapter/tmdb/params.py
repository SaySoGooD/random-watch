from dataclasses import fields

# Filter DTO attributes whose TMDB query key differs from the attribute name.
_PARAM_KEYS = {
    "vote_average_gte": "vote_average.gte",
    "vote_average_lte": "vote_average.lte",
    "vote_count_gte": "vote_count.gte",
    "vote_count_lte": "vote_count.lte",
    "popularity_gte": "popularity.gte",
    "popularity_lte": "popularity.lte",
    "with_runtime_gte": "with_runtime.gte",
    "with_runtime_lte": "with_runtime.lte",
    "primary_release_date_gte": "primary_release_date.gte",
    "primary_release_date_lte": "primary_release_date.lte",
    "air_date_gte": "air_date.gte",
    "air_date_lte": "air_date.lte",
}

# Filter DTO attributes that are not TMDB query params at all.
_EXCLUDED_FROM_PARAMS = frozenset({"random"})


def api_params(filter_dto: object) -> dict[str, object]:
    """Build TMDB query params from an application filter DTO."""
    result: dict[str, object] = {}

    for dto_field in fields(filter_dto):
        if dto_field.name in _EXCLUDED_FROM_PARAMS:
            continue

        value = getattr(filter_dto, dto_field.name)
        if value is None:
            continue

        result[_PARAM_KEYS.get(dto_field.name, dto_field.name)] = value

    return result
