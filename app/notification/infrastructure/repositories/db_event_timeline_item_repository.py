from uuid import UUID

from notification.domain.event_timeline_item import EventTimelineItem
from notification.domain.exceptions.event_timeline_item_not_found_exception import (
    EventTimelineItemNotFoundException,
)
from notification.domain.repositories.event_timeline_item_criteria import EventTimelineItemCriteria
from notification.domain.repositories.event_timeline_item_repository import EventTimelineItemRepository


class DbEventTimelineItemRepository(EventTimelineItemRepository):
    def save(self, event_timeline_item: EventTimelineItem) -> None:
        event_timeline_item.save()

    def find_by_criteria(self, criteria: EventTimelineItemCriteria) -> list[EventTimelineItem]:
        queryset = EventTimelineItem.objects.select_related(
            "stage", "inscription", "inscription__driver", "inscription__codriver", "inscription__car"
        )

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.event is not None:
            queryset = queryset.filter(event_id=criteria.event)
        if criteria.stage is not None:
            queryset = queryset.filter(stage_id=criteria.stage)
        if criteria.inscription is not None:
            queryset = queryset.filter(inscription_id=criteria.inscription)
        if criteria.item_type is not None:
            queryset = queryset.filter(item_type=criteria.item_type)
        if criteria.created_at is not None:
            queryset = queryset.filter(created_at=criteria.created_at)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> EventTimelineItem:
        try:
            return EventTimelineItem.objects.get(id=id)
        except EventTimelineItem.DoesNotExist:
            raise EventTimelineItemNotFoundException(id)
