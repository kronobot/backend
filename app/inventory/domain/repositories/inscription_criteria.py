from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class InscriptionCriteria:
    id: Optional[UUID] = None
    event: Optional[UUID] = None
    category: Optional[str] = None
    team: Optional[UUID] = None
    driver: Optional[UUID] = None
    codriver: Optional[UUID] = None
    car: Optional[UUID] = None
    dorsal: Optional[str] = None
    total_seconds: Optional[float] = None
    total_rank: Optional[int] = None
    total_penalty_seconds: Optional[float] = None
