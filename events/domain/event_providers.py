from django.db import models

class EventProviders(models.TextChoices):
    KRONOBOT = 'kronobot'
    KRONOLIVE = 'kronolive'
    OTHER = 'other'
