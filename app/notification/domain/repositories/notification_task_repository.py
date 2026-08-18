from abc import ABC, abstractmethod
from uuid import UUID

from notification.domain.notification_task import NotificationTask
from notification.domain.repositories.notification_task_criteria import NotificationTaskCriteria


class NotificationTaskRepository(ABC):
    @abstractmethod
    def save(self, notification_task: NotificationTask) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: NotificationTaskCriteria) -> list[NotificationTask]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> NotificationTask:
        raise NotImplementedError
