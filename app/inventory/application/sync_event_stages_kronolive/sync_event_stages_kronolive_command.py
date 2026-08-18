from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SyncEventStagesKronoliveCommand:
    event_id: UUID
