from django.contrib import admin
from .models import RuleType, AdminRule

@admin.register(RuleType)
class RuleTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "created_at", "updated_at")
    search_fields = ("code", "name")

@admin.register(AdminRule)
class AdminRuleAdmin(admin.ModelAdmin):
    list_display = ("semester", "rule_type", "value_int", "is_active", "created_at")
    list_filter = ("semester", "rule_type", "is_active")
    search_fields = ("rule_type__code", "semester__code")
    autocomplete_fields = ("semester", "rule_type")
