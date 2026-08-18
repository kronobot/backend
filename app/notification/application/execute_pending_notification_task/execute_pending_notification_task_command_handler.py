from django.utils import timezone

from notification.domain.notification_context import NotificationContext
from notification.domain.notification_provider_name import NotificationProviderName
from notification.domain.repositories.notification_task_criteria import NotificationTaskCriteria
from notification.domain.repositories.notification_task_repository import NotificationTaskRepository
from notification.infrastructure.notification_provider_debug import NotificationProviderDebug
from notification.infrastructure.notification_provider_telegram import NotificationProviderTelegram
from notification.infrastructure.notification_provider_whatsapp import NotificationProviderWhatsapp

from notification.application.execute_pending_notification_task.execute_pending_notification_task_command import (
    ExecutePendingNotificationTaskCommand,
)


class ExecutePendingNotificationTaskCommandHandler:
    def __init__(
        self,
        notification_task_repository: NotificationTaskRepository,
        notification_provider_debug: NotificationProviderDebug,
        notification_provider_whatsapp: NotificationProviderWhatsapp,
        notification_provider_telegram: NotificationProviderTelegram,
    ):
        self.notification_task_repository = notification_task_repository
        self.notification_providers_by_name = {
            NotificationProviderName.DEBUG: notification_provider_debug,
            NotificationProviderName.WHATSAPP: notification_provider_whatsapp,
            NotificationProviderName.TELEGRAM: notification_provider_telegram,
        }

    def handle(self, command: ExecutePendingNotificationTaskCommand) -> None:
        pending_tasks = self.notification_task_repository.find_by_criteria(
            NotificationTaskCriteria(delivered_at=None)
        )

        for task in pending_tasks:
            notification_provider = self.notification_providers_by_name.get(task.provider)
            if notification_provider is None:
                continue

            notification_context = NotificationContext(
                notification_task_name=task.name,
                event=task.event,
                payload=task.payload,
            )
            notification_provider.notify(notification_context)
            task.delivered_at = timezone.now()
            self.notification_task_repository.save(task)
