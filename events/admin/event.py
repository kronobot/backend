from django.contrib import admin

from events.domain.event import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date"]
    list_filter = ["name"]

admin.site.register(Event, EventAdmin)
