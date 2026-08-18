from django.contrib import admin
from django.db.models import Case, CharField, F, Func, Value, When
from django.db.models.functions import Concat, LPad
from unfold.admin import ModelAdmin


class InscriptionAdmin(ModelAdmin):
    list_display = ["dorsal_sort", "event", "driver", "codriver", "team"]
    list_filter = ["event", "category"]
    search_fields = ["dorsal"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        digits = Func(
            F("dorsal"),
            Value(r"\D"),
            Value(""),
            Value("g"),
            function="regexp_replace",
            output_field=CharField(),
        )
        sort_key = Concat(
            Case(
                When(dorsal__regex=r"\d", then=Value("0")),
                default=Value("1"),
                output_field=CharField(),
            ),
            LPad(digits, 10, Value("0")),
            F("dorsal"),
            output_field=CharField(),
        )
        return queryset.annotate(dorsal_sort_key=sort_key)

    @admin.display(description="Dorsal", ordering="dorsal_sort_key")
    def dorsal_sort(self, obj):
        return obj.dorsal
