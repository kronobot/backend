from django.contrib import admin
from unfold.admin import ModelAdmin

from events.domain.team import Team


class TeamAdmin(ModelAdmin):
    list_display = ["name"]

admin.site.register(Team, TeamAdmin)
