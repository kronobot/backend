from django.db import models


class NotificationTaskName(models.TextChoices):
    STAGE_TIME_IMPORTED = "stage_time_imported"
    EVENT_SYNCED = "event_synced"
    INSCRIPTIONS_IMPORTED = "inscriptions_imported"
