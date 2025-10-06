from django.contrib import admin

from events.admins.car import CarAdmin
from events.admins.competitor import CompetitorAdmin
from events.admins.event import EventAdmin
from events.admins.inscription import InscriptionAdmin
from events.admins.team import TeamAdmin
from events.domain.car import Car
from events.domain.competitor import Competitor
from events.domain.event import Event
from events.domain.inscription import Inscription
from events.domain.team import Team


admin.site.register(Car, CarAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(Team, TeamAdmin)
