from uuid import uuid4

from django.db import models

from inventory.domain.inscription_category import InscriptionCategory


class Inscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    event = models.ForeignKey("Event", related_name="inscriptions", on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=InscriptionCategory.choices)
    team = models.ForeignKey("Team", related_name="inscriptions", on_delete=models.CASCADE)
    driver = models.ForeignKey("Competitor", related_name="driver_inscriptions", on_delete=models.CASCADE)
    codriver = models.ForeignKey(
        "Competitor", related_name="codriver_inscriptions", on_delete=models.CASCADE, blank=True, null=True
    )
    car = models.ForeignKey("Car", related_name="inscriptions", on_delete=models.CASCADE)
    dorsal = models.CharField(max_length=10)
    total_seconds = models.FloatField(null=True, blank=True)
    total_rank = models.PositiveSmallIntegerField(null=True, blank=True)
    total_penalty_seconds = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.codriver:
            return f"{self.dorsal} - {self.driver.name} / {self.codriver.name}"
        return f"{self.dorsal} - {self.driver.name}"
