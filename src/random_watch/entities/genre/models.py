from dataclasses import dataclass

from random_watch.entities.genre.value_objects import GenreId


@dataclass
class Genre:
    id: GenreId
    name: str
