import aiohttp

from src.application.tmdb.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.tmdb.filter_dto.filter_settings_dto import (
    GenresDTO, RangeDTO, ReleaseDateDTO, RuntimeDTO,
    SortDTO, PaginationDTO, CompanyDTO, KeywordDTO, CertificationDTO,
)
from src.application.tmdb.api_dto.tmdb_movie_response_dto import (
    TMDBDiscoverMovieResponseDTO,
    TMDBMovieDTO,
)


class TMDBMovieAdapter:
    _BASE_URL = "https://api.themoviedb.org/3"
    _DISCOVER_PATH = "/discover/movie"
    _DEFAULT_SORT = "popularity.desc"
    _DEFAULT_PAGE = 1

    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        self._api_key = api_key
        self._session = session

    async def discover(self, filter_dto: MovieFilterDTO) -> TMDBDiscoverMovieResponseDTO:
        """Send discover request to TMDB and return mapped response."""
        params = self._build_params(filter_dto)

        async with self._session.get(
            url=f"{self._BASE_URL}{self._DISCOVER_PATH}",
            params=params,
        ) as response:
            response.raise_for_status()
            data = await response.json()

        return self._map_response(data)

    # --- Params ---

    def _build_params(self, dto: MovieFilterDTO) -> dict:
        raw = {
            "api_key": self._api_key,
            **self._base_params(dto),
            **self._genre_params(dto.genres),
            **self._release_date_params(dto.releaseDate),
            **self._range_params("vote_average", dto.rating),
            **self._range_params("vote_count", dto.votes),
            **self._range_params("popularity", dto.popularity),
            **self._runtime_params(dto.runtime),
            **self._companies_params(dto.companies),
            **self._keywords_params(dto.keywords),
            **self._certification_params(dto.certification),
            **self._sort_params(dto.sort),
            **self._pagination_params(dto.pagination),
        }
        return {k: v for k, v in raw.items() if v is not None}

    def _base_params(self, dto: MovieFilterDTO) -> dict:
        return {
            "language": dto.language,
            "region": dto.region,
            "include_adult": dto.adult,
            "include_video": dto.video,
            "with_original_language": self._join(dto.originalLanguage),
            "with_origin_country": self._join(dto.countries),
            "with_release_type": self._join(dto.releaseTypes, cast=str),
        }

    def _genre_params(self, genres: GenresDTO | None) -> dict:
        if not genres:
            return {}
        sep = "," if genres.logic == "and" else "|"
        return {
            "with_genres": self._join(genres.include, sep=sep),
            "without_genres": self._join(genres.exclude),
        }

    def _release_date_params(self, release: ReleaseDateDTO | None) -> dict:
        if not release:
            return {}
        return {
            "primary_release_date.gte": release.gte,
            "primary_release_date.lte": release.lte,
        }

    def _range_params(self, prefix: str, range_dto: RangeDTO | None) -> dict:
        if not range_dto:
            return {}
        return {
            f"{prefix}.gte": range_dto.min,
            f"{prefix}.lte": range_dto.max,
        }

    def _runtime_params(self, runtime: RuntimeDTO | None) -> dict:
        if not runtime:
            return {}
        return {
            "with_runtime.gte": runtime.min,
            "with_runtime.lte": runtime.max,
        }

    def _companies_params(self, companies: list[CompanyDTO] | None) -> dict:
        return {"with_companies": self._join(companies, key=lambda c: c.id)}

    def _keywords_params(self, keywords: list[KeywordDTO] | None) -> dict:
        return {"with_keywords": self._join(keywords, key=lambda k: k.id)}

    def _certification_params(self, cert: CertificationDTO | None) -> dict:
        if not cert:
            return {}
        return {
            "certification_country": cert.country,
            "certification": cert.value,
            "certification.gte": cert.gte,
            "certification.lte": cert.lte,
        }

    def _sort_params(self, sort: SortDTO | None) -> dict:
        return {"sort_by": sort.by if sort else self._DEFAULT_SORT}

    def _pagination_params(self, pagination: PaginationDTO | None) -> dict:
        return {"page": pagination.page if pagination else self._DEFAULT_PAGE}

    # --- Helpers ---

    @staticmethod
    def _join(
        items: list | None,
        sep: str = "|",
        key=None,
        cast=None,
    ) -> str | None:
        """
        Join a list into a TMDB-compatible string.

        Args:
            items: Source list.
            sep:   Separator, default "|".
            key:   Optional callable to extract value from each item.
            cast:  Optional type to cast each value before joining.
        """
        if not items:
            return None
        values = (key(i) if key else i for i in items)
        if cast:
            values = (cast(v) for v in values)
        return sep.join(str(v) for v in values)

    # --- Response mapper ---

    def _map_response(self, data: dict) -> TMDBDiscoverMovieResponseDTO:
        return TMDBDiscoverMovieResponseDTO(
            page=data["page"],
            total_pages=data["total_pages"],
            total_results=data["total_results"],
            results=[self._map_movie(m) for m in data["results"]],
        )

    def _map_movie(self, data: dict) -> TMDBMovieDTO:
        return TMDBMovieDTO(
            id=data["id"],
            title=data["title"],
            original_title=data["original_title"],
            overview=data["overview"],
            poster_path=data.get("poster_path"),
            backdrop_path=data.get("backdrop_path"),
            release_date=data.get("release_date", ""),
            vote_average=data["vote_average"],
            vote_count=data["vote_count"],
            popularity=data["popularity"],
            adult=data["adult"],
            genre_ids=data["genre_ids"],
            original_language=data["original_language"],
        )