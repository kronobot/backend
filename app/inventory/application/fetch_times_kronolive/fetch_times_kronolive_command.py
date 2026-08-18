from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class FetchTimesKronoliveCommand:
    event_id: UUID
