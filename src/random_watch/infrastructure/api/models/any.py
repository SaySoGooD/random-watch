from pydantic import BaseModel, Field

from random_watch.infrastructure.api.models.base import BaseSearchQuery
from random_watch.infrastructure.api.models.movie import MovieResponseModel
from random_watch.infrastructure.api.models.tv import TvResponseModel


class AnySearchQuery(BaseSearchQuery):
    """Query parameters for mixed movie/TV discovery."""

    count: int = Field(default=5, ge=1, le=20, description="Number of results to return (1–20)")


class RandomAnyItemModel(BaseModel):
    """A typed wrapper around a single movie or TV show result."""

    type: str = Field(description="Media type: 'movie' or 'tv'")
    item: MovieResponseModel | TvResponseModel = Field(description="The movie or TV show data")


class RandomAnyResponseModel(BaseModel):
    """Envelope wrapping a mixed collection of random results."""

    items: list[RandomAnyItemModel] = Field(description="List of randomly selected movies and TV shows")