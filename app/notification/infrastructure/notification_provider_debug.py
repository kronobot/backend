import logging

from notification.domain.notification_context import NotificationContext
from notification.domain.notification_provider import NotificationProvider

logger = logging.getLogger(__name__)


class NotificationProviderDebug(NotificationProvider):
    def notify(self, notification_context: NotificationContext) -> None:
        logger.info(notification_context.payload)
