from dataclasses import dataclass
from typing import Literal


@dataclass
class GenreDTO:
    id: int
    name: str


@dataclass
class CompanyDTO:
    id: int
    name: str


@dataclass
class KeywordDTO:
    id: int
    name: str


@dataclass
class NetworkDTO:
    id: int
    name: str


@dataclass
class RandomDTO:
    enabled: bool
    seed: int | None


@dataclass
class SortDTO:
    field: str
    direction: Literal["asc", "desc"]
