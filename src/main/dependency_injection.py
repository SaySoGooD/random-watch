# src/main/dependency_injection.py

from dependency_injector import containers, providers

from src.adapter.tmdb.tmdb_api_adapter import TMDBAPIAdapter
from src.application.find_random_video.interfaces.i_find_random_movie_usecase import (
    IGetRandomMovieUseCase,
)
from src.application.find_random_video.interfaces.i_find_random_tv_usecase import (
    IGetRandomTvUseCase,
)
from src.application.find_random_video.interfaces.i_find_random_usecase import (
    IGetRandomCollectionUseCase,
)
from src.application.find_random_video.interfaces.i_tmdb_api_adapter import (
    ITMDBAPIAdapter,
)
from src.application.find_random_video.usecases.find_random_movie_usecase import (
    GetRandomMovieUseCase,
)
from src.application.find_random_video.usecases.find_random_tv_usecase import (
    GetRandomTvUseCase,
)
from src.application.find_random_video.usecases.find_random_usecase import (
    GetRandomCollectionUseCase,
)
from src.main.config import Config


class Container(containers.DeclarativeContainer):
    """Application dependency injection container."""

    config: providers.Singleton[Config] = providers.Singleton(Config)

    tmdb_adapter: providers.Singleton[ITMDBAPIAdapter] = providers.Singleton(
        TMDBAPIAdapter,
        api_key=config.provided.TMDB_ACCESS_TOKEN,
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


container = Container()
