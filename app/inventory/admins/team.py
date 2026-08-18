from unfold.admin import ModelAdmin


class TeamAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
