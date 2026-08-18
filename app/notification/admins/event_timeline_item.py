from unfold.admin import ModelAdmin


class EventTimelineItemAdmin(ModelAdmin):
    list_display = ["item_type", "event", "stage", "inscription", "created_at"]
    list_filter = ["item_type", "event"]
    list_select_related = ["event", "stage", "inscription"]
