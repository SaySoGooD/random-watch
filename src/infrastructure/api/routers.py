from fastapi import APIRouter, HTTPException

from src.application.find_random_video.filter_dto.any_filter_dto import AnyFilterDTO
from src.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from src.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from src.infrastructure.api.models.any import AnySearchQuery, RandomAnyItemModel, RandomAnyResponseModel
from src.infrastructure.api.models.genre import GenreListResponseModel, GenreModel
from src.infrastructure.api.models.movie import MovieResponseModel, MovieSearchQuery, RandomMovieResponseModel
from src.infrastructure.api.models.tv import RandomTvResponseModel, TvResponseModel, TvSearchQuery
from src.main.dependency_injection import container

router = APIRouter()


def _wrap_item(item) -> RandomAnyItemModel:
    """Detect media type by duck-typing and wrap the item in a typed envelope."""
    is_movie = hasattr(item, "title")
    return RandomAnyItemModel(
        type="movie" if is_movie else "tv",
        item=MovieResponseModel.model_validate(item)
        if is_movie
        else TvResponseModel.model_validate(item),
    )


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe endpoint."""
    return {"status": "ok"}


@router.get("/genres/movie", response_model=GenreListResponseModel)
async def movie_genres(language: str | None = None) -> GenreListResponseModel:
    """Return all available movie genres."""
    genres = await container.tmdb_adapter().fetch_movie_genres(language=language)
    return GenreListResponseModel(genres=[GenreModel(id=g.id, name=g.name) for g in genres])


@router.get("/genres/tv", response_model=GenreListResponseModel)
async def tv_genres(language: str | None = None) -> GenreListResponseModel:
    """Return all available TV show genres."""
    genres = await container.tmdb_adapter().fetch_tv_genres(language=language)
    return GenreListResponseModel(genres=[GenreModel(id=g.id, name=g.name) for g in genres])


@router.post("/random/movie", response_model=RandomMovieResponseModel)
async def random_movie(query: MovieSearchQuery) -> RandomMovieResponseModel:
    """Return a randomly selected movie matching the given filters."""
    movie = await container.get_random_movie_usecase()(MovieFilterDTO(**query.model_dump()))
    if movie is None:
        raise HTTPException(status_code=404, detail="No movie found")
    return RandomMovieResponseModel(movie=MovieResponseModel.model_validate(movie))


@router.post("/random/tv", response_model=RandomTvResponseModel)
async def random_tv(query: TvSearchQuery) -> RandomTvResponseModel:
    """Return a randomly selected TV show matching the given filters."""
    tv = await container.get_random_tv_usecase()(TvFilterDTO(**query.model_dump()))
    if tv is None:
        raise HTTPException(status_code=404, detail="No TV show found")
    return RandomTvResponseModel(tv=TvResponseModel.model_validate(tv))


@router.post("/random/any", response_model=RandomAnyResponseModel)
async def random_any(query: AnySearchQuery) -> RandomAnyResponseModel:
    """Return a mixed random collection of movies and TV shows matching the given filters."""
    items = await container.get_random_collection_usecase()(
        AnyFilterDTO(**query.model_dump(exclude={"count"})), count=query.count
    )
    return RandomAnyResponseModel(items=[_wrap_item(i) for i in items])