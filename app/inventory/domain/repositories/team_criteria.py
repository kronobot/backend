from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class TeamCriteria:
    id: Optional[UUID] = None
    name: Optional[str] = None
    name_normalized: Optional[str] = None
