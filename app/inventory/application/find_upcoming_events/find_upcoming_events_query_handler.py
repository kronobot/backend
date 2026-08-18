from datetime import date

from inventory.domain.event import Event
from inventory.domain.repositories.event_criteria import EventCriteria
from inventory.domain.repositories.event_repository import EventRepository

from inventory.application.find_upcoming_events.find_upcoming_events_query import FindUpcomingEventsQuery

UPCOMING_EVENTS_LIMIT = 6


class FindUpcomingEventsQueryHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, query: FindUpcomingEventsQuery) -> list[Event]:
        criteria = EventCriteria(start_date_gte=date.today())
        events = self.event_repository.find_by_criteria(criteria)
        return sorted(events, key=lambda e: e.start_date)[:UPCOMING_EVENTS_LIMIT]
