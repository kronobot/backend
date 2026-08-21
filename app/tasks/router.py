import logging
from datetime import date

from django.conf import settings
from django.http import HttpResponseForbidden
from ninja import Router

from inventory.application.fetch_times_kronolive.fetch_times_kronolive_command import FetchTimesKronoliveCommand
from inventory.application.fetch_times_kronolive.fetch_times_kronolive_command_handler import (
    FetchTimesKronoliveCommandHandler,
)
from inventory.application.find_close_events.find_close_events_query import FindCloseEventsQuery
from inventory.application.find_close_events.find_close_events_query_handler import FindCloseEventsQueryHandler
from inventory.application.import_inscriptions_kronolive.import_inscriptions_kronolive_command import (
    ImportInscriptionsKronoliveCommand,
)
from inventory.application.import_inscriptions_kronolive.import_inscriptions_kronolive_command_handler import (
    ImportInscriptionsKronoliveCommandHandler,
)
from inventory.application.sync_event_stages_kronolive.sync_event_stages_kronolive_command import (
    SyncEventStagesKronoliveCommand,
)
from inventory.application.sync_event_stages_kronolive.sync_event_stages_kronolive_command_handler import (
    SyncEventStagesKronoliveCommandHandler,
)
from inventory.application.sync_events_kronolive.sync_events_kronolive_command import SyncEventsKronoliveCommand
from inventory.application.sync_events_kronolive.sync_events_kronolive_command_handler import (
    SyncEventsKronoliveCommandHandler,
)
from inventory.domain.event import Event
from inventory.domain.event_categories import EventCategories
from inventory.infrastructure.kronolive_events_gateway import KronoliveEventsGateway
from inventory.infrastructure.kronolive_hillclimb_events_gateway import KronoliveHillclimbEventsGateway
from inventory.infrastructure.repositories.db_car_repository import DbCarRepository
from inventory.infrastructure.repositories.db_competitor_repository import DbCompetitorRepository
from inventory.infrastructure.repositories.db_event_repository import DbEventRepository
from inventory.infrastructure.repositories.db_event_stage_repository import DbEventStageRepository
from inventory.infrastructure.repositories.db_inscription_repository import DbInscriptionRepository
from inventory.infrastructure.repositories.db_stage_result_repository import DbStageResultRepository
from inventory.infrastructure.repositories.db_team_repository import DbTeamRepository
from notification.infrastructure.repositories.db_event_timeline_item_repository import (
    DbEventTimelineItemRepository,
)
from notification.infrastructure.repositories.db_notification_task_repository import DbNotificationTaskRepository

logger = logging.getLogger(__name__)

router = Router()


def _kronolive_gateway_for(event: Event) -> KronoliveEventsGateway:
    if event.category == EventCategories.HILL_CLIMB:
        return KronoliveHillclimbEventsGateway()
    return KronoliveEventsGateway()


def _find_close_events() -> list[Event]:
    handler = FindCloseEventsQueryHandler(event_repository=DbEventRepository())
    return handler.handle(FindCloseEventsQuery())


def _require_appengine_cron(request) -> HttpResponseForbidden | None:
    # App Engine's Cron Service is the only caller that can set this header;
    # App Engine strips it from any externally-originated request.
    if settings.DEBUG:
        return None
    if request.headers.get("X-Appengine-Cron") != "true":
        return HttpResponseForbidden()
    return None


@router.get("/providers/kronolive/import-this-year-events", response={202: None, 403: None})
def import_this_year_events(request):
    if forbidden := _require_appengine_cron(request):
        return forbidden

    handler = SyncEventsKronoliveCommandHandler(
        kronolive_gateway=KronoliveEventsGateway(),
        event_repository=DbEventRepository(),
    )
    handler.handle(SyncEventsKronoliveCommand(year=date.today().year))
    return 202, None


@router.get("/import-close-events-stages", response={202: None, 403: None})
def import_close_events_stages(request):
    if forbidden := _require_appengine_cron(request):
        return forbidden

    for event in _find_close_events():
        try:
            handler = SyncEventStagesKronoliveCommandHandler(
                kronolive_gateway=_kronolive_gateway_for(event),
                event_repository=DbEventRepository(),
                event_stage_repository=DbEventStageRepository(),
                event_timeline_item_repository=DbEventTimelineItemRepository(),
            )
            handler.handle(SyncEventStagesKronoliveCommand(event_id=event.id))
        except Exception:
            logger.exception("Failed to sync stages for event %s", event.id)

    return 202, None


@router.get("/import-close-events-inscriptions", response={202: None, 403: None})
def import_close_events_inscriptions(request):
    if forbidden := _require_appengine_cron(request):
        return forbidden

    for event in _find_close_events():
        try:
            handler = ImportInscriptionsKronoliveCommandHandler(
                kronolive_gateway=_kronolive_gateway_for(event),
                event_repository=DbEventRepository(),
                team_repository=DbTeamRepository(),
                competitor_repository=DbCompetitorRepository(),
                car_repository=DbCarRepository(),
                inscription_repository=DbInscriptionRepository(),
                notification_task_repository=DbNotificationTaskRepository(),
            )
            handler.handle(ImportInscriptionsKronoliveCommand(event_id=event.id))
        except Exception:
            logger.exception("Failed to import inscriptions for event %s", event.id)

    return 202, None


@router.get("/import-close-events-times", response={202: None, 403: None})
def import_close_events_times(request):
    if forbidden := _require_appengine_cron(request):
        return forbidden

    for event in _find_close_events():
        try:
            handler = FetchTimesKronoliveCommandHandler(
                kronolive_gateway=_kronolive_gateway_for(event),
                event_repository=DbEventRepository(),
                inscription_repository=DbInscriptionRepository(),
                event_stage_repository=DbEventStageRepository(),
                stage_result_repository=DbStageResultRepository(),
                notification_task_repository=DbNotificationTaskRepository(),
                event_timeline_item_repository=DbEventTimelineItemRepository(),
            )
            handler.handle(FetchTimesKronoliveCommand(event_id=event.id))
        except Exception:
            logger.exception("Failed to fetch times for event %s", event.id)

    return 202, None
