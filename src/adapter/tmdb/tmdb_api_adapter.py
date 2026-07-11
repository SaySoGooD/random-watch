import aiohttp

from src.application.tmdb.interfaces.i_tmdb_api_adapter import ITMDBAPIAdapter
from src.application.tmdb.filter_dto.base_filter_dto import api_params
from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.tmdb.result_dto.movie_dto import MovieDTO
from src.application.tmdb.result_dto.tv_dto import TvDTO
from src.application.tmdb.filter_dto.filter_settings_dto import GenreDTO
from src.adapter.tmdb.models.discover_movie_response_model import TMDBDiscoverMovieResponse
from src.adapter.tmdb.models.discover_tv_response_model import TMDBDiscoverTvResponse
from src.adapter.tmdb.models.genre_model import TMDBGenreResponseModel


class TMDBAPIAdapter(ITMDBAPIAdapter):
    """Adapter for the TMDB REST API."""

    _BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        self._api_key = api_key
        self._session = session

    async def fetch_random_movies(self, filter_dto: MovieFilterDTO) -> list[MovieDTO]:
        """Return a page of movies matching the given filter."""
        data = await self._get("/discover/movie", filter_dto)
        return TMDBDiscoverMovieResponse.model_validate(data).results

    async def fetch_random_tv(self, filter_dto: TvFilterDTO) -> list[TvDTO]:
        """Return a page of TV shows matching the given filter."""
        data = await self._get("/discover/tv", filter_dto)
        return TMDBDiscoverTvResponse.model_validate(data).results

    async def fetch_movie_genres(self, language: str | None = None) -> list[GenreDTO]:
        """Return all available movie genres."""
        data = await self._get("/genre/movie/list", {"language": language})
        return self._to_genre_dtos(data)

    async def fetch_tv_genres(self, language: str | None = None) -> list[GenreDTO]:
        """Return all available TV genres."""
        data = await self._get("/genre/tv/list", {"language": language})
        return self._to_genre_dtos(data)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _get(self, path: str, params: MovieFilterDTO | TvFilterDTO | dict) -> dict:
        """Send a GET request and return the parsed JSON body."""
        raw = params if isinstance(params, dict) else api_params(params)
        clean = {k: v for k, v in {**raw, "api_key": self._api_key}.items() if v is not None}

        async with self._session.get(f"{self._BASE_URL}{path}", params=clean) as response:
            response.raise_for_status()
            return await response.json()

    def _to_genre_dtos(self, data: dict) -> list[GenreDTO]:
        genres = TMDBGenreResponseModel.model_validate(data).genres

        return [
            GenreDTO(
                id=genre.id,
                name=genre.name,
            )
            for genre in genres
        ]