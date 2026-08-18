from django.db import models


class EventStageStatus(models.TextChoices):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
