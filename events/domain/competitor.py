from uuid import uuid4

from django.db import models
from django.db.models import ForeignKey

class Competitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=256)
    team = ForeignKey('Team', related_name="competitors", on_delete=models.PROTECT)
