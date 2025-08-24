from django.contrib import admin
from .models import Semester, Slot, ProfAvailability, RoomSlotBlock, ClassPlan, ClassSession

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "start_date", "end_date", "created_at", "updated_at")
    search_fields = ("code", "name")

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("semester", "dow", "start_time", "end_time", "is_official", "created_at")
    list_filter = ("semester", "dow", "is_official")
    search_fields = ("semester__code",)
    autocomplete_fields = ("semester",)

@admin.register(ProfAvailability)
class ProfAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("professor", "slot", "available", "note", "created_at")
    list_filter = ("available", "slot__semester", "slot__dow",)
    search_fields = ("professor__name", "slot__semester__code")
    autocomplete_fields = ("professor", "slot")

@admin.register(RoomSlotBlock)
class RoomSlotBlockAdmin(admin.ModelAdmin):
    list_display = ("room", "slot", "reason", "created_at")
    list_filter = ("room__building", "slot__semester", "slot__dow")
    search_fields = ("room__code", "room__building__code", "slot__semester__code")
    autocomplete_fields = ("room", "slot")

@admin.register(ClassPlan)
class ClassPlanAdmin(admin.ModelAdmin):
    list_display = ("department", "subject", "professor", "room", "slot", "status", "created_at")
    list_filter = ("status", "department", "slot__semester", "slot__dow")
    search_fields = ("subject__code", "subject__name", "professor__name", "room__code", "department__code")
    autocomplete_fields = ("department", "subject", "professor", "room", "slot")

@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ("day_date", "slot", "subject", "professor", "room", "status", "created_at")
    list_filter = ("status", "slot__semester", "slot__dow", "day_date")
    search_fields = ("subject__code", "subject__name", "professor__name", "room__code", "slot__semester__code")
    autocomplete_fields = ("plan", "semester", "slot", "subject", "professor", "room")
