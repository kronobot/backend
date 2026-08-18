from collections import Counter
from datetime import timedelta

from django.utils import timezone

from inventory.domain.event import Event
from inventory.domain.event_stage import EventStage
from inventory.domain.inscription import Inscription
from inventory.domain.stage_result import StageResult

BUCKET_MINUTES = 1
BUCKET_SECONDS = BUCKET_MINUTES * 60
WINDOW_DAYS = 14

SERIES = [
    ("Events", Event, "#2a78d6", "#3987e5"),
    ("Inscriptions", Inscription, "#eb6834", "#d95926"),
    ("Stages", EventStage, "#1baf7a", "#199e70"),
    ("Times", StageResult, "#eda100", "#c98500"),
]

RANGES = [
    ("1h", 60, "Last hour"),
    ("3h", 3 * 60, "3 hours"),
    ("6h", 6 * 60, "6 hours"),
    ("12h", 12 * 60, "12 hours"),
    ("24h", 24 * 60, "24 hours"),
    ("3d", 3 * 24 * 60, "3 days"),
    ("7d", 7 * 24 * 60, "7 days"),
    ("14d", 14 * 24 * 60, "14 days"),
]


def _sparse_bucket_counts(model, window_start, bucket_count):
    timestamps = model.objects.filter(created_at__gte=window_start).values_list("created_at", flat=True)
    counter = Counter()
    for created_at in timestamps:
        offset_seconds = (created_at - window_start).total_seconds()
        bucket_index = int(offset_seconds // BUCKET_SECONDS)
        if 0 <= bucket_index < bucket_count:
            counter[bucket_index] += 1
    return sorted(counter.items())


def build_activity_chart_context() -> dict:
    now = timezone.now()
    aligned_now = now.replace(second=0, microsecond=0)
    window_start = aligned_now - timedelta(days=WINDOW_DAYS)
    bucket_count = int((aligned_now - window_start).total_seconds() // BUCKET_SECONDS) + 1

    return {
        "chart_window_start_ms": int(window_start.timestamp() * 1000),
        "chart_bucket_minutes": BUCKET_MINUTES,
        "chart_bucket_count": bucket_count,
        "chart_series": [
            {
                "label": label,
                "colorLight": color_light,
                "colorDark": color_dark,
                "buckets": _sparse_bucket_counts(model, window_start, bucket_count),
            }
            for label, model, color_light, color_dark in SERIES
        ],
        "chart_ranges": [(key, display_label, minutes) for key, minutes, display_label in RANGES],
    }


def dashboard_callback(request, context: dict) -> dict:
    context.update(build_activity_chart_context())
    return context
