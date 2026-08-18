import traceback
from uuid import UUID

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.html import escape
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from unfold.decorators import action

from inventory.application.find_duplicate_competitor_candidates.find_duplicate_competitor_candidates_query import (
    FindDuplicateCompetitorCandidatesQuery,
)
from inventory.application.find_duplicate_competitor_candidates.find_duplicate_competitor_candidates_query_handler import (
    FindDuplicateCompetitorCandidatesQueryHandler,
)
from inventory.application.merge_competitors.merge_competitors_command import MergeCompetitorsCommand
from inventory.application.merge_competitors.merge_competitors_command_handler import MergeCompetitorsCommandHandler
from inventory.infrastructure.repositories.db_car_repository import DbCarRepository
from inventory.infrastructure.repositories.db_competitor_repository import DbCompetitorRepository
from inventory.infrastructure.repositories.db_inscription_repository import DbInscriptionRepository


class CompetitorAdmin(ModelAdmin):
    list_display = ["name", "team"]
    list_filter = ["team"]
    search_fields = ["name"]
    actions_list = ["find_duplicates"]
    actions = ["merge_selected_competitors"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @action(description="Find duplicates", icon="content_copy", url_path="find-duplicates")
    def find_duplicates(self, request: HttpRequest):
        handler = FindDuplicateCompetitorCandidatesQueryHandler(competitor_repository=DbCompetitorRepository())
        groups = handler.handle(FindDuplicateCompetitorCandidatesQuery())

        context = dict(
            self.admin_site.each_context(request),
            title="Duplicate competitors",
            opts=self.model._meta,
            groups=groups,
        )
        return TemplateResponse(request, "inventory/competitor_duplicates.html", context)

    def merge_selected_competitors(self, request: HttpRequest, queryset):
        if queryset.count() != 2:
            messages.error(request, "Select exactly two competitors to merge.")
            return None

        competitors = list(queryset)

        if request.POST.get("post") == "yes":
            winner_id = request.POST.get("winner_id")
            valid_ids = {str(competitor.id) for competitor in competitors}

            if winner_id not in valid_ids:
                messages.error(request, "Select which competitor should survive the merge.")
                return None

            loser = next(competitor for competitor in competitors if str(competitor.id) != winner_id)
            winner = next(competitor for competitor in competitors if str(competitor.id) == winner_id)

            handler = MergeCompetitorsCommandHandler(
                competitor_repository=DbCompetitorRepository(),
                inscription_repository=DbInscriptionRepository(),
                car_repository=DbCarRepository(),
            )
            try:
                handler.handle(MergeCompetitorsCommand(winner_id=UUID(winner_id), loser_id=loser.id))
            except Exception:
                messages.error(
                    request,
                    mark_safe(
                        "Merge failed due to an internal error."
                        f"<pre class=\"whitespace-pre-wrap text-xs mt-2\">{escape(traceback.format_exc())}</pre>"
                    ),
                )
            else:
                messages.success(request, f'Merged "{loser.name}" into "{winner.name}".')

            return redirect(reverse_lazy("admin:inventory_competitor_changelist"))

        context = dict(
            self.admin_site.each_context(request),
            title="Merge competitors",
            opts=self.model._meta,
            competitors=competitors,
            action_checkbox_name="_selected_action",
        )
        return TemplateResponse(request, "inventory/competitor_merge_confirmation.html", context)

    merge_selected_competitors.short_description = "Merge selected competitors"
