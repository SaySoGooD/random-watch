from dependency_injector import containers, providers

from random_watch.adapter.tmdb.tmdb_client import TMDBClient
from random_watch.adapter.tmdb.tmdb_gateway import TMDBGateway
from random_watch.application.find_random_video.interfaces.i_find_random_movie_usecase import \
    IGetRandomMovieUseCase
from random_watch.application.find_random_video.interfaces.i_find_random_tv_usecase import \
    IGetRandomTvUseCase
from random_watch.application.find_random_video.interfaces.i_find_random_usecase import \
    IGetRandomCollectionUseCase
from random_watch.application.find_random_video.usecases.find_random_movie_usecase import \
    GetRandomMovieUseCase
from random_watch.application.find_random_video.usecases.find_random_tv_usecase import \
    GetRandomTvUseCase
from random_watch.application.find_random_video.usecases.find_random_usecase import \
    GetRandomCollectionUseCase
from random_watch.infrastructure.config import Config


class Container(containers.DeclarativeContainer):
    """Application dependency injection container."""

    config: providers.Singleton[Config] = providers.Singleton(Config)

    tmdb_client: providers.Singleton[TMDBClient] = providers.Singleton(
        TMDBClient,
        api_key=config.provided.TMDB_ACCESS_TOKEN,
    )

    tmdb_gateway: providers.Singleton[TMDBGateway] = providers.Singleton(
        TMDBGateway,
        client=tmdb_client,
    )

    get_random_movie_usecase: providers.Factory[IGetRandomMovieUseCase] = (
        providers.Factory(
            GetRandomMovieUseCase,
            gateway=tmdb_gateway,
        )
    )

    get_random_tv_usecase: providers.Factory[IGetRandomTvUseCase] = providers.Factory(
        GetRandomTvUseCase,
        gateway=tmdb_gateway,
    )

    get_random_collection_usecase: providers.Factory[IGetRandomCollectionUseCase] = (
        providers.Factory(
            GetRandomCollectionUseCase,
            movie_gateway=tmdb_gateway,
            tv_gateway=tmdb_gateway,
        )
    )
