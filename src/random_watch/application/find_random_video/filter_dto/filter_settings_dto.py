from dataclasses import dataclass


@dataclass
class RandomDTO:
    enabled: bool
    seed: int | None
