from src.adapter.tmdb.models.discover_tv_response_model import TMDBDiscoverTvResponse
from src.application.find_random_video.result_dto.movie_dto import MovieDTO


class TMDBDiscoverMovieResponse(TMDBDiscoverTvResponse):
    results: list[MovieDTO]
