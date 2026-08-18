from django.db import models


class EventTimelineItemType(models.TextChoices):
    STAGE_FINISHED = "stage_finished"
    ABANDONMENT = "abandonment"
    DID_NOT_START = "did_not_start"
    SCRATCH = "scratch"
    STAGE_COMPLETED = "stage_completed"
