from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ImportInscriptionsKronoliveCommand:
    event_id: UUID
