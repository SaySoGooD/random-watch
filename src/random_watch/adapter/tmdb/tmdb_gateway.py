from random_watch.adapter.tmdb.models.genre_model import TMDBGenreModel
from random_watch.adapter.tmdb.models.movie_model import TMDBMovieModel
from random_watch.adapter.tmdb.models.tv_model import TMDBTvModel
from random_watch.adapter.tmdb.params import api_params
from random_watch.adapter.tmdb.tmdb_client import TMDBClient
from random_watch.application.find_random_video.filter_dto.movie_filter_dto import \
    MovieFilterDTO
from random_watch.application.find_random_video.filter_dto.tv_filter_dto import \
    TvFilterDTO
from random_watch.entities.genre import Genre
from random_watch.entities.movie import Movie
from random_watch.entities.tv import Tv


class TMDBGateway:
    """TMDB-backed implementation of the movie, TV and genre gateways.

    Converts application filter DTOs into TMDB query params and raw TMDB
    models back into application entities.
    """

    def __init__(self, client: TMDBClient) -> None:
        self._client = client

    async def fetch_random_movies(self, filter_dto: MovieFilterDTO) -> list[Movie]:
        """Return movies matching the given filter."""
        response = await self._client.discover_movies(api_params(filter_dto))
        return [self._to_movie(model) for model in response.results]

    async def fetch_random_tv(self, filter_dto: TvFilterDTO) -> list[Tv]:
        """Return TV shows matching the given filter."""
        response = await self._client.discover_tv(api_params(filter_dto))
        return [self._to_tv(model) for model in response.results]

    async def fetch_movie_genres(self, language: str | None = None) -> list[Genre]:
        """Return all available movie genres."""
        response = await self._client.movie_genres(language)
        return [self._to_genre(model) for model in response.genres]

    async def fetch_tv_genres(self, language: str | None = None) -> list[Genre]:
        """Return all available TV genres."""
        response = await self._client.tv_genres(language)
        return [self._to_genre(model) for model in response.genres]

    def _to_movie(self, model: TMDBMovieModel) -> Movie:
        return Movie(
            id=model.id,
            title=model.title,
            original_title=model.original_title,
            overview=model.overview,
            poster_path=model.poster_path,
            backdrop_path=model.backdrop_path,
            release_date=model.release_date,
            vote_average=model.vote_average,
            vote_count=model.vote_count,
            popularity=model.popularity,
            adult=model.adult,
            genre_ids=model.genre_ids,
            original_language=model.original_language,
        )

    def _to_tv(self, model: TMDBTvModel) -> Tv:
        return Tv(
            id=model.id,
            name=model.name,
            original_name=model.original_name,
            overview=model.overview,
            poster_path=model.poster_path,
            backdrop_path=model.backdrop_path,
            first_air_date=model.first_air_date,
            vote_average=model.vote_average,
            vote_count=model.vote_count,
            popularity=model.popularity,
            adult=model.adult,
            genre_ids=model.genre_ids,
            original_language=model.original_language,
            origin_country=model.origin_country,
        )

    def _to_genre(self, model: TMDBGenreModel) -> Genre:
        return Genre(
            id=model.id,
            name=model.name,
        )
