import uuid

from django.db import models

from catalog.models import CourseOffering, Department, Section, Tenant


class Instructor(models.Model):
    prof_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    display_name = models.CharField(max_length=200)

    def __str__(self):
        return self.display_name


class Student(models.Model):
    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    display_name = models.CharField(max_length=200)
    cohort = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.display_name


class Enrollment(models.Model):
    enrollment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("tenant", "student", "offering"),)

    def __str__(self):
        return f"{self.student} → {self.offering}"
