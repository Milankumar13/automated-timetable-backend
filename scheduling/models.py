from django.db import models
from common.models import BaseModel

class Semester(BaseModel):
    """Academic semester (replaces Term)."""
    code = models.CharField(max_length=32, unique=True)   # e.g., 2025-S1
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(end_date__gte=models.F('start_date')),
                                   name='semester_end_after_start')
        ]
    def __str__(self): return self.code

class Slot(BaseModel):
    """Discrete official time slots within a semester."""
    MON, TUE, WED, THU, FRI, SAT, SUN = range(1, 8)
    DOW_CHOICES = [(MON,"Mon"),(TUE,"Tue"),(WED,"Wed"),(THU,"Thu"),(FRI,"Fri"),(SAT,"Sat"),(SUN,"Sun")]
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='slots')
    dow = models.PositiveSmallIntegerField(choices=DOW_CHOICES)  # 1..7
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_official = models.BooleanField(default=True)             # within teaching hours
    class Meta:
        unique_together = [('semester', 'dow', 'start_time', 'end_time')]
        constraints = [
            models.CheckConstraint(check=models.Q(end_time__gt=models.F('start_time')),
                                   name='slot_end_after_start')
        ]
    def __str__(self): return f"{self.semester.code} {self.get_dow_display()} {self.start_time}-{self.end_time}"

class ProfAvailability(BaseModel):
    """Professor availability per slot (TRUE = can teach)."""
    professor = models.ForeignKey('people.Professor', on_delete=models.CASCADE, related_name='availabilities')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='prof_availabilities')
    available = models.BooleanField(default=True)
    note = models.TextField(null=True, blank=True)
    class Meta:
        unique_together = [('professor', 'slot')]

class RoomSlotBlock(BaseModel):
    """Block a room in a specific slot (maintenance/events)."""
    room = models.ForeignKey('catalog.Room', on_delete=models.CASCADE, related_name='blocked_slots')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='room_blocks')
    reason = models.TextField(null=True, blank=True)
    class Meta:
        unique_together = [('room', 'slot')]

class ClassPlan(BaseModel):
    """
    Weekly plan: subject + professor + room + slot.
    DB constraints prevent room/professor double-booking across all departments.
    """
    department = models.ForeignKey('catalog.Department', on_delete=models.RESTRICT, related_name='class_plans')
    subject = models.ForeignKey('catalog.Subject', on_delete=models.RESTRICT, related_name='class_plans')
    professor = models.ForeignKey('people.Professor', on_delete=models.RESTRICT, related_name='class_plans')
    room = models.ForeignKey('catalog.Room', on_delete=models.RESTRICT, related_name='class_plans')
    slot = models.ForeignKey(Slot, on_delete=models.RESTRICT, related_name='class_plans')

    status = models.CharField(max_length=16, default='ACTIVE')  # ACTIVE/PAUSED/CANCELLED
    note = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot','room'], name='uniq_plan_room_per_slot'),       # one room per slot
            models.UniqueConstraint(fields=['slot','professor'], name='uniq_plan_prof_per_slot'), # one prof per slot
        ]
        indexes = [
            models.Index(fields=['slot','room']),
            models.Index(fields=['slot','professor']),
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return f"{self.subject} @ {self.slot} in {self.room} by {self.professor}"

class ClassSession(BaseModel):
    """
    Dated occurrence:
      - CANCELLED: professor cancels this date
      - RESCHEDULED: moved to different day/slot/room/prof
      - EXTRA: additional session not in the weekly plan
    """
    plan = models.ForeignKey(ClassPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    semester = models.ForeignKey(Semester, on_delete=models.RESTRICT, related_name='class_sessions')
    day_date = models.DateField()
    slot = models.ForeignKey(Slot, on_delete=models.RESTRICT, related_name='class_sessions')

    # resolved resources for this date (may differ from plan when rescheduled)
    subject = models.ForeignKey('catalog.Subject', on_delete=models.RESTRICT, related_name='class_sessions')
    professor = models.ForeignKey('people.Professor', on_delete=models.RESTRICT, related_name='class_sessions')
    room = models.ForeignKey('catalog.Room', on_delete=models.RESTRICT, related_name='class_sessions')

    status = models.CharField(
        max_length=16,
        default='PLANNED',
        choices=[('PLANNED','PLANNED'),('CANCELLED','CANCELLED'),
                 ('RESCHEDULED','RESCHEDULED'),('EXTRA','EXTRA'),('COMPLETED','COMPLETED')]
    )
    change_reason = models.TextField(null=True, blank=True)
    replaces_session = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                         related_name='replacement_sessions')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day_date','slot','room'], name='uniq_session_room_on_date_slot'),
            models.UniqueConstraint(fields=['day_date','slot','professor'], name='uniq_session_prof_on_date_slot'),
        ]
        indexes = [
            models.Index(fields=['day_date','slot']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.day_date} {self.slot} — {self.subject} in {self.room} by {self.professor} [{self.status}]"
