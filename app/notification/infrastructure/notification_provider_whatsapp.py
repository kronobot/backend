from notification.domain.notification_context import NotificationContext
from notification.domain.notification_provider import NotificationProvider


class NotificationProviderWhatsapp(NotificationProvider):
    def notify(self, notification_context: NotificationContext) -> None:
        pass
