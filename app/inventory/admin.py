from django.contrib import admin

from inventory.admins.car import CarAdmin
from inventory.admins.competitor import CompetitorAdmin
from inventory.admins.event import EventAdmin
from inventory.admins.event_stage import EventStageAdmin
from inventory.admins.inscription import InscriptionAdmin
from inventory.admins.stage_result import StageResultAdmin
from inventory.admins.team import TeamAdmin
from inventory.domain.car import Car
from inventory.domain.competitor import Competitor
from inventory.domain.event import Event
from inventory.domain.event_stage import EventStage
from inventory.domain.inscription import Inscription
from inventory.domain.stage_result import StageResult
from inventory.domain.team import Team

admin.site.register(Car, CarAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventStage, EventStageAdmin)
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(StageResult, StageResultAdmin)
admin.site.register(Team, TeamAdmin)
