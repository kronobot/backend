from datetime import date, timedelta

from inventory.domain.event import Event
from inventory.domain.repositories.event_criteria import EventCriteria
from inventory.domain.repositories.event_repository import EventRepository

from inventory.application.find_close_events.find_close_events_query import FindCloseEventsQuery

CLOSE_EVENTS_WINDOW_DAYS = 3


class FindCloseEventsQueryHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, query: FindCloseEventsQuery) -> list[Event]:
        today = date.today()
        window = timedelta(days=CLOSE_EVENTS_WINDOW_DAYS)

        criteria = EventCriteria(
            start_date_gte=today - window,
            end_date_lte=today + window,
        )
        return self.event_repository.find_by_criteria(criteria)
