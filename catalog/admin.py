from django.contrib import admin

from .models import (
    Course,
    CourseOffering,
    Department,
    Room,
    Section,
    Tenant,
    Term,
    TimeSlot,
)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("code", "starts_on", "ends_on", "tenant")
    list_filter = ("tenant",)
    search_fields = ("code",)
    ordering = ("-starts_on",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "tenant")
    list_filter = ("tenant",)
    search_fields = ("code", "name")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("code", "capacity", "department", "is_active", "tenant")
    list_filter = ("tenant", "department", "is_active")
    search_fields = ("code",)
    autocomplete_fields = ("department",)
    ordering = ("code",)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("day", "start_time", "end_time", "is_official", "tenant", "label")
    list_filter = ("tenant", "day", "is_official")
    ordering = ("day", "start_time")
    search_fields = ("label", "start_time", "end_time")


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "department", "tenant")
    list_filter = ("tenant", "department")
    search_fields = ("code", "title")
    autocomplete_fields = ("department",)


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ("course", "term", "expected_enrollment", "tenant")
    list_filter = ("tenant", "term")
    search_fields = ("course__code", "course__title")
    autocomplete_fields = ("course", "term")
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "offering",
        "section_code",
        "meetings_per_week",
        "minutes_per_meeting",
        "tenant",
    )
    list_filter = ("tenant",)
    search_fields = ("offering__course__code", "section_code")
    autocomplete_fields = ("offering",)
