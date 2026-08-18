from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class NotificationTaskCriteria:
    id: Optional[UUID] = None
    event: Optional[UUID] = None
    provider: Optional[str] = None
    name: Optional[str] = None
    delivered_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
