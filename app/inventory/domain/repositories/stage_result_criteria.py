from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class StageResultCriteria:
    id: Optional[UUID] = None
    inscription: Optional[UUID] = None
    event_stage: Optional[UUID] = None
    value_seconds: Optional[float] = None
    rank: Optional[int] = None
