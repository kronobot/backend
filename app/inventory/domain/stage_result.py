from uuid import uuid4

from django.db import models
from django.db.models import ForeignKey


class StageResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    inscription = ForeignKey("Inscription", related_name="stage_results", on_delete=models.CASCADE)
    event_stage = ForeignKey("EventStage", related_name="stage_results", on_delete=models.CASCADE)
    value_seconds = models.FloatField()
    rank = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("inscription", "event_stage")]

    def __str__(self):
        return f"{self.inscription} - {self.event_stage}: {self.value_seconds}s"
