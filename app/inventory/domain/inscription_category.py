from django.db import models


class InscriptionCategory(models.TextChoices):
    REGULARITY = "regularity"
    REGULARITY_SPORT = "regularity_sport"
    SOLO = "solo"
    WITH_CODRIVER = "with_codriver"
    SINGLE_SPORT_REGULARITY = "single_sport_regularity"
    DRIFT = "drift"
