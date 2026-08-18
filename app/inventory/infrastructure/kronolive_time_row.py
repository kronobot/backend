from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class KronoliveStageValue:
    stage_position: int
    value_seconds: float
    rank: Optional[int]


@dataclass(frozen=True)
class KronoliveTimeRow:
    dorsal: str
    stage_values: list[KronoliveStageValue]
    total_seconds: Optional[float]
    total_rank: Optional[int]
    total_penalty_seconds: Optional[float]
