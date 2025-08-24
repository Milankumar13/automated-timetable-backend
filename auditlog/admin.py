from django.contrib import admin
from .models import AdminLog

# @admin.register(AdminLog)
# class AdminLogAdmin(admin.ModelAdmin):
#     pass
#     # list_display = ("action", "table_name", "row_id", "changed_by", "created_at")
#     # list_filter = ("action", "table_name", "created_at")
#     # search_fields = ("table_name", "changed_by")
