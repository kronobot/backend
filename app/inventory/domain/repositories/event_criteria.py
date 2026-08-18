from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class EventCriteria:
    id: Optional[UUID] = None
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category: Optional[str] = None
    provider: Optional[str] = None
    status: Optional[bool] = None
    description: Optional[str] = None
    provider_inscriptions_url: Optional[str] = None
    provider_event_url: Optional[str] = None
    provider_times_url: Optional[str] = None
    start_date_gte: Optional[date] = None
    start_date_lte: Optional[date] = None
    end_date_lte: Optional[date] = None
