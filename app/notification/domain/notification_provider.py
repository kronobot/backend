from abc import ABC, abstractmethod

from notification.domain.notification_context import NotificationContext


class NotificationProvider(ABC):
    @abstractmethod
    def notify(self, notification_context: NotificationContext) -> None:
        raise NotImplementedError
