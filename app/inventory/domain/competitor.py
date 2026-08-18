from uuid import uuid4

from django.db import models
from django.db.models import ForeignKey


class Competitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=256)
    name_normalized = models.CharField(max_length=256, db_index=True)
    team = ForeignKey("Team", related_name="competitors", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.team.name})"
