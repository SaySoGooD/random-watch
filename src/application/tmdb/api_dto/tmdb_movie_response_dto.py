# dto/tmdb_movie_response_dto.py
from dataclasses import dataclass


@dataclass
class TMDBMovieDTO:
    id: int
    title: str
    original_title: str
    overview: str
    poster_path: str | None
    backdrop_path: str | None
    release_date: str
    vote_average: float
    vote_count: int
    popularity: float
    adult: bool
    genre_ids: list[int]
    original_language: str


@dataclass
class TMDBDiscoverMovieResponseDTO:
    page: int
    total_pages: int
    total_results: int
    results: list[TMDBMovieDTO]