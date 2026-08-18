from datetime import date
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router

from api.schemas import EventOut, EventStageOut, InscriptionOut
from inventory.domain.event import Event
from inventory.domain.event_stage import EventStage
from inventory.domain.inscription import Inscription

router = Router()


@router.get("", response=list[EventOut])
def list_events(request, starts_at__gte: date | None = None, starts_at__lte: date | None = None):
    queryset = Event.objects.all()
    if starts_at__gte is not None:
        queryset = queryset.filter(start_date__gte=starts_at__gte)
    if starts_at__lte is not None:
        queryset = queryset.filter(start_date__lte=starts_at__lte)
    return queryset.order_by("start_date")


@router.get("/{event_id}/times", response=list[EventStageOut])
def list_event_times(request, event_id: UUID):
    get_object_or_404(Event, id=event_id)
    return EventStage.objects.filter(event_id=event_id).order_by("order")


@router.get("/{event_id}/inscriptions", response=list[InscriptionOut])
def list_event_inscriptions(request, event_id: UUID):
    get_object_or_404(Event, id=event_id)
    return Inscription.objects.filter(event_id=event_id).select_related("team", "driver", "codriver", "car")
