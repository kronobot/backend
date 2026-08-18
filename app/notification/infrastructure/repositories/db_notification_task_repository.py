from uuid import UUID

from notification.domain.notification_task import NotificationTask
from notification.domain.exceptions.notification_task_not_found_exception import (
    NotificationTaskNotFoundException,
)
from notification.domain.repositories.notification_task_criteria import NotificationTaskCriteria
from notification.domain.repositories.notification_task_repository import NotificationTaskRepository


class DbNotificationTaskRepository(NotificationTaskRepository):
    def save(self, notification_task: NotificationTask) -> None:
        notification_task.save()

    def find_by_criteria(self, criteria: NotificationTaskCriteria) -> list[NotificationTask]:
        queryset = NotificationTask.objects.all()

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.event is not None:
            queryset = queryset.filter(event_id=criteria.event)
        if criteria.provider is not None:
            queryset = queryset.filter(provider=criteria.provider)
        if criteria.name is not None:
            queryset = queryset.filter(name=criteria.name)
        if criteria.delivered_at is not None:
            queryset = queryset.filter(delivered_at=criteria.delivered_at)
        if criteria.created_at is not None:
            queryset = queryset.filter(created_at=criteria.created_at)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> NotificationTask:
        try:
            return NotificationTask.objects.get(id=id)
        except NotificationTask.DoesNotExist:
            raise NotificationTaskNotFoundException(id)
