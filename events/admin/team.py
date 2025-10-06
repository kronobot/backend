from django.contrib import admin

from events.domain.event import Event
from events.domain.team import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(Team, TeamAdmin)
