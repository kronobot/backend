from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class EventTimelineItemCriteria:
    id: Optional[UUID] = None
    event: Optional[UUID] = None
    stage: Optional[UUID] = None
    inscription: Optional[UUID] = None
    item_type: Optional[str] = None
    created_at: Optional[datetime] = None
