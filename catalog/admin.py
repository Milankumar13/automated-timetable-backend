from django.contrib import admin
from .models import (
    Department, Building, Room, Feature, RoomFeature,
    Course, Subject, SubjectNeed
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "created_at", "updated_at")
    search_fields = ("code", "name")
    list_filter = ("is_active",)

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "created_at", "updated_at")
    search_fields = ("code", "name")
    list_filter = ("is_active",)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("building", "code", "name", "capacity", "is_active", "created_at")
    search_fields = ("code", "name", "building__code", "building__name")
    list_filter = ("is_active", "building")
    autocomplete_fields = ("building",)  # valid FK on Room

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "created_at", "updated_at")
    search_fields = ("code", "name")

@admin.register(RoomFeature)
class RoomFeatureAdmin(admin.ModelAdmin):
    list_display = ("room", "feature", "quantity", "created_at")
    list_filter = ("feature", "room__building")
    search_fields = ("room__code", "room__building__code", "feature__code")
    autocomplete_fields = ("room", "feature")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("department", "code", "name", "credits", "is_active", "created_at")
    search_fields = ("code", "name", "department__code", "department__name")
    list_filter = ("is_active", "department")
    autocomplete_fields = ("department",)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("course", "code", "name", "hours_per_week", "expected_size", "created_at")
    search_fields = ("code", "name", "course__code", "course__name")
    list_filter = ("course__department",)
    autocomplete_fields = ("course",)

# @admin.register(SubjectNeed)
# class SubjectNeedAdmin(admin.ModelAdmin):
#     list_display = ("subject", "feature", "quantity", "created_at")
#     list_filter = ("feature", "subject__course__department")
#     search_fields = ("subject__code", "subject__name", "feature__code")
#     autocomplete_fields = ("subject", "feature")
