from unittest.mock import AsyncMock, MagicMock

import pytest

from random_watch.adapter.tmdb.models.discover_movie_response_model import \
    TMDBDiscoverMovieResponse
from random_watch.adapter.tmdb.models.discover_tv_response_model import \
    TMDBDiscoverTvResponse
from random_watch.adapter.tmdb.models.genre_model import TMDBGenreResponseModel
from random_watch.adapter.tmdb.params import api_params
from random_watch.adapter.tmdb.tmdb_client import TMDBClient
from random_watch.adapter.tmdb.tmdb_gateway import TMDBGateway
from random_watch.application.find_random_video.exceptions import (
    APINotFoundError, APIRateLimitError, APIServerError, APIUnauthorizedError)
from random_watch.application.find_random_video.filter_dto.filter_settings_dto import \
    RandomDTO
from random_watch.application.find_random_video.filter_dto.movie_filter_dto import \
    MovieFilterDTO
from random_watch.application.find_random_video.filter_dto.tv_filter_dto import \
    TvFilterDTO
from random_watch.entities.genre import Genre
from random_watch.entities.movie import Movie
from random_watch.entities.tv import Tv

_API_KEY = "test_api_key_abc"

_MOVIE_PAYLOAD: dict = {
    "results": [
        {
            "id": 101,
            "title": "Inception",
            "original_title": "Inception",
            "overview": "A mind-bending thriller.",
            "poster_path": "/inception.jpg",
            "backdrop_path": "/inception_bg.jpg",
            "release_date": "2010-07-16",
            "vote_average": 8.8,
            "vote_count": 35_000,
            "popularity": 120.5,
            "adult": False,
            "genre_ids": [28, 878],
            "original_language": "en",
        }
    ],
}

_TV_PAYLOAD: dict = {
    "results": [
        {
            "id": 202,
            "name": "Breaking Bad",
            "original_name": "Breaking Bad",
            "overview": "A chemistry teacher turns to crime.",
            "poster_path": "/bb.jpg",
            "backdrop_path": "/bb_bg.jpg",
            "first_air_date": "2008-01-20",
            "vote_average": 9.5,
            "vote_count": 12_000,
            "popularity": 200.0,
            "adult": False,
            "genre_ids": [18, 80],
            "original_language": "en",
            "origin_country": ["US"],
        }
    ],
}

_GENRES_PAYLOAD: dict = {
    "genres": [
        {"id": 28, "name": "Action"},
        {"id": 12, "name": "Adventure"},
    ]
}


def _make_session(payload: dict, status: int = 200) -> MagicMock:
    """Build a mock aiohttp.ClientSession whose GET returns *payload* as JSON."""
    response = AsyncMock()
    response.status = status
    response.raise_for_status = MagicMock()
    response.json = AsyncMock(return_value=payload)

    session = MagicMock()
    session.get.return_value.__aenter__ = AsyncMock(return_value=response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=False)

    return session


def _make_client(payload: dict, status: int = 200) -> tuple[TMDBClient, MagicMock]:
    client = TMDBClient(_API_KEY)
    session = _make_session(payload, status)
    client.session = session
    return client, session


class TestApiParams:
    """Tests for the filter DTO → TMDB query params conversion."""

    def test_maps_dotted_keys(self):
        params = api_params(
            MovieFilterDTO(vote_average_gte=7.5, primary_release_date_gte="2020-01-01")
        )

        assert params == {
            "vote_average.gte": 7.5,
            "primary_release_date.gte": "2020-01-01",
        }

    def test_plain_fields_pass_through(self):
        params = api_params(
            MovieFilterDTO(with_genres="28,12", sort_by="popularity.desc")
        )

        assert params == {"with_genres": "28,12", "sort_by": "popularity.desc"}

    def test_none_values_dropped(self):
        assert api_params(MovieFilterDTO()) == {}

    def test_random_field_excluded(self):
        params = api_params(MovieFilterDTO(random=RandomDTO(enabled=True, seed=42)))

        assert params == {}


class TestTMDBClient:
    """Tests for the raw HTTP client."""

    @pytest.mark.asyncio
    async def test_returns_parsed_movie_response(self):
        client, _ = _make_client(_MOVIE_PAYLOAD)
        response = await client.discover_movies({"with_genres": "28"})

        assert isinstance(response, TMDBDiscoverMovieResponse)
        assert response.results[0].title == "Inception"

    @pytest.mark.asyncio
    async def test_none_params_stripped(self):
        client, session = _make_client(_GENRES_PAYLOAD)
        await client.movie_genres(language=None)

        assert session.get.call_args.kwargs["params"] == {}

    @pytest.mark.asyncio
    async def test_bearer_header_sent(self):
        client, session = _make_client(_GENRES_PAYLOAD)
        await client.tv_genres(language="de")

        headers = session.get.call_args.kwargs["headers"]
        assert headers["Authorization"] == f"Bearer {_API_KEY}"

    @pytest.mark.asyncio
    async def test_401_raises_unauthorized(self):
        client, _ = _make_client({}, status=401)
        with pytest.raises(APIUnauthorizedError):
            await client.discover_movies({})

    @pytest.mark.asyncio
    async def test_404_raises_not_found(self):
        client, _ = _make_client({}, status=404)
        with pytest.raises(APINotFoundError):
            await client.discover_tv({})

    @pytest.mark.asyncio
    async def test_429_raises_rate_limit(self):
        client, _ = _make_client({}, status=429)
        with pytest.raises(APIRateLimitError):
            await client.movie_genres()

    @pytest.mark.asyncio
    async def test_500_raises_server_error(self):
        client, _ = _make_client({}, status=500)
        with pytest.raises(APIServerError):
            await client.tv_genres()

    @pytest.mark.asyncio
    async def test_close_shuts_session(self):
        client, session = _make_client(_GENRES_PAYLOAD)
        session.close = AsyncMock()
        await client.close()

        session.close.assert_awaited_once()


class TestTMDBGateway:
    """Tests for the raw model → entity mapping."""

    def _gateway_with(self, **client_methods) -> TMDBGateway:
        client = MagicMock()
        for name, value in client_methods.items():
            setattr(client, name, AsyncMock(return_value=value))
        return TMDBGateway(client)

    @pytest.mark.asyncio
    async def test_movies_mapped_to_entities(self):
        gateway = self._gateway_with(
            discover_movies=TMDBDiscoverMovieResponse.model_validate(_MOVIE_PAYLOAD)
        )
        movies = await gateway.fetch_random_movies(MovieFilterDTO())

        assert len(movies) == 1
        movie = movies[0]
        assert isinstance(movie, Movie)
        assert movie.id == 101
        assert movie.title == "Inception"
        assert movie.release_date == "2010-07-16"
        assert movie.genre_ids == [28, 878]

    @pytest.mark.asyncio
    async def test_tv_mapped_to_entities(self):
        gateway = self._gateway_with(
            discover_tv=TMDBDiscoverTvResponse.model_validate(_TV_PAYLOAD)
        )
        tv_shows = await gateway.fetch_random_tv(TvFilterDTO())

        assert len(tv_shows) == 1
        tv = tv_shows[0]
        assert isinstance(tv, Tv)
        assert tv.id == 202
        assert tv.name == "Breaking Bad"
        assert tv.origin_country == ["US"]

    @pytest.mark.asyncio
    async def test_genres_mapped_to_entities(self):
        gateway = self._gateway_with(
            movie_genres=TMDBGenreResponseModel.model_validate(_GENRES_PAYLOAD)
        )
        genres = await gateway.fetch_movie_genres()

        assert genres == [Genre(id=28, name="Action"), Genre(id=12, name="Adventure")]

    @pytest.mark.asyncio
    async def test_empty_results_give_empty_list(self):
        gateway = self._gateway_with(
            discover_movies=TMDBDiscoverMovieResponse.model_validate({"results": []})
        )

        assert await gateway.fetch_random_movies(MovieFilterDTO()) == []
