from unfold.admin import ModelAdmin, StackedInline

from events.domain.car import Car
from events.domain.inscription import Inscription


class CarInline(StackedInline):
    model = Car
    extra = 0
    fields = ['brand', 'model', 'group']
    readonly_fields = ['brand', 'model', 'group']
    can_delete = False

class InscriptionInline(StackedInline):
    model = Inscription
    fk_name = 'driver'
    extra = 0
    fields = ['event_name', 'category', 'team_name', 'car_name', 'dorsal']
    readonly_fields = ['event_name', 'category', 'team_name', 'car_name', 'dorsal']
    can_delete = False

    def event_name(self, obj):
        return obj.event.name
    event_name.short_description = 'Event'

    def team_name(self, obj):
        return obj.team.name
    team_name.short_description = 'Team'

    def car_name(self, obj):
        return f"{obj.car.brand} {obj.car.model}"
    car_name.short_description = 'Car'

class CompetitorAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    inlines = [CarInline, InscriptionInline]
