from __future__ import annotations

import asyncio
from typing import Callable, Literal

from src.application.find_random_video.filter_dto.any_filter_dto import AnyFilterDTO
from src.application.find_random_video.filter_dto.base_filter_dto import base_filter_values
from src.application.find_random_video.filter_dto.filter_settings_dto import GenreDTO, RandomDTO
from src.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.find_random_video.result_dto.movie_dto import MovieDTO
from src.application.find_random_video.result_dto.tv_dto import TvDTO
from src.main.dependency_injection import container

FilterDTO = MovieFilterDTO | TvFilterDTO | AnyFilterDTO
ContentType = Literal["movie", "tv", "any"]


def create_filter_dto(content_type: ContentType, source: FilterDTO | None = None) -> FilterDTO:
    """Create a FilterDTO of *content_type*, copying shared fields from *source*."""
    shared = base_filter_values(source) if source else {}
    match content_type:
        case "movie":
            return MovieFilterDTO(**shared)
        case "tv":
            return TvFilterDTO(**shared)
        case "any":
            return AnyFilterDTO(**shared)


MOVIE_GENRES = [
    GenreDTO(28, "Action"),
    GenreDTO(12, "Adventure"),
    GenreDTO(16, "Animation"),
    GenreDTO(35, "Comedy"),
    GenreDTO(27, "Horror"),
]

TV_GENRES = [
    GenreDTO(10759, "Action & Adventure"),
    GenreDTO(16, "Animation"),
    GenreDTO(35, "Comedy"),
    GenreDTO(18, "Drama"),
    GenreDTO(10765, "Sci-Fi & Fantasy"),
]


def get_genres(content_type: ContentType) -> list[GenreDTO]:
    """Return deduplicated genre list for *content_type*."""
    match content_type:
        case "movie":
            return MOVIE_GENRES
        case "tv":
            return TV_GENRES
        case "any":
            seen: set[int] = set()
            result: list[GenreDTO] = []
            for genre in MOVIE_GENRES + TV_GENRES:
                if genre.id not in seen:
                    seen.add(genre.id)
                    result.append(genre)
            return result


# ---------------------------------------------------------------------------
# Result rendering
# ---------------------------------------------------------------------------


def _render_movie(movie: MovieDTO) -> None:
    print(f"\n{'─' * 40}")
    print(f"🎬  {movie.title}")
    if movie.original_title and movie.original_title != movie.title:
        print(f"    ({movie.original_title})")
    if movie.release_date:
        print(f"📅  {movie.release_date[:4]}")
    if movie.vote_average is not None:
        print(f"⭐  {movie.vote_average:.1f}  ({movie.vote_count} votes)")
    if movie.overview:
        print(f"\n{movie.overview[:300]}{'...' if len(movie.overview) > 300 else ''}")
    print(f"🔗  https://www.themoviedb.org/movie/{movie.id}")


def _render_tv(tv: TvDTO) -> None:
    print(f"\n{'─' * 40}")
    print(f"📺  {tv.name}")
    if tv.original_name and tv.original_name != tv.name:
        print(f"    ({tv.original_name})")
    if tv.first_air_date:
        print(f"📅  {tv.first_air_date[:4]}")
    if tv.vote_average is not None:
        print(f"⭐  {tv.vote_average:.1f}  ({tv.vote_count} votes)")
    if tv.overview:
        print(f"\n{tv.overview[:300]}{'...' if len(tv.overview) > 300 else ''}")
    print(f"🔗  https://www.themoviedb.org/tv/{tv.id}")


def render_results(results: list[MovieDTO | TvDTO]) -> None:
    """Pretty-print a list of movies and TV shows."""
    if not results:
        print("\nNo results found.")
        return
    print(f"\n{'=' * 40}")
    print(f"  Found {len(results)} result(s)")
    print(f"{'=' * 40}")
    for item in results:
        if isinstance(item, MovieDTO):
            _render_movie(item)
        else:
            _render_tv(item)
    print(f"\n{'─' * 40}")


# ---------------------------------------------------------------------------
# Generic console menu
# ---------------------------------------------------------------------------

MenuItem = tuple[str, Callable[[], None]]


class Menu:
    """
    Reusable interactive console menu.

    Responsibilities (SRP):
      - Render numbered items to stdout.
      - Read a single integer from stdin and dispatch to the matching action.
      - Loop until the user selects the implicit "Back / Exit" option.
    """

    def __init__(
        self,
        title: str,
        items: list[MenuItem],
        subtitle: Callable[[], str] | None = None,
    ) -> None:
        self._title = title
        self._items = items
        self._subtitle = subtitle

    def run(self) -> None:
        """Run the menu loop until the back/exit option is selected."""
        while True:
            self._render()
            choice = self._read_int()
            if choice == len(self._items) + 1:
                break
            if 1 <= choice <= len(self._items):
                self._items[choice - 1][1]()

    def _render(self) -> None:
        print(f"\n{'=' * 32}\n  {self._title}")
        if self._subtitle:
            print(f"  {self._subtitle()}")
        print("=" * 32)
        for i, (label, _) in enumerate(self._items, 1):
            print(f"{i}. {label}")
        print(f"{len(self._items) + 1}. Back\n")

    @staticmethod
    def _read_int() -> int:
        try:
            return int(input("> ").strip())
        except ValueError:
            return -1


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------


def _prompt_str(prompt: str) -> str:
    """Read a non-empty string from stdin."""
    return input(prompt).strip()


def _prompt_range(entity: str) -> tuple[float, float]:
    """Read a min/max float pair for *entity*."""
    return (
        float(input(f"Min {entity}: ")),
        float(input(f"Max {entity}: ")),
    )


# ---------------------------------------------------------------------------
# FilterMenu
# ---------------------------------------------------------------------------


class FilterMenu:
    """Interactive menu for configuring a FilterDTO."""

    def __init__(self, dto: FilterDTO, genres: list[GenreDTO]) -> None:
        self.dto = dto
        self.genres = genres
        self._include: list[GenreDTO] = []
        self._exclude: list[GenreDTO] = []

    def run(self) -> FilterDTO:
        """Run the filter menu and return the configured DTO."""
        self._build_main_menu().run()
        return self.dto

    def _build_main_menu(self) -> Menu:
        items: list[MenuItem] = [
            ("Content type (movie / tv / any)", self._content_type_menu),
            ("Genres", self._genre_menu),
            ("Reviews count", self._reviews_menu),
            ("Rating", self._rating_menu),
            ("Release year", self._year_menu),
            ("Popularity", self._popularity_menu),
            ("Runtime", self._runtime_menu),
            ("Language", self._language_menu),
            ("Countries", self._country_menu),
            ("Companies", self._company_menu),
            ("Keywords", self._keyword_menu),
            ("Certification", self._certification_menu),
            ("Sort", self._sort_menu),
            ("Random", self._random_menu),
            ("Show DTO", lambda: print(self.dto)),
        ]
        return Menu(
            "FILTER MENU",
            items,
            subtitle=lambda: f"Target: {self.dto.contentType}",
        )

    def _content_type_menu(self) -> None:
        def switch(ct: ContentType) -> None:
            self.dto = create_filter_dto(ct, self.dto)
            self.genres = get_genres(ct)
            self._sync_genres()

        Menu(
            "CONTENT TYPE",
            [
                ("Movie", lambda: switch("movie")),
                ("TV", lambda: switch("tv")),
                ("Any (movie+tv)", lambda: switch("any")),
            ],
        ).run()

    def _genre_menu(self) -> None:
        Menu(
            "GENRES",
            [
                ("Add include", lambda: self._pick_genre(self._include)),
                ("Add exclude", lambda: self._pick_genre(self._exclude)),
                ("Clear all", self._clear_genres),
            ],
        ).run()

    def _pick_genre(self, target: list[GenreDTO]) -> None:
        """Display genre list and append the chosen genre to *target*."""
        for i, genre in enumerate(self.genres, 1):
            print(f"{i}. {genre.name} ({genre.id})")
        try:
            idx = int(input("> ")) - 1
            if 0 <= idx < len(self.genres):
                genre = self.genres[idx]
                if genre.id not in {g.id for g in target}:
                    target.append(genre)
                    self._sync_genres()
        except ValueError:
            pass

    def _sync_genres(self) -> None:
        self.dto.with_genres = "|".join(str(g.id) for g in self._include) or None
        self.dto.without_genres = "|".join(str(g.id) for g in self._exclude) or None

    def _clear_genres(self) -> None:
        self._include.clear()
        self._exclude.clear()
        self._sync_genres()

    def _reviews_menu(self) -> None:
        try:
            value = int(input("Minimum reviews: "))
            self.dto.vote_count_gte = float(value)
        except ValueError:
            pass

    def _rating_menu(self) -> None:
        mn, mx = _prompt_range("rating")
        self.dto.vote_average_gte = mn
        self.dto.vote_average_lte = mx

    def _popularity_menu(self) -> None:
        mn, mx = _prompt_range("popularity")
        self.dto.popularity_gte = mn
        self.dto.popularity_lte = mx

    def _language_menu(self) -> None:
        value = _prompt_str("Language (en, ja, ko): ")
        if value:
            self.dto.with_original_language = value

    def _country_menu(self) -> None:
        value = _prompt_str("Country (US, JP): ")
        if value:
            self.dto.with_origin_country = value

    def _sort_menu(self) -> None:
        field = _prompt_str("Sort field: ")
        direction = _prompt_str("Direction (asc/desc): ")
        self.dto.sort_by = f"{field}.{direction}"

    def _random_menu(self) -> None:
        self.dto.random = RandomDTO(enabled=True, seed=None)

    def _year_menu(self) -> None:
        print("TODO: primary_release_date / air_date")

    def _runtime_menu(self) -> None:
        print("TODO: with_runtime")

    def _company_menu(self) -> None:
        print("TODO: with_companies")

    def _keyword_menu(self) -> None:
        print("TODO: with_keywords")

    def _certification_menu(self) -> None:
        print("TODO: certification")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------


class MainMenu:
    """Top-level application menu."""

    def __init__(self) -> None:
        self._dto: FilterDTO = create_filter_dto("any")
        self._movie_genres: list[GenreDTO] = []
        self._tv_genres: list[GenreDTO] = []

    def run(self) -> None:
        """Run the main menu loop."""
        self._load_genres()
        Menu(
            "RANDOM WATCH",
            [
                ("Configure filters", self._configure_filters),
                ("Find random collection (movie + tv)", self._find_collection),
                ("Find random movie", self._find_movie),
                ("Find random TV show", self._find_tv),
            ],
        ).run()

    def _load_genres(self) -> None:
        """Fetch genres from the API once on startup."""
        async def _fetch() -> tuple[list[GenreDTO], list[GenreDTO]]:
            async with container.tmdb_adapter() as adapter:
                return await asyncio.gather(
                    adapter.fetch_movie_genres(),
                    adapter.fetch_tv_genres(),
                )

        try:
            self._movie_genres, self._tv_genres = asyncio.run(_fetch())
        except Exception as e:
            print(f"\n[Warning] Could not load genres: {e}")

    def _get_genres(self, content_type: ContentType) -> list[GenreDTO]:
        """Return genres for the given content type."""
        match content_type:
            case "movie":
                return self._movie_genres
            case "tv":
                return self._tv_genres
            case "any":
                seen: set[int] = set()
                result: list[GenreDTO] = []
                for genre in self._movie_genres + self._tv_genres:
                    if genre.id not in seen:
                        seen.add(genre.id)
                        result.append(genre)
                return result

    def _configure_filters(self) -> None:
        content_type: ContentType = (
            self._dto.contentType if hasattr(self._dto, "contentType") else "any"
        )
        self._dto = FilterMenu(self._dto, self._get_genres(content_type)).run()

    def _find_collection(self) -> None:
        """Run GetRandomCollectionUseCase and display results."""
        try:
            use_case = container.get_random_collection_usecase()
            assert isinstance(self._dto, AnyFilterDTO)
            results = asyncio.run(use_case(self._dto, count=5))
            render_results(results)
        except Exception as e:
            print(f"\n[Error] {e}")

    def _find_movie(self) -> None:
        """Run GetRandomMovieUseCase and display result."""
        try:
            use_case = container.get_random_movie_usecase()
            dto = self._dto if isinstance(self._dto, MovieFilterDTO) else create_filter_dto("movie", self._dto)
            result = asyncio.run(use_case(dto))
            render_results([result] if result else [])
        except Exception as e:
            print(f"\n[Error] {e}")

    def _find_tv(self) -> None:
        """Run GetRandomTvUseCase and display result."""
        try:
            use_case = container.get_random_tv_usecase()
            dto = self._dto if isinstance(self._dto, TvFilterDTO) else create_filter_dto("tv", self._dto)
            result = asyncio.run(use_case(dto))
            render_results([result] if result else [])
        except Exception as e:
            print(f"\n[Error] {e}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    MainMenu().run()