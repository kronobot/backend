from uuid import uuid4

from django.db import models

from notification.domain.event_timeline_item_type import EventTimelineItemType


class EventTimelineItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    event = models.ForeignKey(
        "inventory.Event", related_name="timeline_items", on_delete=models.CASCADE
    )
    stage = models.ForeignKey(
        "inventory.EventStage", related_name="timeline_items", on_delete=models.CASCADE
    )
    inscription = models.ForeignKey(
        "inventory.Inscription",
        related_name="timeline_items",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    item_type = models.CharField(max_length=30, choices=EventTimelineItemType.choices)
    context = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_type} - {self.stage} ({self.event})"
