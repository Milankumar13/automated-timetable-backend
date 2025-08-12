import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Tenant(models.Model):
    tenant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Term(models.Model):
    term_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    code = models.CharField(max_length=32)  # '2025-FALL'
    starts_on = models.DateField()
    ends_on = models.DateField()

    class Meta:
        unique_together = (("tenant", "code"),)

    def __str__(self):
        return self.code


class Department(models.Model):
    department_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = (("tenant", "code"),)

    def __str__(self):
        return f"{self.code} — {self.name}"


class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    code = models.CharField(max_length=32)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    features = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (("tenant", "code"),)

    def __str__(self):
        return f"{self.code} (cap {self.capacity})"


class TimeSlot(models.Model):
    slot_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField()  # 1..7
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_official = models.BooleanField(default=False)
    label = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="timeslot_range_ok",
            )
        ]
        unique_together = (("tenant", "day", "start_time", "end_time"),)

    def __str__(self):
        return self.label or f"D{self.day} {self.start_time}-{self.end_time}"


class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=200)
    default_minutes = models.PositiveSmallIntegerField(
        default=60, validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = (("tenant", "code"),)

    def __str__(self):
        return f"{self.code} — {self.title}"


class CourseOffering(models.Model):
    offering_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    term = models.ForeignKey(Term, on_delete=models.RESTRICT)
    expected_enrollment = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = (("tenant", "course", "term"),)

    def __str__(self):
        return f"{self.course.code} @ {self.term.code}"


class Section(models.Model):
    section_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    section_code = models.CharField(max_length=16)  # 'A', 'B1'
    meetings_per_week = models.PositiveSmallIntegerField(default=1)
    minutes_per_meeting = models.PositiveSmallIntegerField(default=60)

    class Meta:
        unique_together = (("tenant", "offering", "section_code"),)

    def __str__(self):
        return f"{self.offering.course.code}-{self.section_code}"
