from uuid import uuid4

from django.db import models
from django.db.models import ForeignKey

from inventory.domain.event_stage_status import EventStageStatus


class EventStage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    event = ForeignKey("Event", related_name="stages", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    loop = models.CharField(max_length=5)
    loop_position = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=150)
    date = models.DateField()
    time = models.TimeField()
    distance_km = models.FloatField()
    status = models.CharField(max_length=20, choices=EventStageStatus.choices)
    finished_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("event", "order")]

    def __str__(self):
        return f"{self.loop}{self.loop_position} - {self.name}"
