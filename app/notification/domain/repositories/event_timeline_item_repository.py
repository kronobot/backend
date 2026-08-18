from abc import ABC, abstractmethod
from uuid import UUID

from notification.domain.event_timeline_item import EventTimelineItem
from notification.domain.repositories.event_timeline_item_criteria import EventTimelineItemCriteria


class EventTimelineItemRepository(ABC):
    @abstractmethod
    def save(self, event_timeline_item: EventTimelineItem) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: EventTimelineItemCriteria) -> list[EventTimelineItem]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> EventTimelineItem:
        raise NotImplementedError
