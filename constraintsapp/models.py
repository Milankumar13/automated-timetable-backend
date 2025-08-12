import uuid

from django.db import models

from catalog.models import Course, Room, Tenant, TimeSlot
from people.models import Instructor, Student


class AdminRule(models.Model):
    RULE_CHOICES = [
        ("maxclassesperday", "maxclassesperday"),
        ("room_closed", "room_closed"),
        ("term_limit", "term_limit"),
        ("custom", "custom"),
    ]
    admin_rule_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)
    rule_type = models.CharField(max_length=32, choices=RULE_CHOICES)
    parameter = models.JSONField(default=dict)

    # NEW: global flag
    is_global = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                # allow if global OR room OR slot is set
                check=(
                    models.Q(is_global=True)
                    | models.Q(room__isnull=False)
                    | models.Q(slot__isnull=False)
                ),
                name="adminrule_has_scope",
            )
        ]

    def __str__(self):
        scope = (
            "global"
            if getattr(self, "is_global", False)
            else ("room" if self.room_id else "slot" if self.slot_id else "n/a")
        )
        return f"{self.rule_type} ({scope})"


class BlockedSlot(models.Model):
    blocked_slot_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()

    class Meta:
        unique_together = (("tenant", "slot", "room"),)

    def __str__(self):
        room = self.room.code if self.room_id else "ANY-ROOM"
        return f"Blocked {room} @ {self.slot}"


class ProfessorAvailability(models.Model):
    availability_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    prof = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    available = models.BooleanField()

    class Meta:
        unique_together = (("tenant", "prof", "slot"),)

    def __str__(self):
        return f"{self.prof} @ {self.slot}: {'yes' if self.available else 'no'}"


class StudentPreference(models.Model):
    preference_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)
    preference_score = models.SmallIntegerField()  # e.g. -10..+10

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(course__isnull=False) & models.Q(slot__isnull=True))
                | (models.Q(course__isnull=True) & models.Q(slot__isnull=False)),
                name="pref_course_xor_slot",
            )
        ]

    def __str__(self):
        target = self.course.code if self.course_id else str(self.slot)
        return f"{self.student} prefers {target} [{self.preference_score}]"
