from pydantic import BaseModel


class TMDBGenreModel(BaseModel):
    id: int
    name: str


class TMDBGenreResponseModel(BaseModel):
    genres: list[TMDBGenreModel]
