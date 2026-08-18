from abc import ABC, abstractmethod
from uuid import UUID

from inventory.domain.event import Event
from inventory.domain.repositories.event_criteria import EventCriteria


class EventRepository(ABC):
    @abstractmethod
    def save(self, event: Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: EventCriteria) -> list[Event]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> Event:
        raise NotImplementedError
