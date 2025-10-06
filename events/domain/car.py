from uuid import uuid4

from django.db import models
from django.db.models import ForeignKey

class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=150)
    group = models.CharField(max_length=150)
    competitor = ForeignKey('Competitor', related_name="cars", on_delete=models.PROTECT)
