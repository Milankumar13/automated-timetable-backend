from django.db import models
from django.core.validators import MinValueValidator
from common.models import BaseModel

class Professor(BaseModel):
    """Professors (admin-managed)."""
    department = models.ForeignKey('catalog.Department', on_delete=models.RESTRICT, related_name='professors')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    employee_no = models.CharField(max_length=64, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Optional policy knobs (useful for constraints)
    max_hours_per_week = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    max_classes_per_day = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])

    def __str__(self): return self.name
