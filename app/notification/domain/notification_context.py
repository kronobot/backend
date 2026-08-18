from dataclasses import dataclass

from inventory.domain.event import Event
from notification.domain.notification_task_name import NotificationTaskName


@dataclass(frozen=True)
class NotificationContext:
    notification_task_name: NotificationTaskName
    event: Event
    payload: dict
