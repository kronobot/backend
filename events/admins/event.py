from django.utils.html import format_html
from unfold.admin import ModelAdmin


class EventAdmin(ModelAdmin):
    list_display = ["name", "start_date", "end_date"]
    list_filter = ["name"]
    search_fields = ["name"]

