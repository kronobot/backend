from django.contrib import admin

from events.domain.event import Event
from events.domain.inscription import Inscription


class InscriptionAdmin(admin.ModelAdmin):
    list_display = ["event", "driver", "codriver", "car"]
    list_filter = ["event"]

admin.site.register(Inscription, InscriptionAdmin)
