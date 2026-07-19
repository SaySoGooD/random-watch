from types import TracebackType

import aiohttp

from random_watch.adapter.tmdb.models.discover_movie_response_model import (
    TMDBDiscoverMovieResponse,
)
from random_watch.adapter.tmdb.models.discover_tv_response_model import TMDBDiscoverTvResponse
from random_watch.adapter.tmdb.models.genre_model import TMDBGenreResponseModel
from random_watch.application.find_random_video.exceptions import (
    APIConnectionError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
    APIUnauthorizedError,
)


class TMDBPresenter:
    """Talks to the TMDB REST API and returns raw TMDB models."""

    _BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._session: aiohttp.ClientSession | None = None

    async def discover_movies(self, params: dict) -> TMDBDiscoverMovieResponse:
        """Return a raw page of movies from /discover/movie."""
        data = await self._get("/discover/movie", params)
        return TMDBDiscoverMovieResponse.model_validate(data)

    async def discover_tv(self, params: dict) -> TMDBDiscoverTvResponse:
        """Return a raw page of TV shows from /discover/tv."""
        data = await self._get("/discover/tv", params)
        return TMDBDiscoverTvResponse.model_validate(data)

    async def movie_genres(self, language: str | None = None) -> TMDBGenreResponseModel:
        """Return the raw movie genre list."""
        data = await self._get("/genre/movie/list", {"language": language})
        return TMDBGenreResponseModel.model_validate(data)

    async def tv_genres(self, language: str | None = None) -> TMDBGenreResponseModel:
        """Return the raw TV genre list."""
        data = await self._get("/genre/tv/list", {"language": language})
        return TMDBGenreResponseModel.model_validate(data)

    @property
    def session(self) -> aiohttp.ClientSession:
        """Return the active HTTP session, creating it lazily if needed."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    @session.setter
    def session(self, value: aiohttp.ClientSession) -> None:
        self._session = value

    async def __aenter__(self) -> "TMDBPresenter":
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

    async def _get(self, path: str, params: dict) -> dict:
        """Send a GET request and return the parsed JSON body."""
        clean = {k: v for k, v in params.items() if v is not None}

        headers = {"Authorization": f"Bearer {self._api_key}"}

        try:
            async with self.session.get(
                f"{self._BASE_URL}{path}", params=clean, headers=headers
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
