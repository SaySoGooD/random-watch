from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from random_watch.application.find_random_video.filter_dto.any_filter_dto import AnyFilterDTO
from random_watch.application.find_random_video.filter_dto.movie_filter_dto import MovieFilterDTO
from random_watch.application.find_random_video.filter_dto.tv_filter_dto import TvFilterDTO
from random_watch.application.find_random_video.interfaces.i_find_random_movie_usecase import (
    IGetRandomMovieUseCase,
)
from random_watch.application.find_random_video.interfaces.i_find_random_tv_usecase import (
    IGetRandomTvUseCase,
)
from random_watch.application.find_random_video.interfaces.i_find_random_usecase import (
    IGetRandomCollectionUseCase,
)
from random_watch.application.find_random_video.interfaces.i_tmdb_api_adapter import (
    ITMDBAPIAdapter,
)
from random_watch.infrastructure.api.models.any import AnySearchQuery, RandomAnyItemModel, RandomAnyResponseModel
from random_watch.infrastructure.api.models.genre import GenreListResponseModel, GenreModel
from random_watch.infrastructure.api.models.movie import MovieResponseModel, MovieSearchQuery, RandomMovieResponseModel
from random_watch.infrastructure.api.models.tv import RandomTvResponseModel, TvResponseModel, TvSearchQuery
from random_watch.dependency_injection import Container

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
@inject
async def movie_genres(
    language: str | None = None,
    adapter: ITMDBAPIAdapter = Depends(Provide[Container.tmdb_adapter]),
) -> GenreListResponseModel:
    """Return all available movie genres."""
    genres = await adapter.fetch_movie_genres(language=language)
    return GenreListResponseModel(genres=[GenreModel(id=g.id, name=g.name) for g in genres])


@router.get("/genres/tv", response_model=GenreListResponseModel)
@inject
async def tv_genres(
    language: str | None = None,
    adapter: ITMDBAPIAdapter = Depends(Provide[Container.tmdb_adapter]),
) -> GenreListResponseModel:
    """Return all available TV show genres."""
    genres = await adapter.fetch_tv_genres(language=language)
    return GenreListResponseModel(genres=[GenreModel(id=g.id, name=g.name) for g in genres])


@router.post("/random/movie", response_model=RandomMovieResponseModel)
@inject
async def random_movie(
    query: MovieSearchQuery,
    usecase: IGetRandomMovieUseCase = Depends(Provide[Container.get_random_movie_usecase]),
) -> RandomMovieResponseModel:
    """Return a randomly selected movie matching the given filters."""
    movie = await usecase(MovieFilterDTO(**query.model_dump()))
    return RandomMovieResponseModel(movie=MovieResponseModel.model_validate(movie))


@router.post("/random/tv", response_model=RandomTvResponseModel)
@inject
async def random_tv(
    query: TvSearchQuery,
    usecase: IGetRandomTvUseCase = Depends(Provide[Container.get_random_tv_usecase]),
) -> RandomTvResponseModel:
    """Return a randomly selected TV show matching the given filters."""
    tv = await usecase(TvFilterDTO(**query.model_dump()))
    return RandomTvResponseModel(tv=TvResponseModel.model_validate(tv))


@router.post("/random/any", response_model=RandomAnyResponseModel)
@inject
async def random_any(
    query: AnySearchQuery,
    usecase: IGetRandomCollectionUseCase = Depends(
        Provide[Container.get_random_collection_usecase]
    ),
) -> RandomAnyResponseModel:
    """Return a mixed random collection of movies and TV shows matching the given filters."""
    items = await usecase(
        AnyFilterDTO(**query.model_dump(exclude={"count"})), count=query.count
    )
    return RandomAnyResponseModel(items=[_wrap_item(i) for i in items])
