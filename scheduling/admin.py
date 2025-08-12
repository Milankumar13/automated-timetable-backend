from django.contrib import admin

from .models import Assignment, TimetableRun


@admin.register(TimetableRun)
class TimetableRunAdmin(admin.ModelAdmin):
    list_display = (
        "term",
        "status",
        "solver_name",
        "started_at",
        "finished_at",
        "runtime_ms",
        "soft_score",
    )
    list_filter = ("status", "term")
    date_hierarchy = "started_at"
    search_fields = ("solver_name",)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("run", "section", "prof", "room", "slot", "tenant")
    list_filter = ("run", "prof", "room", "slot", "tenant")
    search_fields = (
        "section__offering__course__code",
        "prof__display_name",
        "room__code",
    )
    autocomplete_fields = ("run", "section", "prof", "room", "slot")
