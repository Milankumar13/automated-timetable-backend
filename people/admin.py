from django.contrib import admin

from .models import Enrollment, Instructor, Student


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("display_name", "email", "department", "tenant")
    list_filter = ("tenant", "department")
    search_fields = ("display_name", "email")
    autocomplete_fields = ("department",)


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    autocomplete_fields = ("offering",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("display_name", "email", "cohort", "department", "tenant")
    list_filter = ("tenant", "department", "cohort")
    search_fields = ("display_name", "email")
    autocomplete_fields = ("department",)
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "offering", "tenant")
    list_filter = ("tenant",)
    search_fields = ("student__display_name", "offering__course__code")
    autocomplete_fields = ("student", "offering")
