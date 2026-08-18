from django.core.files.base import ContentFile

from inventory.domain.repositories.event_criteria import EventCriteria
from inventory.domain.repositories.event_repository import EventRepository
from inventory.infrastructure.kronolive_events_gateway import KronoliveEventsGateway

from inventory.application.sync_events_kronolive.sync_events_kronolive_command import (
    SyncEventsKronoliveCommand,
)


class SyncEventsKronoliveCommandHandler:
    def __init__(
        self,
        kronolive_gateway: KronoliveEventsGateway,
        event_repository: EventRepository,
    ):
        self.kronolive_gateway = kronolive_gateway
        self.event_repository = event_repository

    def handle(self, command: SyncEventsKronoliveCommand) -> int:
        events = self.kronolive_gateway.get_events(command.year)

        for event in events:
            existing = self.event_repository.find_by_criteria(
                EventCriteria(provider_event_url=event.provider_event_url)
            )

            if existing:
                event_to_save = existing[0]
                event_to_save.name = event.name
                event_to_save.start_date = event.start_date
                event_to_save.end_date = event.end_date
                event_to_save.category = event.category
                event_to_save.provider = event.provider
                event_to_save.status = event.status
                event_to_save.provider_times_url = event.provider_times_url
                event_to_save.provider_inscriptions_url = event.provider_inscriptions_url
                event_to_save.provider_stages_url = event.provider_stages_url
            else:
                event_to_save = event

            if not event_to_save.image and event.poster_url:
                filename, content = self.kronolive_gateway.download_poster(event.poster_url)
                event_to_save.image.save(filename, ContentFile(content), save=False)

            self.event_repository.save(event_to_save)

        return len(events)
