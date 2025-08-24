from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "email", "employee_no", "is_active", "created_at")
    search_fields = ("name", "email", "employee_no", "department__code", "department__name")
    list_filter = ("is_active", "department")
    autocomplete_fields = ("department",)
