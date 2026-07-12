from dataclasses import dataclass, field


@dataclass
class TvDTO:
    id: int
    name: str

    original_name: str | None = None
    overview: str | None = None

    poster_path: str | None = None
    backdrop_path: str | None = None
    first_air_date: str | None = None

    vote_average: float | None = None
    vote_count: int | None = None
    popularity: float | None = None
    adult: bool | None = None

    genre_ids: list[int] = field(default_factory=list)
    original_language: str | None = None
    origin_country: list[str] = field(default_factory=list)
