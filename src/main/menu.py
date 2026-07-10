from __future__ import annotations

from typing import Callable, Literal

from src.application.tmdb.filter_dto.any_filter_dto import AnyFilterDTO
from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.filter_dto.tv_filter_dto import TvFilterDTO
from src.application.tmdb.filter_dto.filter_settings_dto import (
    GenresDTO, GenreDTO, RangeDTO, SortDTO, RandomDTO,
)

FilterDTO = MovieFilterDTO | TvFilterDTO | AnyFilterDTO
ContentType = Literal["movie", "tv", "any"]

COMMON_FILTER_FIELDS = (
    "language", "region", "genres", "rating", "votes",
    "popularity", "runtime", "originalLanguage",
    "countries", "companies", "keywords", "adult",
    "sort", "random", "pagination",
)

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


# ---------------------------------------------------------------------------
# Domain helpers (unchanged logic, extracted to module level)
# ---------------------------------------------------------------------------

def create_filter_dto(
    content_type: ContentType,
    source: FilterDTO | None = None,
) -> FilterDTO:
    """Create a FilterDTO of *content_type*, copying common fields from *source*."""
    common: dict = {}
    if source is not None:
        common = {
            f: getattr(source, f)
            for f in COMMON_FILTER_FIELDS
            if hasattr(source, f)
        }
    match content_type:
        case "movie":
            return MovieFilterDTO(contentType="movie", **common)
        case "tv":
            return TvFilterDTO(contentType="tv", **common)
        case "any":
            return AnyFilterDTO(contentType="any", **common)


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
# Generic console menu  (SRP: owns loop + render only)
# ---------------------------------------------------------------------------

MenuItem = tuple[str, Callable[[], None]]


class Menu:
    """
    Reusable interactive console menu.

    Responsibilities (SRP):
      - Render numbered items to stdout.
      - Read a single integer from stdin and dispatch to the matching action.
      - Loop until the user selects the implicit "Back / Exit" option.

    Adding a new item never requires editing this class (OCP):
    callers simply extend the *items* list.
    """

    def __init__(
        self,
        title: str,
        items: list[MenuItem],
        subtitle: Callable[[], str] | None = None,
    ) -> None:
        self._title = title
        self._items = items
        self._subtitle = subtitle  # dynamic line shown under the title

    def run(self) -> None:
        """Run the menu loop until the back/exit option is selected."""
        while True:
            self._render()
            choice = self._read_int()
            if choice == len(self._items) + 1:
                break
            if 1 <= choice <= len(self._items):
                self._items[choice - 1][1]()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

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
# Input helpers  (DRY: one place for each repeated input pattern)
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
# FilterMenu  (SRP: owns DTO mutation only)
# ---------------------------------------------------------------------------

class FilterMenu:
    """
    Interactive menu for configuring a FilterDTO.

    Responsibilities (SRP):
      - Build the menu structure once.
      - Mutate self.dto in response to user choices.

    Adding a new filter option requires only appending to the items list
    inside _build_main_menu — run() is never touched (OCP).
    """

    def __init__(self, dto: FilterDTO, genres: list[GenreDTO]) -> None:
        self.dto = dto
        self.genres = genres

    def run(self) -> FilterDTO:
        """Run the filter menu and return the configured DTO."""
        self._build_main_menu().run()
        return self.dto

    # ------------------------------------------------------------------
    # Menu builders
    # ------------------------------------------------------------------

    def _build_main_menu(self) -> Menu:
        items: list[MenuItem] = [
            ("Content type (movie / tv / any)", self._content_type_menu),
            ("Genres",                          self._genre_menu),
            ("Reviews count",                  self._reviews_menu),
            ("Rating",                          self._rating_menu),
            ("Release year",                   self._year_menu),
            ("Popularity",                      self._popularity_menu),
            ("Runtime",                         self._runtime_menu),
            ("Language",                        self._language_menu),
            ("Countries",                       self._country_menu),
            ("Companies",                       self._company_menu),
            ("Keywords",                        self._keyword_menu),
            ("Certification",                   self._certification_menu),
            ("Sort",                            self._sort_menu),
            ("Random",                          self._random_menu),
            ("Show DTO",                        lambda: print(self.dto)),
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

        Menu("CONTENT TYPE", [
            ("Movie",          lambda: switch("movie")),
            ("TV",             lambda: switch("tv")),
            ("Any (movie+tv)", lambda: switch("any")),
        ]).run()

    def _genre_menu(self) -> None:
        if self.dto.genres is None:
            self.dto.genres = GenresDTO(include=[], exclude=[])

        Menu("GENRES", [
            ("Add include", lambda: self._pick_genre(self.dto.genres.include)),
            ("Add exclude", lambda: self._pick_genre(self.dto.genres.exclude)),
            ("Clear all",   self._clear_genres),
        ]).run()

    # ------------------------------------------------------------------
    # DTO mutators
    # ------------------------------------------------------------------

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
        except ValueError:
            pass

    def _clear_genres(self) -> None:
        self.dto.genres.include.clear()
        self.dto.genres.exclude.clear()

    def _reviews_menu(self) -> None:
        try:
            value = int(input("Minimum reviews: "))
            if self.dto.votes is None:
                self.dto.votes = RangeDTO(min=value, max=99_999_999)
            else:
                self.dto.votes.min = value
        except ValueError:
            pass

    def _rating_menu(self) -> None:
        mn, mx = _prompt_range("rating")        # DRY: shared helper
        self.dto.rating = RangeDTO(min=mn, max=mx)

    def _popularity_menu(self) -> None:
        mn, mx = _prompt_range("popularity")    # DRY: same helper
        self.dto.popularity = RangeDTO(min=mn, max=mx)

    def _language_menu(self) -> None:
        value = _prompt_str("Language (en, ja, ko): ")
        if value:
            self.dto.originalLanguage = [value]

    def _country_menu(self) -> None:
        value = _prompt_str("Country (US, JP): ")
        if value:
            self.dto.countries = [value]

    def _sort_menu(self) -> None:
        self.dto.sort = SortDTO(
            field=_prompt_str("Sort field: "),
            direction=_prompt_str("Direction (asc/desc): "),
        )

    def _random_menu(self) -> None:
        self.dto.random = RandomDTO(enabled=True, seed=None)

    # Stubs — not yet implemented
    def _year_menu(self)          -> None: print("TODO: ReleaseDateDTO")
    def _runtime_menu(self)       -> None: print("TODO: RuntimeDTO")
    def _company_menu(self)       -> None: print("TODO: CompanyDTO")
    def _keyword_menu(self)       -> None: print("TODO: KeywordDTO")
    def _certification_menu(self) -> None: print("TODO: CertificationDTO")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    dto = create_filter_dto("any")
    result = FilterMenu(dto, get_genres("any")).run()
    print(result)