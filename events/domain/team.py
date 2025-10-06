from uuid import uuid4

from django.db import models


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=50)
