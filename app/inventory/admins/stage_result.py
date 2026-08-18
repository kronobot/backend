from unfold.admin import ModelAdmin


class StageResultAdmin(ModelAdmin):
    list_display = ["inscription", "event_stage", "value_seconds", "rank"]
    list_filter = ["event_stage", "inscription__event"]
    search_fields = ["inscription__dorsal"]
    list_select_related = [
        "inscription",
        "inscription__driver",
        "inscription__codriver",
        "inscription__event",
        "event_stage",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
