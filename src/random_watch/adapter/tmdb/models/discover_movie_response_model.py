from pydantic import BaseModel

from random_watch.adapter.tmdb.models.movie_model import TMDBMovieModel


class TMDBDiscoverMovieResponse(BaseModel):
    results: list[TMDBMovieModel]
