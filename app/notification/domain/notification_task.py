from uuid import uuid4

from django.db import models

from notification.domain.notification_provider_name import NotificationProviderName
from notification.domain.notification_task_name import NotificationTaskName


class NotificationTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    event = models.ForeignKey(
        "inventory.Event", related_name="notification_tasks", on_delete=models.CASCADE
    )
    provider = models.CharField(max_length=20, choices=NotificationProviderName.choices)
    name = models.CharField(max_length=50, choices=NotificationTaskName.choices)
    payload = models.JSONField(default=dict)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.provider} ({self.event})"
