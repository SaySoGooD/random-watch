from dataclasses import dataclass, field

from random_watch.entities.genre.value_objects import GenreId
from random_watch.entities.movie.value_objects import MovieId


@dataclass
class Movie:
    id: MovieId
    title: str

    original_title: str | None = None
    overview: str | None = None

    poster_path: str | None = None
    backdrop_path: str | None = None
    release_date: str | None = None

    vote_average: float | None = None
    vote_count: int | None = None
    popularity: float | None = None
    adult: bool | None = None

    genre_ids: list[GenreId] = field(default_factory=list)
    original_language: str | None = None
