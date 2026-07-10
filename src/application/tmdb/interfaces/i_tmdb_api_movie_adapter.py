from typing import Protocol

from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.api_dto.tmdb_movie_response_dto import TMDBDiscoverMovieResponseDTO


class ITMDBAPIMovieAdapter(Protocol):
    async def discover(self, filter_dto: MovieFilterDTO) -> TMDBDiscoverMovieResponseDTO:
        """Fetch movies from TMDB discover endpoint."""
        ...