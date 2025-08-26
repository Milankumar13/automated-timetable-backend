from django.db import models
from django.core.validators import MinValueValidator
from common.models import BaseModel

class Department(BaseModel):
    """Academic departments (e.g., CSE)."""
    code = models.CharField(max_length=32, unique=True)   # short code
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    def __str__(self): return f"{self.code} — {self.name}"

class Building(BaseModel):
    """Campus buildings."""
    code = models.CharField(max_length=32, unique=True)   # e.g., ENG
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return f"{self.code} — {self.name}"

class Room(BaseModel):
    """Rooms with capacity."""
    building = models.ForeignKey(Building, on_delete=models.RESTRICT, related_name="rooms")
    code = models.CharField(max_length=64)                # e.g., 101
    name = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = [("building", "code")]
    def __str__(self): return f"{self.building.code}-{self.code}"

class Feature(BaseModel):
    """Room feature catalog (equipment/traits)."""
    code = models.CharField(max_length=64, unique=True)   # e.g., PROJECTOR, LAB
    name = models.CharField(max_length=255)
    def __str__(self): return self.code

class RoomFeature(BaseModel):
    """Room has features (with quantity)."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_features")
    feature = models.ForeignKey(Feature, on_delete=models.RESTRICT, related_name="feature_rooms")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    class Meta:
        unique_together = [("room", "feature")]
    def __str__(self): return f"{self.room} → {self.feature.code} x{self.quantity}"

class Course(BaseModel):
    """Course under a department (e.g., CSE101)."""
    department = models.ForeignKey(Department, on_delete=models.RESTRICT, related_name="courses")
    code = models.CharField(max_length=32)                # e.g., CSE101
    name = models.CharField(max_length=255)
    credits = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = [("department", "code")]
    def __str__(self): return f"{self.department.code}-{self.code}"

class Subject(BaseModel):
    """Atomic teachable unit under a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects")
    code = models.CharField(max_length=64)                # e.g., CSE101-ALG
    name = models.CharField(max_length=255)
    hours_per_week = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    expected_size = models.PositiveIntegerField(null=True, blank=True)  # for capacity planning
    class Meta:
        unique_together = [("course", "code")]
    def __str__(self): return f"{self.course}-{self.code}"

class SubjectNeed(BaseModel):
    """What the subject requires in the room (features with quantities)."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="needs")
    feature = models.ForeignKey(Feature, on_delete=models.RESTRICT, related_name="needed_by_subjects")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    class Meta:
        unique_together = [("subject", "feature")]
    def __str__(self): return f"{self.subject} needs {self.feature.code} x{self.quantity}"
