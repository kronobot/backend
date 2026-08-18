from uuid import UUID

from inventory.domain.event_stage import EventStage
from inventory.domain.exceptions.event_stage_not_found_exception import EventStageNotFoundException
from inventory.domain.repositories.event_stage_criteria import EventStageCriteria
from inventory.domain.repositories.event_stage_repository import EventStageRepository


class DbEventStageRepository(EventStageRepository):
    def save(self, event_stage: EventStage) -> None:
        event_stage.save()

    def find_by_criteria(self, criteria: EventStageCriteria) -> list[EventStage]:
        queryset = EventStage.objects.all()

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.event is not None:
            queryset = queryset.filter(event_id=criteria.event)
        if criteria.order is not None:
            queryset = queryset.filter(order=criteria.order)
        if criteria.loop is not None:
            queryset = queryset.filter(loop=criteria.loop)
        if criteria.loop_position is not None:
            queryset = queryset.filter(loop_position=criteria.loop_position)
        if criteria.status is not None:
            queryset = queryset.filter(status=criteria.status)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> EventStage:
        try:
            return EventStage.objects.get(id=id)
        except EventStage.DoesNotExist:
            raise EventStageNotFoundException(id)
