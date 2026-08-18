from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import action

from inventory.domain.event_stage import EventStage


class EventStageInline(TabularInline):
    model = EventStage
    template = "inventory/eventstage_tabular_inline.html"
    fields = ["order", "loop", "loop_position", "name", "date", "time", "distance_km", "status", "finished_count"]
    readonly_fields = fields
    ordering = ["order"]
    extra = 0
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class EventStageAdmin(ModelAdmin):
    list_display = ["event", "loop", "loop_position", "name", "date", "time", "distance_km", "status", "finished_count"]
    list_filter = ["status", "loop", "event"]
    ordering = ["event", "order"]
    actions_detail = ["view_stage_results"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @action(description="View stage results", icon="table_chart", url_path="view-stage-results")
    def view_stage_results(self, request: HttpRequest, object_id: str):
        return redirect(f"{reverse_lazy('admin:inventory_stageresult_changelist')}?event_stage__id__exact={object_id}")
