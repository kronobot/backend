from uuid import uuid4

from django.db import models

from events.domain.event_categories import EventCategories


class Inscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    event = models.ForeignKey("Event", related_name='inscriptions', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=EventCategories.choices)
    team = models.ForeignKey("Team", related_name='inscriptions', on_delete=models.CASCADE)
    driver = models.ForeignKey("Competitor", related_name='driver_inscriptions', on_delete=models.CASCADE)
    codriver = models.ForeignKey("Competitor", related_name='codriver_inscriptions', on_delete=models.CASCADE, blank=True, null=True)
    car = models.ForeignKey("Car", related_name='inscriptions', on_delete=models.CASCADE)
    dorsal = models.CharField(max_length=10)
