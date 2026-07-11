from src.application.tmdb.result_dto.movie_dto import MovieDTO
from src.adapter.tmdb.models.discover_tv_response_model import TMDBDiscoverTvResponse


class TMDBDiscoverMovieResponse(TMDBDiscoverTvResponse):
    results: list[MovieDTO]
