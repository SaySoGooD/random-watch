from dependency_injector import containers, providers

from random_watch.adapter.tmdb.tmdb_api_adapter import TMDBAPIAdapter
from random_watch.adapter.tmdb.tmdb_presenter import TMDBPresenter
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
from random_watch.application.find_random_video.usecases.find_random_movie_usecase import (
    GetRandomMovieUseCase,
)
from random_watch.application.find_random_video.usecases.find_random_tv_usecase import (
    GetRandomTvUseCase,
)
from random_watch.application.find_random_video.usecases.find_random_usecase import (
    GetRandomCollectionUseCase,
)
from random_watch.infrastructure.config import Config


class Container(containers.DeclarativeContainer):
    """Application dependency injection container."""

    config: providers.Singleton[Config] = providers.Singleton(Config)

    tmdb_presenter: providers.Singleton[TMDBPresenter] = providers.Singleton(
        TMDBPresenter,
        api_key=config.provided.TMDB_ACCESS_TOKEN,
    )

    tmdb_adapter: providers.Singleton[ITMDBAPIAdapter] = providers.Singleton(
        TMDBAPIAdapter,
        presenter=tmdb_presenter,
    )

    get_random_movie_usecase: providers.Factory[IGetRandomMovieUseCase] = (
        providers.Factory(
            GetRandomMovieUseCase,
            adapter=tmdb_adapter,
        )
    )

    get_random_tv_usecase: providers.Factory[IGetRandomTvUseCase] = providers.Factory(
        GetRandomTvUseCase,
        adapter=tmdb_adapter,
    )

    get_random_collection_usecase: providers.Factory[IGetRandomCollectionUseCase] = (
        providers.Factory(
            GetRandomCollectionUseCase,
            adapter=tmdb_adapter,
        )
    )
