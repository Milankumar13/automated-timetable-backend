from django.db import models
from common.models import BaseModel

class RuleType(BaseModel):
    """
    Lookup for admin rule types — seed once via admin or data migration.
    Examples: maxclassesperday, room_closed, term_limit, custom
    """
    code = models.CharField(max_length=64, unique=True)  # machine name
    name = models.CharField(max_length=128)              # human label
    description = models.TextField(null=True, blank=True)
    def __str__(self): return self.code

class AdminRule(BaseModel):
    """
    Concrete rule value for a semester.
    You can store numbers, text, or JSON — pick what fits each rule type.
    """
    semester = models.ForeignKey('scheduling.Semester', on_delete=models.CASCADE, related_name='admin_rules')
    rule_type = models.ForeignKey(RuleType, on_delete=models.PROTECT, related_name='rules')
    value_int = models.IntegerField(null=True, blank=True)
    value_text = models.TextField(null=True, blank=True)
    value_json = models.JSONField(default=dict, blank=True)
    note = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('semester', 'rule_type')]
    def __str__(self): return f"{self.semester.code}:{self.rule_type.code}"
