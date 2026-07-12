from pydantic import BaseModel


class TMDBDiscoverResponse(BaseModel):
    page: int
    total_pages: int
    total_results: int
