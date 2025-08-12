from datetime import time

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import (
    Course,
    CourseOffering,
    Department,
    Room,
    Section,
    Tenant,
    Term,
    TimeSlot,
)
from constraintsapp.models import AdminRule, BlockedSlot, ProfessorAvailability
from people.models import Instructor, Student


class Command(BaseCommand):
    help = "Seed pilot dataset"

    @transaction.atomic
    def handle(self, *args, **opts):
        tenant, _ = Tenant.objects.get_or_create(name="PilotU")
        term, _ = Term.objects.get_or_create(
            tenant=tenant,
            code="2025-FALL",
            defaults={"starts_on": "2025-09-01", "ends_on": "2025-12-20"},
        )
        dept, _ = Department.objects.get_or_create(
            tenant=tenant, code="CS", defaults={"name": "Computer Science"}
        )

        rooms = [
            ("R101", 60, {"projector": True}),
            ("R102", 40, {"lab": True, "computers": 25}),
            ("R103", 80, {"projector": True}),
            ("R201", 35, {}),
            ("R202", 50, {"wheelchair": True}),
        ]
        for code, cap, feat in rooms:
            Room.objects.get_or_create(
                tenant=tenant,
                code=code,
                defaults={"department": dept, "capacity": cap, "features": feat},
            )

        # Mon–Fri official slots: 09-10, 10-11, 11-12, 13-14, 14-15, 15-16
        for day in range(1, 6):
            for st, et in [
                (time(9, 0), time(10, 0)),
                (time(10, 0), time(11, 0)),
                (time(11, 0), time(12, 0)),
                (time(13, 0), time(14, 0)),
                (time(14, 0), time(15, 0)),
                (time(15, 0), time(16, 0)),
            ]:
                TimeSlot.objects.get_or_create(
                    tenant=tenant,
                    day=day,
                    start_time=st,
                    end_time=et,
                    defaults={"is_official": True},
                )

        courses = [
            ("CS101", "Intro to Programming"),
            ("CS102", "Data Structures"),
            ("CS201", "Algorithms"),
            ("CS221", "Databases"),
            ("CS241", "Networks"),
            ("CS251", "Operating Systems"),
            ("CS261", "AI Basics"),
            ("CS271", "HCI"),
            ("CS281", "Software Eng"),
            ("CS291", "Discrete Math"),
        ]
        for code, title in courses:
            c, _ = Course.objects.get_or_create(
                tenant=tenant, department=dept, code=code, defaults={"title": title}
            )
            off, _ = CourseOffering.objects.get_or_create(
                tenant=tenant, course=c, term=term, defaults={"expected_enrollment": 40}
            )
            Section.objects.get_or_create(
                tenant=tenant,
                offering=off,
                section_code="A",
                defaults={"meetings_per_week": 3, "minutes_per_meeting": 60},
            )

        for i in range(1, 10 + 1):
            Instructor.objects.get_or_create(
                tenant=tenant, display_name=f"Prof {i}", email=f"prof{i}@pilotu.edu"
            )
        for i in range(1, 15 + 1):
            Student.objects.get_or_create(
                tenant=tenant, display_name=f"Student {i}", email=f"s{i}@pilotu.edu"
            )

        # Availability for first 5 profs: Mon/Tue 09–11
        profs = Instructor.objects.filter(tenant=tenant).order_by("display_name")[:5]
        slots = TimeSlot.objects.filter(
            tenant=tenant, day__in=[1, 2], start_time__in=[time(9, 0), time(10, 0)]
        )
        for p in profs:
            for s in slots:
                ProfessorAvailability.objects.get_or_create(
                    tenant=tenant, prof=p, slot=s, defaults={"available": True}
                )

        # Block R101 on Wed 13:00
        r101 = Room.objects.get(tenant=tenant, code="R101")
        wed_13 = TimeSlot.objects.get(tenant=tenant, day=3, start_time=time(13, 0))
        BlockedSlot.objects.get_or_create(
            tenant=tenant, room=r101, slot=wed_13, defaults={"reason": "Maintenance"}
        )

        # Example admin rule
        AdminRule.objects.get_or_create(
            tenant=tenant,
            rule_type="maxclassesperday",
            room=None,
            slot=None,
            is_global=True,
            defaults={"parameter": {"limit": 3}},
        )

        self.stdout.write(self.style.SUCCESS("Pilot seed complete."))
