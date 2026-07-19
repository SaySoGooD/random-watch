from pydantic import BaseModel

from random_watch.adapter.tmdb.models.tv_model import TMDBTvModel


class TMDBDiscoverTvResponse(BaseModel):
    results: list[TMDBTvModel]
