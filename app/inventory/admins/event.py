import traceback

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from unfold.decorators import action

from config.dashboard import build_activity_chart_context
from inventory.admins.event_stage import EventStageInline
from inventory.application.fetch_times_kronolive.fetch_times_kronolive_command import FetchTimesKronoliveCommand
from inventory.application.fetch_times_kronolive.fetch_times_kronolive_command_handler import (
    FetchTimesKronoliveCommandHandler,
)
from inventory.application.import_inscriptions_kronolive.import_inscriptions_kronolive_command import (
    ImportInscriptionsKronoliveCommand,
)
from inventory.application.import_inscriptions_kronolive.import_inscriptions_kronolive_command_handler import (
    ImportInscriptionsKronoliveCommandHandler,
)
from inventory.application.sync_event_stages_kronolive.sync_event_stages_kronolive_command import (
    SyncEventStagesKronoliveCommand,
)
from inventory.application.sync_event_stages_kronolive.sync_event_stages_kronolive_command_handler import (
    SyncEventStagesKronoliveCommandHandler,
)
from inventory.application.sync_events_kronolive.sync_events_kronolive_command import SyncEventsKronoliveCommand
from inventory.application.sync_events_kronolive.sync_events_kronolive_command_handler import (
    SyncEventsKronoliveCommandHandler,
)
from inventory.domain.event import Event
from inventory.domain.event_categories import EventCategories
from inventory.domain.stage_result import StageResult
from inventory.infrastructure.kronolive_events_gateway import KronoliveEventsGateway
from inventory.infrastructure.kronolive_hillclimb_events_gateway import KronoliveHillclimbEventsGateway
from inventory.infrastructure.repositories.db_car_repository import DbCarRepository
from inventory.infrastructure.repositories.db_competitor_repository import DbCompetitorRepository
from inventory.infrastructure.repositories.db_event_repository import DbEventRepository
from inventory.infrastructure.repositories.db_event_stage_repository import DbEventStageRepository
from inventory.infrastructure.repositories.db_inscription_repository import DbInscriptionRepository
from inventory.infrastructure.repositories.db_stage_result_repository import DbStageResultRepository
from inventory.infrastructure.repositories.db_team_repository import DbTeamRepository
from notification.infrastructure.repositories.db_event_timeline_item_repository import (
    DbEventTimelineItemRepository,
)
from notification.infrastructure.repositories.db_notification_task_repository import DbNotificationTaskRepository


class EventAdmin(ModelAdmin):
    list_display = ["name", "start_date", "end_date", "category"]
    list_filter = ["category"]
    search_fields = ["name"]
    ordering = ["start_date"]
    actions_detail = ["sync_stages", "sync_inscriptions", "sync_times"]
    actions_list = ["sync_current_year_events"]
    actions = ["sync_stages_bulk", "sync_inscriptions_bulk", "sync_times_bulk"]
    inlines = [EventStageInline]
    change_form_outer_before_template = "inventory/event_journey.html"

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def change_view(self, request: HttpRequest, object_id: str, form_url: str = "", extra_context=None):
        extra_context = extra_context or {}
        extra_context["stage_times_count"] = StageResult.objects.filter(inscription__event_id=object_id).count()
        chart_context = build_activity_chart_context()
        chart_context["chart_series"] = [s for s in chart_context["chart_series"] if s["label"] != "Events"]
        extra_context.update(chart_context)
        return super().change_view(request, object_id, form_url, extra_context)

    def _kronolive_gateway_for(self, event: Event) -> KronoliveEventsGateway:
        if event.category == EventCategories.HILL_CLIMB:
            return KronoliveHillclimbEventsGateway()
        return KronoliveEventsGateway()

    def _report_sync_exception(self, request: HttpRequest, action_label: str) -> None:
        messages.error(
            request,
            mark_safe(
                f"{action_label} failed due to an internal error.<pre class=\"whitespace-pre-wrap text-xs mt-2\">"
                f"{escape(traceback.format_exc())}</pre>"
            ),
        )

    def _sync_stages_for_event(self, event: Event) -> int:
        handler = SyncEventStagesKronoliveCommandHandler(
            kronolive_gateway=self._kronolive_gateway_for(event),
            event_repository=DbEventRepository(),
            event_stage_repository=DbEventStageRepository(),
            event_timeline_item_repository=DbEventTimelineItemRepository(),
        )
        return handler.handle(SyncEventStagesKronoliveCommand(event_id=event.id))

    def _sync_inscriptions_for_event(self, event: Event) -> int:
        handler = ImportInscriptionsKronoliveCommandHandler(
            kronolive_gateway=self._kronolive_gateway_for(event),
            event_repository=DbEventRepository(),
            team_repository=DbTeamRepository(),
            competitor_repository=DbCompetitorRepository(),
            car_repository=DbCarRepository(),
            inscription_repository=DbInscriptionRepository(),
            notification_task_repository=DbNotificationTaskRepository(),
        )
        return handler.handle(ImportInscriptionsKronoliveCommand(event_id=event.id))

    def _sync_times_for_event(self, event: Event) -> int:
        handler = FetchTimesKronoliveCommandHandler(
            kronolive_gateway=self._kronolive_gateway_for(event),
            event_repository=DbEventRepository(),
            inscription_repository=DbInscriptionRepository(),
            event_stage_repository=DbEventStageRepository(),
            stage_result_repository=DbStageResultRepository(),
            notification_task_repository=DbNotificationTaskRepository(),
            event_timeline_item_repository=DbEventTimelineItemRepository(),
        )
        return handler.handle(FetchTimesKronoliveCommand(event_id=event.id))

    def _run_bulk_sync(self, request: HttpRequest, queryset, sync_fn, action_label: str, item_label: str) -> None:
        total_synced = 0
        failed_count = 0
        for event in queryset:
            try:
                total_synced += sync_fn(event)
            except Exception:
                failed_count += 1
                self._report_sync_exception(request, f"{action_label} for '{event.name}'")

        succeeded_count = queryset.count() - failed_count
        if total_synced:
            messages.success(
                request, f"{total_synced} {item_label} synced successfully across {succeeded_count} event(s)."
            )
        elif not failed_count:
            messages.warning(request, f"Could not find any {item_label} to sync for the selected events.")

    def sync_stages_bulk(self, request: HttpRequest, queryset):
        self._run_bulk_sync(request, queryset, self._sync_stages_for_event, "Stages sync", "stages")

    sync_stages_bulk.short_description = "Sync stages"

    def sync_inscriptions_bulk(self, request: HttpRequest, queryset):
        self._run_bulk_sync(
            request, queryset, self._sync_inscriptions_for_event, "Inscriptions sync", "inscriptions"
        )

    sync_inscriptions_bulk.short_description = "Sync inscriptions"

    def sync_times_bulk(self, request: HttpRequest, queryset):
        self._run_bulk_sync(request, queryset, self._sync_times_for_event, "Times sync", "stage times")

    sync_times_bulk.short_description = "Sync times"

    @action(description="Sync current year events", icon="event_repeat", url_path="sync-current-year")
    def sync_current_year_events(self, request: HttpRequest):
        handler = SyncEventsKronoliveCommandHandler(
            kronolive_gateway=KronoliveEventsGateway(),
            event_repository=DbEventRepository(),
        )
        year = timezone.now().year
        try:
            synced_count = handler.handle(SyncEventsKronoliveCommand(year=year))
        except Exception:
            self._report_sync_exception(request, "Events sync")
        else:
            if synced_count == 0:
                messages.warning(request, f"Could not find any {year} events to sync in the external provider.")
            else:
                messages.success(request, f"{synced_count} events synced successfully for {year}.")

        return redirect(reverse_lazy("admin:inventory_event_changelist"))

    @action(description="Sync inscriptions", icon="how_to_reg", url_path="sync-inscriptions")
    def sync_inscriptions(self, request: HttpRequest, object_id: str):
        try:
            event = DbEventRepository().find_or_fail_by_id(object_id)
            synced_count = self._sync_inscriptions_for_event(event)
        except Exception:
            self._report_sync_exception(request, "Inscriptions sync")
        else:
            if synced_count == 0:
                messages.warning(request, "Could not find any inscriptions to sync in the external provider.")
            else:
                messages.success(request, f"{synced_count} inscriptions synced successfully.")

        return redirect(reverse_lazy("admin:inventory_event_change", args=(object_id,)))

    @action(description="View stage results", icon="table_chart", url_path="view-stage-results")
    def view_stage_results(self, request: HttpRequest, object_id: str):
        return redirect(
            f"{reverse_lazy('admin:inventory_stageresult_changelist')}?inscription__event__id__exact={object_id}"
        )

    @action(description="Sync stages", icon="route", url_path="sync-stages")
    def sync_stages(self, request: HttpRequest, object_id: str):
        try:
            event = DbEventRepository().find_or_fail_by_id(object_id)
            synced_count = self._sync_stages_for_event(event)
        except Exception:
            self._report_sync_exception(request, "Stages sync")
        else:
            if synced_count == 0:
                messages.warning(request, "Could not find any stages to sync in the external provider.")
            else:
                messages.success(request, f"{synced_count} stages synced successfully.")

        return redirect(reverse_lazy("admin:inventory_event_change", args=(object_id,)))

    @action(description="Sync times", icon="timer", url_path="sync-times")
    def sync_times(self, request: HttpRequest, object_id: str):
        try:
            event = DbEventRepository().find_or_fail_by_id(object_id)
            synced_count = self._sync_times_for_event(event)
        except Exception:
            self._report_sync_exception(request, "Times sync")
        else:
            if synced_count == 0:
                messages.warning(
                    request,
                    "Could not find any stage times to sync in the external provider. Make sure "
                    "inscriptions and stages have been synced for this event first.",
                )
            else:
                messages.success(request, f"{synced_count} stage times synced successfully.")

        return redirect(reverse_lazy("admin:inventory_event_change", args=(object_id,)))
