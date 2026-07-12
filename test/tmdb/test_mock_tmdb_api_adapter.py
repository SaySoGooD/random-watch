from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientResponseError

from src.adapter.tmdb.tmdb_api_adapter import TMDBAPIAdapter
from src.application.find_random_video.filter_dto.filter_settings_dto import GenreDTO
from src.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.find_random_video.result_dto.movie_dto import MovieDTO
from src.application.find_random_video.result_dto.tv_dto import TvDTO

_ADAPTER_MODULE = "src.adapter.tmdb.tmdb_api_adapter"

_API_KEY = "test_api_key_abc"
_BASE_URL = "https://api.themoviedb.org/3"

_FAKE_FILTER_PARAMS: dict = {"sort_by": "popularity.desc", "page": "1"}

_MOVIE_PAYLOAD: dict = {
    "page": 1,
    "total_pages": 10,
    "total_results": 200,
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
    "page": 1,
    "total_pages": 5,
    "total_results": 80,
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
        {"id": 18, "name": "Drama"},
    ]
}


def _make_session(payload: dict) -> MagicMock:
    """Build a mock aiohttp.ClientSession whose GET returns *payload* as JSON."""
    response = AsyncMock()
    response.raise_for_status = AsyncMock()
    response.json = AsyncMock(return_value=payload)

    session = MagicMock()
    session.get.return_value.__aenter__ = AsyncMock(return_value=response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=False)

    return session


def _make_error_session(status: int) -> MagicMock:
    """Build a mock session whose GET triggers ClientResponseError via raise_for_status."""
    response = AsyncMock()

    response.raise_for_status = MagicMock(
        side_effect=ClientResponseError(
            request_info=MagicMock(),
            history=(),
            status=status,
        )
    )

    response.json = AsyncMock(return_value={})

    session = MagicMock()
    session.get.return_value.__aenter__ = AsyncMock(return_value=response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=False)

    return session


def _called_url(session: MagicMock) -> str:
    """Return the URL from the last session.get() call."""
    call = session.get.call_args

    if "url" in call.kwargs:
        return call.kwargs["url"]

    return call.args[0]


def _called_params(session: MagicMock) -> dict:
    """Return the params keyword argument from the last session.get() call."""
    return session.get.call_args.kwargs["params"]


class TestFetchRandomMovies:
    """Tests for the fetch_random_movies public method."""

    @pytest.fixture(autouse=True)
    def _patch_api_params(self):
        """Isolate adapter from FilterDTO internals by stubbing api_params."""
        with patch(f"{_ADAPTER_MODULE}.api_params", return_value=_FAKE_FILTER_PARAMS):
            yield

    @pytest.mark.asyncio
    async def test_returns_list_of_movie_dtos(self):
        """Response is mapped to a plain list of MovieDTO instances."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(_MOVIE_PAYLOAD))
        result = await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert isinstance(result, list)
        assert all(isinstance(item, MovieDTO) for item in result)

    @pytest.mark.asyncio
    async def test_results_contain_correct_movie_dtos(self):
        """Each item in the result list is a fully populated MovieDTO."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(_MOVIE_PAYLOAD))
        result = await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert len(result) == 1
        movie = result[0]

        assert movie.id == 101
        assert movie.title == "Inception"
        assert movie.original_title == "Inception"
        assert movie.overview == "A mind-bending thriller."
        assert movie.poster_path == "/inception.jpg"
        assert movie.backdrop_path == "/inception_bg.jpg"
        assert movie.release_date == "2010-07-16"
        assert movie.vote_average == 8.8
        assert movie.vote_count == 35_000
        assert movie.popularity == 120.5
        assert movie.adult is False
        assert movie.genre_ids == [28, 878]
        assert movie.original_language == "en"

    @pytest.mark.asyncio
    async def test_hits_discover_movie_endpoint(self):
        """Request targets the /discover/movie path."""
        session = _make_session(_MOVIE_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert _called_url(session) == f"{_BASE_URL}/discover/movie"

    @pytest.mark.asyncio
    async def test_api_key_injected_into_params(self):
        """api_key is always appended to the outgoing query params."""
        session = _make_session(_MOVIE_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert _called_params(session)["api_key"] == _API_KEY

    @pytest.mark.asyncio
    async def test_filter_dto_params_forwarded(self):
        """Params produced by api_params() are forwarded to the HTTP request."""
        session = _make_session(_MOVIE_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        params = _called_params(session)
        assert params["sort_by"] == _FAKE_FILTER_PARAMS["sort_by"]
        assert params["page"] == _FAKE_FILTER_PARAMS["page"]

    @pytest.mark.asyncio
    async def test_empty_results_list_mapped_correctly(self):
        """An empty results array in the response returns an empty list."""
        payload = {**_MOVIE_PAYLOAD, "results": [], "total_results": 0}
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(payload))
        result = await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert result == []

    @pytest.mark.asyncio
    async def test_multiple_movies_all_mapped(self):
        """All items in a multi-result response are mapped to MovieDTO instances."""
        second = {**_MOVIE_PAYLOAD["results"][0], "id": 999, "title": "Dune"}
        payload = {**_MOVIE_PAYLOAD, "results": [_MOVIE_PAYLOAD["results"][0], second]}

        adapter = TMDBAPIAdapter(_API_KEY, _make_session(payload))
        result = await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert len(result) == 2
        assert result[1].id == 999
        assert result[1].title == "Dune"


class TestFetchRandomTv:
    """Tests for the fetch_random_tv public method."""

    @pytest.fixture(autouse=True)
    def _patch_api_params(self):
        """Isolate adapter from FilterDTO internals by stubbing api_params."""
        with patch(f"{_ADAPTER_MODULE}.api_params", return_value=_FAKE_FILTER_PARAMS):
            yield

    @pytest.mark.asyncio
    async def test_returns_list_of_tv_dtos(self):
        """Response is mapped to a plain list of TvDTO instances."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(_TV_PAYLOAD))
        result = await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert isinstance(result, list)
        assert all(isinstance(item, TvDTO) for item in result)

    @pytest.mark.asyncio
    async def test_results_contain_correct_tv_dtos(self):
        """Each item in the result list is a fully populated TvDTO."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(_TV_PAYLOAD))
        result = await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert len(result) == 1
        show = result[0]

        assert show.id == 202
        assert show.name == "Breaking Bad"
        assert show.original_name == "Breaking Bad"
        assert show.overview == "A chemistry teacher turns to crime."
        assert show.poster_path == "/bb.jpg"
        assert show.backdrop_path == "/bb_bg.jpg"
        assert show.first_air_date == "2008-01-20"
        assert show.vote_average == 9.5
        assert show.vote_count == 12_000
        assert show.popularity == 200.0
        assert show.adult is False
        assert show.genre_ids == [18, 80]
        assert show.original_language == "en"
        assert show.origin_country == ["US"]

    @pytest.mark.asyncio
    async def test_hits_discover_tv_endpoint(self):
        """Request targets the /discover/tv path."""
        session = _make_session(_TV_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert _called_url(session) == f"{_BASE_URL}/discover/tv"

    @pytest.mark.asyncio
    async def test_api_key_injected_into_params(self):
        """api_key is always appended to the outgoing query params."""
        session = _make_session(_TV_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert _called_params(session)["api_key"] == _API_KEY

    @pytest.mark.asyncio
    async def test_empty_results_list_mapped_correctly(self):
        """An empty results array in the response returns an empty list."""
        payload = {**_TV_PAYLOAD, "results": [], "total_results": 0}
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(payload))
        result = await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert result == []


class TestFetchMovieGenres:
    """Tests for the fetch_movie_genres public method."""

    @pytest.mark.asyncio
    async def test_returns_list_of_genre_dtos(self):
        """Response is mapped to a plain list of GenreDTO instances."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(_GENRES_PAYLOAD))
        result = await adapter.fetch_movie_genres()

        assert isinstance(result, list)
        assert all(isinstance(item, GenreDTO) for item in result)

    @pytest.mark.asyncio
    async def test_all_genres_mapped(self):
        """All genres in the payload are present in the result."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(_GENRES_PAYLOAD))
        result = await adapter.fetch_movie_genres()

        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_genre_dto_fields_mapped_correctly(self):
        """Each GenreDTO carries the correct id and name from the API response."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(_GENRES_PAYLOAD))
        result = await adapter.fetch_movie_genres()

        first = result[0]
        assert first.id == 28
        assert first.name == "Action"

        last = result[2]
        assert last.id == 18
        assert last.name == "Drama"

    @pytest.mark.asyncio
    async def test_hits_genre_movie_list_endpoint(self):
        """Request targets the /genre/movie/list path."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_movie_genres()

        assert _called_url(session) == f"{_BASE_URL}/genre/movie/list"

    @pytest.mark.asyncio
    async def test_api_key_injected_into_params(self):
        """api_key is always appended to the outgoing query params."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_movie_genres()

        assert _called_params(session)["api_key"] == _API_KEY

    @pytest.mark.asyncio
    async def test_language_passed_when_provided(self):
        """An explicit language code is forwarded as a query param."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_movie_genres(language="de")

        assert _called_params(session).get("language") == "de"

    @pytest.mark.asyncio
    async def test_language_omitted_when_none(self):
        """language=None is stripped from query params before the request is dispatched."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_movie_genres(language=None)

        assert "language" not in _called_params(session)

    @pytest.mark.asyncio
    async def test_empty_genres_list_mapped_correctly(self):
        """An empty genres array in the response returns an empty list."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session({"genres": []}))
        result = await adapter.fetch_movie_genres()

        assert result == []


class TestFetchTvGenres:
    """Tests for the fetch_tv_genres public method."""

    @pytest.mark.asyncio
    async def test_returns_list_of_genre_dtos(self):
        """Response is mapped to a plain list of GenreDTO instances."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_session(_GENRES_PAYLOAD))
        result = await adapter.fetch_tv_genres()

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(item, GenreDTO) for item in result)

    @pytest.mark.asyncio
    async def test_hits_genre_tv_list_endpoint(self):
        """Request targets the /genre/tv/list path."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_tv_genres()

        assert _called_url(session) == f"{_BASE_URL}/genre/tv/list"

    @pytest.mark.asyncio
    async def test_api_key_injected_into_params(self):
        """api_key is always appended to the outgoing query params."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_tv_genres()

        assert _called_params(session)["api_key"] == _API_KEY

    @pytest.mark.asyncio
    async def test_language_passed_when_provided(self):
        """An explicit language code is forwarded as a query param."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_tv_genres(language="fr")

        assert _called_params(session).get("language") == "fr"

    @pytest.mark.asyncio
    async def test_language_omitted_when_none(self):
        """language=None is stripped from query params before the request is dispatched."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_tv_genres(language=None)

        assert "language" not in _called_params(session)


class TestMovieMappingEdgeCases:
    """Tests for optional-field defaults in movie mapping."""

    @pytest.fixture(autouse=True)
    def _patch_api_params(self):
        with patch(f"{_ADAPTER_MODULE}.api_params", return_value=_FAKE_FILTER_PARAMS):
            yield

    def _payload_without(self, *keys: str) -> dict:
        """Return _MOVIE_PAYLOAD with *keys* removed from the first result entry."""
        raw = {**_MOVIE_PAYLOAD["results"][0]}
        for key in keys:
            raw.pop(key, None)
        return {**_MOVIE_PAYLOAD, "results": [raw]}

    @pytest.mark.asyncio
    async def test_missing_poster_path_defaults_to_none(self):
        """poster_path is None when the key is absent in the API response."""
        adapter = TMDBAPIAdapter(
            _API_KEY, _make_session(self._payload_without("poster_path"))
        )
        result = await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert result[0].poster_path is None

    @pytest.mark.asyncio
    async def test_missing_backdrop_path_defaults_to_none(self):
        """backdrop_path is None when the key is absent in the API response."""
        adapter = TMDBAPIAdapter(
            _API_KEY, _make_session(self._payload_without("backdrop_path"))
        )
        result = await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert result[0].backdrop_path is None

    @pytest.mark.asyncio
    async def test_missing_release_date_defaults_to_empty_string(self):
        """release_date falls back to '' when the key is absent in the API response."""
        adapter = TMDBAPIAdapter(
            _API_KEY, _make_session(self._payload_without("release_date"))
        )
        result = await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert result[0].release_date is None

    @pytest.mark.asyncio
    async def test_null_poster_path_stored_as_none(self):
        """An explicit null poster_path from the API is stored as None."""
        raw = {**_MOVIE_PAYLOAD["results"][0], "poster_path": None}
        payload = {**_MOVIE_PAYLOAD, "results": [raw]}

        adapter = TMDBAPIAdapter(_API_KEY, _make_session(payload))
        result = await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))

        assert result[0].poster_path is None


class TestTvMappingEdgeCases:
    """Tests for optional-field defaults in TV mapping."""

    @pytest.fixture(autouse=True)
    def _patch_api_params(self):
        with patch(f"{_ADAPTER_MODULE}.api_params", return_value=_FAKE_FILTER_PARAMS):
            yield

    def _payload_without(self, *keys: str) -> dict:
        """Return _TV_PAYLOAD with *keys* removed from the first result entry."""
        raw = {**_TV_PAYLOAD["results"][0]}
        for key in keys:
            raw.pop(key, None)
        return {**_TV_PAYLOAD, "results": [raw]}

    @pytest.mark.asyncio
    async def test_missing_poster_path_defaults_to_none(self):
        """poster_path is None when the key is absent in the TV API response."""
        adapter = TMDBAPIAdapter(
            _API_KEY, _make_session(self._payload_without("poster_path"))
        )
        result = await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert result[0].poster_path is None

    @pytest.mark.asyncio
    async def test_missing_backdrop_path_defaults_to_none(self):
        """backdrop_path is None when the key is absent in the TV API response."""
        adapter = TMDBAPIAdapter(
            _API_KEY, _make_session(self._payload_without("backdrop_path"))
        )
        result = await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert result[0].backdrop_path is None

    @pytest.mark.asyncio
    async def test_missing_first_air_date_defaults_to_empty_string(self):
        """first_air_date falls back to '' when the key is absent in the TV API response."""
        adapter = TMDBAPIAdapter(
            _API_KEY, _make_session(self._payload_without("first_air_date"))
        )
        result = await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert result[0].first_air_date is None

    @pytest.mark.asyncio
    async def test_missing_origin_country_defaults_to_empty_list(self):
        """origin_country falls back to [] when the key is absent in the TV API response."""
        adapter = TMDBAPIAdapter(
            _API_KEY, _make_session(self._payload_without("origin_country"))
        )
        result = await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))

        assert result[0].origin_country == []


class TestHttpErrorPropagation:
    """Tests that ClientResponseError from raise_for_status() bubbles up correctly."""

    @pytest.fixture(autouse=True)
    def _patch_api_params(self):
        with patch(f"{_ADAPTER_MODULE}.api_params", return_value=_FAKE_FILTER_PARAMS):
            yield

    @pytest.mark.asyncio
    async def test_movie_request_raises_on_401(self):
        """Unauthorized API key (401) propagates as ClientResponseError."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_error_session(401))
        with pytest.raises(ClientResponseError) as exc_info:
            await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))
        assert exc_info.value.status == 401

    @pytest.mark.asyncio
    async def test_movie_request_raises_on_404(self):
        """Not found (404) propagates as ClientResponseError."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_error_session(404))
        with pytest.raises(ClientResponseError) as exc_info:
            await adapter.fetch_random_movies(MagicMock(spec=MovieFilterDTO))
        assert exc_info.value.status == 404

    @pytest.mark.asyncio
    async def test_tv_request_raises_on_500(self):
        """Internal server error (500) propagates as ClientResponseError."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_error_session(500))
        with pytest.raises(ClientResponseError) as exc_info:
            await adapter.fetch_random_tv(MagicMock(spec=TvFilterDTO))
        assert exc_info.value.status == 500

    @pytest.mark.asyncio
    async def test_genre_request_raises_on_429(self):
        """Rate limit exceeded (429) propagates as ClientResponseError."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_error_session(429))
        with pytest.raises(ClientResponseError) as exc_info:
            await adapter.fetch_movie_genres()
        assert exc_info.value.status == 429

    @pytest.mark.asyncio
    async def test_tv_genre_request_raises_on_503(self):
        """Service unavailable (503) propagates as ClientResponseError."""
        adapter = TMDBAPIAdapter(_API_KEY, _make_error_session(503))
        with pytest.raises(ClientResponseError) as exc_info:
            await adapter.fetch_tv_genres()
        assert exc_info.value.status == 503


class TestGetParamHandling:
    """Tests for None-value filtering and api_key injection inside _get."""

    @pytest.mark.asyncio
    async def test_none_values_stripped_from_params(self):
        """No None value should survive into the final query params dict."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_movie_genres(language=None)

        params = _called_params(session)
        assert all(v is not None for v in params.values())

    @pytest.mark.asyncio
    async def test_api_key_present_for_movie_genres(self):
        """api_key is injected for genre movie requests."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_movie_genres()

        assert _called_params(session)["api_key"] == _API_KEY

    @pytest.mark.asyncio
    async def test_api_key_present_for_tv_genres(self):
        """api_key is injected for genre TV requests."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_tv_genres()

        assert _called_params(session)["api_key"] == _API_KEY

    @pytest.mark.asyncio
    async def test_dict_params_merged_with_api_key(self):
        """When _get receives a plain dict, it is combined with api_key without calling api_params."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)
        await adapter.fetch_movie_genres(language="en")

        params = _called_params(session)
        assert params["language"] == "en"
        assert params["api_key"] == _API_KEY

    @pytest.mark.asyncio
    async def test_different_api_keys_forwarded_correctly(self):
        """The api_key supplied at construction time is the one sent in requests."""
        custom_key = "another_secret_key_xyz"
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(custom_key, session)
        await adapter.fetch_movie_genres()

        assert _called_params(session)["api_key"] == custom_key

    @pytest.mark.asyncio
    async def test_none_params_removed_but_existing_params_preserved(self):
        """None values are removed while valid params and api_key remain."""
        session = _make_session(_GENRES_PAYLOAD)
        adapter = TMDBAPIAdapter(_API_KEY, session)

        await adapter.fetch_movie_genres(language="de")

        params = _called_params(session)

        assert params == {
            "language": "de",
            "api_key": _API_KEY,
        }
