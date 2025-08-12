import uuid

from django.db import models

from catalog.models import Room, Section, Tenant, Term, TimeSlot
from people.models import Instructor


class TimetableRun(models.Model):
    STATUS = [("PENDING", "PENDING"), ("SUCCESS", "SUCCESS"), ("FAILURE", "FAILURE")]
    run_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.RESTRICT)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    runtime_ms = models.IntegerField(null=True, blank=True)
    soft_score = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(max_length=16, choices=STATUS, default="PENDING")
    solver_name = models.CharField(max_length=128, blank=True, null=True)
    input_hash = models.TextField(blank=True, null=True)
    notes = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Run {self.run_id} [{self.status}] {self.term.code}"


class Assignment(models.Model):
    assignment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    run = models.ForeignKey(TimetableRun, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    prof = models.ForeignKey(Instructor, on_delete=models.RESTRICT)
    room = models.ForeignKey(Room, on_delete=models.RESTRICT)
    slot = models.ForeignKey(TimeSlot, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["run", "room", "slot"], name="uniq_run_room_slot"
            ),
            models.UniqueConstraint(
                fields=["run", "prof", "slot"], name="uniq_run_prof_slot"
            ),
            models.UniqueConstraint(fields=["run", "section"], name="uniq_run_section"),
        ]

    def __str__(self):
        return f"{self.section} → {self.room} @ {self.slot} by {self.prof}"
