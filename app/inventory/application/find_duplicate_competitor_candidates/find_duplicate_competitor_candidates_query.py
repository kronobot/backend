from dataclasses import dataclass


@dataclass(frozen=True)
class FindDuplicateCompetitorCandidatesQuery:
    similarity_threshold: float = 0.85
