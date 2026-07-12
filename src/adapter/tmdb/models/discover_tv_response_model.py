from src.adapter.tmdb.models.base_discover_response_model import TMDBDiscoverResponse
from src.application.tmdb.result_dto.tv_dto import TvDTO


class TMDBDiscoverTvResponse(TMDBDiscoverResponse):
    results: list[TvDTO]