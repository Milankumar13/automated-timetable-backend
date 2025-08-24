from django.db import models
from common.models import BaseModel

class AdminLog(BaseModel):
    """Minimal audit log for admin changes (what/where/who/when)."""
    table_name = models.CharField(max_length=128)   # e.g., 'catalog.Room' or 'scheduling.ClassPlan'
    row_id = models.BigIntegerField()               # PK of changed row (DB id)
    action = models.CharField(max_length=8, choices=[('INSERT','INSERT'),('UPDATE','UPDATE'),('DELETE','DELETE')])
    changed_by = models.CharField(max_length=255, null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)  # optional before/after diff
    def __str__(self): return f"{self.action} {self.table_name}#{self.row_id}"
