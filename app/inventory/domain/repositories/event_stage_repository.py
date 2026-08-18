from abc import ABC, abstractmethod
from uuid import UUID

from inventory.domain.event_stage import EventStage
from inventory.domain.repositories.event_stage_criteria import EventStageCriteria


class EventStageRepository(ABC):
    @abstractmethod
    def save(self, event_stage: EventStage) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: EventStageCriteria) -> list[EventStage]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> EventStage:
        raise NotImplementedError
