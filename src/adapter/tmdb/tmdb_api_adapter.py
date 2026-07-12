from types import TracebackType

import aiohttp

from src.adapter.tmdb.models.discover_movie_response_model import (
    TMDBDiscoverMovieResponse,
)
from src.adapter.tmdb.models.discover_tv_response_model import TMDBDiscoverTvResponse
from src.adapter.tmdb.models.genre_model import TMDBGenreResponseModel
from src.application.find_random_video.exceptions import (
    APIConnectionError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
    APIUnauthorizedError,
)
from src.application.find_random_video.filter_dto.base_filter_dto import api_params
from src.application.find_random_video.filter_dto.filter_settings_dto import GenreDTO
from src.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.find_random_video.interfaces.i_tmdb_api_adapter import (
    ITMDBAPIAdapter,
)
from src.application.find_random_video.result_dto.movie_dto import MovieDTO
from src.application.find_random_video.result_dto.tv_dto import TvDTO


class TMDBAPIAdapter(ITMDBAPIAdapter):
    """Adapter for the TMDB REST API."""

    _BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._session: aiohttp.ClientSession | None = None

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

    @property
    def session(self) -> aiohttp.ClientSession:
        """Return the active HTTP session, creating it lazily if needed."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    @session.setter
    def session(self, value: aiohttp.ClientSession) -> None:
        self._session = value

    async def __aenter__(self) -> "TMDBAPIAdapter":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc: BaseException | None = None,
        tb: TracebackType | None = None,
    ) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def _get(
        self, path: str, params: MovieFilterDTO | TvFilterDTO | dict
    ) -> dict:
        """Send a GET request and return the parsed JSON body."""
        raw = params if isinstance(params, dict) else api_params(params)
        clean = {
            k: v for k, v in {**raw, "api_key": self._api_key}.items() if v is not None
        }

        try:
            async with self.session.get(
                f"{self._BASE_URL}{path}", params=clean
            ) as response:
                match response.status:
                    case 401:
                        raise APIUnauthorizedError("Invalid or missing API key.")
                    case 404:
                        raise APINotFoundError(f"Resource not found: {path}")
                    case 429:
                        raise APIRateLimitError("TMDB API rate limit exceeded.")
                    case status if status >= 500:
                        raise APIServerError(f"TMDB server error: {status}")

                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientConnectionError as e:
            raise APIConnectionError(f"Failed to connect to TMDB API: {e}") from e

    def _to_genre_dtos(self, data: dict) -> list[GenreDTO]:
        """Convert raw genre data to GenreDTO list."""
        genres = TMDBGenreResponseModel.model_validate(data).genres

        return [
            GenreDTO(
                id=genre.id,
                name=genre.name,
            )
            for genre in genres
        ]
