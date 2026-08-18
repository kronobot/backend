from dataclasses import dataclass


@dataclass(frozen=True)
class FindEventsByYearQuery:
    year: int
