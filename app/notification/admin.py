from django.contrib import admin

from notification.admins.event_timeline_item import EventTimelineItemAdmin
from notification.admins.notification_task import NotificationTaskAdmin
from notification.domain.event_timeline_item import EventTimelineItem
from notification.domain.notification_task import NotificationTask

admin.site.register(NotificationTask, NotificationTaskAdmin)
admin.site.register(EventTimelineItem, EventTimelineItemAdmin)
