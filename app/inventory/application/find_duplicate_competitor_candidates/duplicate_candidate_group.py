from dataclasses import dataclass

from inventory.domain.competitor import Competitor


@dataclass(frozen=True)
class DuplicateCandidateGroup:
    competitors: list[Competitor]
    score: float
    match_reason: str
