from datetime import date

from inventory.domain.event import Event
from inventory.domain.repositories.event_criteria import EventCriteria
from inventory.domain.repositories.event_repository import EventRepository

from inventory.application.find_events_by_year.find_events_by_year_query import FindEventsByYearQuery


class FindEventsByYearQueryHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, query: FindEventsByYearQuery) -> list[Event]:
        criteria = EventCriteria(
            start_date_gte=date(query.year, 1, 1),
            start_date_lte=date(query.year, 12, 31),
        )
        events = self.event_repository.find_by_criteria(criteria)
        return sorted(events, key=lambda e: e.start_date)
