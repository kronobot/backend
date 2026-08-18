from inventory.domain.event import Event
from inventory.domain.event_stage import EventStage
from inventory.domain.inscription import Inscription
from inventory.domain.repositories.event_repository import EventRepository
from inventory.domain.repositories.event_stage_criteria import EventStageCriteria
from inventory.domain.repositories.event_stage_repository import EventStageRepository
from inventory.domain.repositories.inscription_criteria import InscriptionCriteria
from inventory.domain.repositories.inscription_repository import InscriptionRepository
from inventory.domain.repositories.stage_result_criteria import StageResultCriteria
from inventory.domain.repositories.stage_result_repository import StageResultRepository
from inventory.domain.stage_result import StageResult
from inventory.infrastructure.kronolive_events_gateway import KronoliveEventsGateway
from inventory.infrastructure.kronolive_time_row import KronoliveStageValue
from notification.domain.event_timeline_item import EventTimelineItem
from notification.domain.event_timeline_item_type import EventTimelineItemType
from notification.domain.notification_provider_name import NotificationProviderName
from notification.domain.notification_task import NotificationTask
from notification.domain.notification_task_name import NotificationTaskName
from notification.domain.repositories.event_timeline_item_repository import EventTimelineItemRepository
from notification.domain.repositories.notification_task_repository import NotificationTaskRepository

from inventory.application.fetch_times_kronolive.fetch_times_kronolive_command import (
    FetchTimesKronoliveCommand,
)


class FetchTimesKronoliveCommandHandler:
    def __init__(
        self,
        kronolive_gateway: KronoliveEventsGateway,
        event_repository: EventRepository,
        inscription_repository: InscriptionRepository,
        event_stage_repository: EventStageRepository,
        stage_result_repository: StageResultRepository,
        notification_task_repository: NotificationTaskRepository,
        event_timeline_item_repository: EventTimelineItemRepository,
    ):
        self.kronolive_gateway = kronolive_gateway
        self.event_repository = event_repository
        self.inscription_repository = inscription_repository
        self.event_stage_repository = event_stage_repository
        self.stage_result_repository = stage_result_repository
        self.notification_task_repository = notification_task_repository
        self.event_timeline_item_repository = event_timeline_item_repository

    def handle(self, command: FetchTimesKronoliveCommand) -> int:
        event = self.event_repository.find_or_fail_by_id(command.event_id)
        time_rows = self.kronolive_gateway.get_times(event.provider_times_url)

        synced_count = 0
        for row in time_rows:
            matches = self.inscription_repository.find_by_criteria(
                InscriptionCriteria(event=event.id, dorsal=row.dorsal)
            )
            if not matches:
                continue

            inscription = matches[0]
            inscription.total_seconds = row.total_seconds
            inscription.total_rank = row.total_rank
            inscription.total_penalty_seconds = row.total_penalty_seconds
            self.inscription_repository.save(inscription)

            for stage_value in row.stage_values:
                event_stage_matches = self.event_stage_repository.find_by_criteria(
                    EventStageCriteria(event=event.id, order=stage_value.stage_position)
                )
                if not event_stage_matches:
                    continue
                event_stage = event_stage_matches[0]

                existing = self.stage_result_repository.find_by_criteria(
                    StageResultCriteria(inscription=inscription.id, event_stage=event_stage.id)
                )
                is_new = not existing
                if existing:
                    stage_result = existing[0]
                    stage_result.value_seconds = stage_value.value_seconds
                    stage_result.rank = stage_value.rank
                else:
                    stage_result = StageResult(
                        inscription=inscription,
                        event_stage=event_stage,
                        value_seconds=stage_value.value_seconds,
                        rank=stage_value.rank,
                    )
                self.stage_result_repository.save(stage_result)
                synced_count += 1

                if is_new:
                    self._notify_stage_time_imported(event, inscription, event_stage, stage_result)
                    self._record_stage_finished(event, inscription, event_stage, stage_value)

        return synced_count

    def _notify_stage_time_imported(
        self, event: Event, inscription: Inscription, event_stage: EventStage, stage_result: StageResult
    ) -> None:
        notification_task = NotificationTask(
            event=event,
            provider=NotificationProviderName.DEBUG,
            name=NotificationTaskName.STAGE_TIME_IMPORTED,
            payload={
                "stage_result_id": str(stage_result.id),
                "dorsal": inscription.dorsal,
                "stage_order": event_stage.order,
            },
        )
        self.notification_task_repository.save(notification_task)

    def _record_stage_finished(
        self, event: Event, inscription: Inscription, event_stage: EventStage, stage_value: KronoliveStageValue
    ) -> None:
        timeline_item = EventTimelineItem(
            event=event,
            stage=event_stage,
            inscription=inscription,
            item_type=EventTimelineItemType.STAGE_FINISHED,
            context={"seconds": stage_value.value_seconds, "car_image": None},
        )
        self.event_timeline_item_repository.save(timeline_item)
