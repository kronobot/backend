from django.contrib import admin
from django.utils.html import format_html

from events.domain.event import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date"]
    list_filter = ["name"]
    search_fields = ["name"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"

    image_tag.short_description = "Image preview"

admin.site.register(Event, EventAdmin)
