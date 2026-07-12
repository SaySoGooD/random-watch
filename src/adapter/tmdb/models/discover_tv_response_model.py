from src.adapter.tmdb.models.base_discover_response_model import TMDBDiscoverResponse
from src.application.find_random_video.result_dto.tv_dto import TvDTO


class TMDBDiscoverTvResponse(TMDBDiscoverResponse):
    results: list[TvDTO]
