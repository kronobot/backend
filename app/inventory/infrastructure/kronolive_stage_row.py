from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True)
class KronoliveStageRow:
    order: int
    loop: str
    loop_position: int
    name: str
    date: date
    time: time
    distance_km: float
    status: str
    finished_count: int
