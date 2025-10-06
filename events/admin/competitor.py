from django.contrib import admin

from events.domain.car import Car
from events.domain.competitor import Competitor


class CarInline(admin.TabularInline):
    model = Car
    extra = 0
    fields = ['brand', 'model', 'group']


class CompetitorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    inlines = [CarInline]

admin.site.register(Competitor, CompetitorAdmin)
