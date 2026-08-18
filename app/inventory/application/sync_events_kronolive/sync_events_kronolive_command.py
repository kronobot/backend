from dataclasses import dataclass


@dataclass(frozen=True)
class SyncEventsKronoliveCommand:
    year: int
