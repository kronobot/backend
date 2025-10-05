from uuid import uuid4

from django.db import models

from events.domain.event_categories import EventCategories
from events.domain.event_providers import EventProviders


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.CharField(max_length=50, choices=EventCategories.choices)
    provider = models.CharField(max_length=50, choices=EventProviders.choices)
    status = models.BooleanField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='events', blank=True, null=True)

    provider_inscriptions_url = models.URLField(blank=True, null=True)
    provider_event_url = models.URLField(blank=True, null=True)
    provider_times_url = models.URLField(blank=True, null=True)
