from django.db import models

class EventCategories(models.TextChoices):
    RALLY = 'rally'
    HILL_CLIMB = 'hill_climb'
    AUTOCROSS = 'autocross'
    KARTING = 'karting'
