from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class MergeCompetitorsCommand:
    winner_id: UUID
    loser_id: UUID
