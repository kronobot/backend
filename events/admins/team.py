from unfold.admin import ModelAdmin


class TeamAdmin(ModelAdmin):
    list_display = ["name"]
