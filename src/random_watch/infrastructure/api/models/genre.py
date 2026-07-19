from pydantic import BaseModel, Field


class GenreModel(BaseModel):
    """Response schema for a single genre entry."""

    id: int = Field(description="TMDB genre ID")
    name: str = Field(description="Genre name, e.g. 'Action'")


class GenreListResponseModel(BaseModel):
    """Envelope wrapping a list of genres."""

    genres: list[GenreModel] = Field(description="List of available genres")
