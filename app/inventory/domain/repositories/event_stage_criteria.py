from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class EventStageCriteria:
    id: Optional[UUID] = None
    event: Optional[UUID] = None
    order: Optional[int] = None
    loop: Optional[str] = None
    loop_position: Optional[int] = None
    status: Optional[str] = None
