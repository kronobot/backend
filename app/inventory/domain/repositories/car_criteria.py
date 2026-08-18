from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class CarCriteria:
    id: Optional[UUID] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    group: Optional[str] = None
    competitor: Optional[UUID] = None
