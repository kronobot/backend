from inventory.domain.event import Event
from inventory.domain.repositories.event_criteria import EventCriteria
from inventory.domain.repositories.event_repository import EventRepository

from inventory.application.find_all_events.find_all_events_query import FindAllEventsQuery


class FindAllEventsQueryHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, query: FindAllEventsQuery) -> list[Event]:
        return self.event_repository.find_by_criteria(EventCriteria())
