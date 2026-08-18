from django.db import models


class NotificationProviderName(models.TextChoices):
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    DEBUG = "debug"
