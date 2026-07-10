# use_cases/get_random_movies_use_case.py
import random

from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.filter_dto.filter_settings_dto import PaginationDTO
from src.application.tmdb.api_dto.tmdb_movie_response_dto import TMDBMovieDTO
from src.application.tmdb.interfaces.i_tmdb_api_movie_adapter import IMovieAdapter


class GetRandomMoviesUseCase:
    """
    Returns up to MAX_RESULTS randomly picked movies from page 1
    of TMDB discover results matching the given filter.
    """

    MAX_RESULTS = 5

    def __init__(self, adapter: IMovieAdapter) -> None:
        self._adapter = adapter

    async def execute(self, filter_dto: MovieFilterDTO) -> list[TMDBMovieDTO]:
        """
        Fetch page 1 from TMDB, shuffle results, return up to MAX_RESULTS.
        """
        normalized = self._force_page_one(filter_dto)
        response = await self._adapter.discover(normalized)

        if not response.results:
            return []

        shuffled = random.sample(
            response.results,
            k=min(self.MAX_RESULTS, len(response.results)),
        )
        return shuffled

    def _force_page_one(self, filter_dto: MovieFilterDTO) -> MovieFilterDTO:
        """Return a copy of the filter with pagination forced to page 1."""
        from dataclasses import replace
        return replace(filter_dto, pagination=PaginationDTO(page=1))