from inventory.domain.event import Event
from inventory.domain.event_stage import EventStage
from inventory.domain.event_stage_status import EventStageStatus
from inventory.domain.repositories.event_repository import EventRepository
from inventory.domain.repositories.event_stage_criteria import EventStageCriteria
from inventory.domain.repositories.event_stage_repository import EventStageRepository
from inventory.infrastructure.kronolive_events_gateway import KronoliveEventsGateway
from notification.domain.event_timeline_item import EventTimelineItem
from notification.domain.event_timeline_item_type import EventTimelineItemType
from notification.domain.repositories.event_timeline_item_repository import EventTimelineItemRepository

from inventory.application.sync_event_stages_kronolive.sync_event_stages_kronolive_command import (
    SyncEventStagesKronoliveCommand,
)


class SyncEventStagesKronoliveCommandHandler:
    def __init__(
        self,
        kronolive_gateway: KronoliveEventsGateway,
        event_repository: EventRepository,
        event_stage_repository: EventStageRepository,
        event_timeline_item_repository: EventTimelineItemRepository,
    ):
        self.kronolive_gateway = kronolive_gateway
        self.event_repository = event_repository
        self.event_stage_repository = event_stage_repository
        self.event_timeline_item_repository = event_timeline_item_repository

    def handle(self, command: SyncEventStagesKronoliveCommand) -> int:
        event = self.event_repository.find_or_fail_by_id(command.event_id)
        stage_rows = self.kronolive_gateway.get_stages(event.provider_stages_url)

        for row in stage_rows:
            existing = self.event_stage_repository.find_by_criteria(
                EventStageCriteria(event=event.id, order=row.order)
            )
            if existing:
                event_stage = existing[0]
                previous_status = event_stage.status
            else:
                event_stage = EventStage(event=event, order=row.order)
                previous_status = None

            event_stage.loop = row.loop
            event_stage.loop_position = row.loop_position
            event_stage.name = row.name
            event_stage.date = row.date
            event_stage.time = row.time
            event_stage.distance_km = row.distance_km
            event_stage.status = row.status
            event_stage.finished_count = row.finished_count
            self.event_stage_repository.save(event_stage)

            if event_stage.status == EventStageStatus.FINISHED and previous_status != EventStageStatus.FINISHED:
                self._record_stage_completed(event, event_stage)

        return len(stage_rows)

    def _record_stage_completed(self, event: Event, event_stage: EventStage) -> None:
        timeline_item = EventTimelineItem(
            event=event,
            stage=event_stage,
            item_type=EventTimelineItemType.STAGE_COMPLETED,
            context={},
        )
        self.event_timeline_item_repository.save(timeline_item)
