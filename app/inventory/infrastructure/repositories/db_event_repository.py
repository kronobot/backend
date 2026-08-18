from uuid import UUID

from inventory.domain.event import Event
from inventory.domain.exceptions.event_not_found_exception import EventNotFoundException
from inventory.domain.repositories.event_criteria import EventCriteria
from inventory.domain.repositories.event_repository import EventRepository


class DbEventRepository(EventRepository):
    def save(self, event: Event) -> None:
        event.save()

    def find_by_criteria(self, criteria: EventCriteria) -> list[Event]:
        queryset = Event.objects.all()

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.name is not None:
            queryset = queryset.filter(name=criteria.name)
        if criteria.start_date is not None:
            queryset = queryset.filter(start_date=criteria.start_date)
        if criteria.end_date is not None:
            queryset = queryset.filter(end_date=criteria.end_date)
        if criteria.category is not None:
            queryset = queryset.filter(category=criteria.category)
        if criteria.provider is not None:
            queryset = queryset.filter(provider=criteria.provider)
        if criteria.status is not None:
            queryset = queryset.filter(status=criteria.status)
        if criteria.description is not None:
            queryset = queryset.filter(description=criteria.description)
        if criteria.provider_inscriptions_url is not None:
            queryset = queryset.filter(
                provider_inscriptions_url=criteria.provider_inscriptions_url
            )
        if criteria.provider_event_url is not None:
            queryset = queryset.filter(provider_event_url=criteria.provider_event_url)
        if criteria.provider_times_url is not None:
            queryset = queryset.filter(provider_times_url=criteria.provider_times_url)
        if criteria.start_date_gte is not None:
            queryset = queryset.filter(start_date__gte=criteria.start_date_gte)
        if criteria.start_date_lte is not None:
            queryset = queryset.filter(start_date__lte=criteria.start_date_lte)
        if criteria.end_date_lte is not None:
            queryset = queryset.filter(end_date__lte=criteria.end_date_lte)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> Event:
        try:
            return Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise EventNotFoundException(id)
