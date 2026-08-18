import re
from datetime import date

from django.http import Http404
from django.shortcuts import render

from inventory.domain.event_categories import EventCategories
from inventory.domain.event_stage_status import EventStageStatus
from inventory.domain.exceptions.event_not_found_exception import EventNotFoundException
from inventory.domain.repositories.event_stage_criteria import EventStageCriteria
from inventory.domain.repositories.inscription_criteria import InscriptionCriteria
from inventory.infrastructure.repositories.db_event_repository import DbEventRepository
from inventory.infrastructure.repositories.db_event_stage_repository import DbEventStageRepository
from inventory.infrastructure.repositories.db_inscription_repository import DbInscriptionRepository
from notification.domain.event_timeline_item_type import EventTimelineItemType
from notification.domain.repositories.event_timeline_item_criteria import EventTimelineItemCriteria
from notification.infrastructure.repositories.db_event_timeline_item_repository import (
    DbEventTimelineItemRepository,
)

from inventory.application.find_all_events.find_all_events_query import FindAllEventsQuery
from inventory.application.find_all_events.find_all_events_query_handler import FindAllEventsQueryHandler
from inventory.application.find_events_by_year.find_events_by_year_query import FindEventsByYearQuery
from inventory.application.find_events_by_year.find_events_by_year_query_handler import (
    FindEventsByYearQueryHandler,
)
from inventory.application.find_upcoming_events.find_upcoming_events_query import FindUpcomingEventsQuery
from inventory.application.find_upcoming_events.find_upcoming_events_query_handler import (
    FindUpcomingEventsQueryHandler,
)

CATEGORY_LABELS = {
    EventCategories.RALLY: "Rallyes",
    EventCategories.HILL_CLIMB: "Pujades",
    EventCategories.KARTING: "Karting",
    EventCategories.AUTOCROSS: "Autocross",
}

STAGE_STATUS_LABELS = {
    EventStageStatus.PENDING: "Pendiente",
    EventStageStatus.IN_PROGRESS: "En curso",
    EventStageStatus.FINISHED: "Finalizado",
}


def _attach_category_labels(events):
    for event in events:
        event.category_label = CATEGORY_LABELS.get(event.category, event.get_category_display())
    return events


def _group_by_category(events):
    rows = []
    for category, label in CATEGORY_LABELS.items():
        category_events = [event for event in events if event.category == category]
        if category_events:
            rows.append({"label": label, "events": category_events})
    return rows


def _dorsal_sort_key(inscription):
    match = re.match(r"^(\d+)", inscription.dorsal or "")
    return (0, int(match.group(1))) if match else (1, inscription.dorsal or "")


def _format_seconds(seconds):
    minutes, remainder = divmod(seconds, 60)
    return f"{int(minutes)}:{remainder:05.2f}"


def _inscription_display_name(inscription):
    if inscription.codriver:
        return f"{inscription.driver.name} / {inscription.codriver.name}"
    return inscription.driver.name


def _car_label(inscription):
    return f"{inscription.car.brand} {inscription.car.model}"


def _build_timeline_entries(timeline_items):
    entries = []
    for item in timeline_items:
        seconds = item.context.get("seconds")
        time_suffix = f" · {_format_seconds(seconds)}" if seconds is not None else ""

        if item.item_type == EventTimelineItemType.STAGE_COMPLETED:
            title = f"{item.stage.name} finalizado"
            subtitle = ""
        else:
            title = _inscription_display_name(item.inscription)
            subtitle = (
                f"Dorsal {item.inscription.dorsal} | {_car_label(item.inscription)} | "
                f"{item.stage.name}{time_suffix}"
            )

        entries.append({
            "type": item.item_type,
            "timestamp": item.created_at,
            "inscription_id": item.inscription_id,
            "title": title,
            "subtitle": subtitle,
            "car_image": item.context.get("car_image"),
        })
    return entries


def landing(request):
    today = date.today()
    event_repository = DbEventRepository()

    upcoming_events = _attach_category_labels(
        FindUpcomingEventsQueryHandler(event_repository).handle(FindUpcomingEventsQuery())
    )

    this_year_events = _attach_category_labels(
        FindEventsByYearQueryHandler(event_repository).handle(FindEventsByYearQuery(year=today.year))
    )
    category_rows = _group_by_category(this_year_events)

    all_events = FindAllEventsQueryHandler(event_repository).handle(FindAllEventsQuery())
    other_years = sorted({event.start_date.year for event in all_events} - {today.year}, reverse=True)

    return render(
        request,
        "webapp/landing.html",
        {
            "upcoming_events": upcoming_events,
            "category_rows": category_rows,
            "other_years": other_years,
        },
    )


def event_detail(request, event_id):
    event_repository = DbEventRepository()
    try:
        event = event_repository.find_or_fail_by_id(event_id)
    except EventNotFoundException:
        raise Http404

    inscription_repository = DbInscriptionRepository()
    inscriptions = inscription_repository.find_by_criteria(InscriptionCriteria(event=event_id))
    inscriptions = sorted(inscriptions, key=_dorsal_sort_key)

    event_stage_repository = DbEventStageRepository()
    stages = event_stage_repository.find_by_criteria(EventStageCriteria(event=event_id))
    stages = sorted(stages, key=lambda stage: stage.order)
    for stage in stages:
        stage.status_label = STAGE_STATUS_LABELS.get(stage.status, stage.get_status_display())

    timeline_repository = DbEventTimelineItemRepository()
    timeline_items = timeline_repository.find_by_criteria(EventTimelineItemCriteria(event=event_id))
    timeline_items = sorted(timeline_items, key=lambda item: item.created_at, reverse=True)
    timeline = _build_timeline_entries(timeline_items)

    return render(
        request,
        "webapp/event_detail.html",
        {
            "event": event,
            "category_label": CATEGORY_LABELS.get(event.category, event.get_category_display()),
            "inscriptions": inscriptions,
            "stages": stages,
            "timeline": timeline,
        },
    )


def year_archive(request, year):
    event_repository = DbEventRepository()
    events = _attach_category_labels(
        FindEventsByYearQueryHandler(event_repository).handle(FindEventsByYearQuery(year=year))
    )
    category_rows = _group_by_category(events)

    return render(
        request,
        "webapp/year_archive.html",
        {
            "year": year,
            "category_rows": category_rows,
        },
    )
