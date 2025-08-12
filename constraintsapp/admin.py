from django.contrib import admin

from .models import AdminRule, BlockedSlot, ProfessorAvailability, StudentPreference


@admin.register(AdminRule)
class AdminRuleAdmin(admin.ModelAdmin):
    list_display = ("rule_type", "tenant", "is_global", "room", "slot", "parameter")
    list_filter = ("tenant", "rule_type", "is_global")
    search_fields = ("rule_type",)
    autocomplete_fields = ("room", "slot")


@admin.register(BlockedSlot)
class BlockedSlotAdmin(admin.ModelAdmin):
    list_display = ("tenant", "room", "slot", "reason")
    list_filter = ("tenant", "room")
    search_fields = ("reason",)
    autocomplete_fields = ("room", "slot")


@admin.register(ProfessorAvailability)
class ProfessorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("tenant", "prof", "slot", "available")
    list_filter = ("tenant", "available")
    search_fields = ("prof__display_name",)
    autocomplete_fields = ("prof", "slot")


@admin.register(StudentPreference)
class StudentPreferenceAdmin(admin.ModelAdmin):
    list_display = ("tenant", "student", "course", "slot", "preference_score")
    list_filter = ("tenant",)
    search_fields = ("student__display_name", "course__code")
    autocomplete_fields = ("student", "course", "slot")
