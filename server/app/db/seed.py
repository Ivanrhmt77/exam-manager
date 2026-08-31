"""Seed dummy data for local development.

Usage:
    python -m app.db.seed
"""

import random

from app.db.base import SessionLocal
from app.models.user import User, UserRole
from app.models.course import Course
from app.models.class_ import Class, Semester
from app.core.security import hash_password

random.seed(42)

DEFAULT_PASSWORD = "password123"

FIRST_NAMES = [
    "Bagas",
    "Citra",
    "Dwi",
    "Eka",
    "Fitri",
    "Galih",
    "Hana",
    "Irfan",
    "Jihan",
    "Kevin",
    "Laras",
    "Miko",
    "Naila",
    "Osman",
    "Putra",
    "Qonita",
    "Rangga",
    "Sasa",
    "Teguh",
    "Umar",
    "Vania",
    "Wahyu",
    "Xena",
    "Yusuf",
    "Zahra",
    "Arka",
    "Bela",
    "Candra",
    "Dila",
    "Erlan",
]

LAST_NAMES = [
    "Pratama",
    "Wijaya",
    "Saputra",
    "Kusuma",
    "Hidayat",
    "Nugraha",
    "Setiawan",
    "Utomo",
    "Permana",
    "Handoko",
    "Firmansyah",
    "Anggara",
    "Purnomo",
    "Santoso",
    "Widodo",
    "Kurniawan",
    "Susanto",
    "Ramadhan",
]


def random_name(used: set[str]) -> str:
    while True:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if name not in used:
            used.add(name)
            return name


COURSES = [
    ("IF-101", "Pemrograman Web", "Dasar pengembangan aplikasi web."),
    ("IF-102", "Struktur Data", "Struktur data dasar dan penerapannya."),
    ("SD-201", "Data Mining", "Teknik ekstraksi pola dari data besar."),
    ("SD-202", "Machine Learning", "Algoritma pembelajaran mesin."),
    ("SD-203", "Neuro Computing", "Jaringan saraf tiruan dan penerapannya."),
    ("SD-204", "Kecerdasan Buatan", "Konsep dasar AI dan penerapannya."),
    ("IF-103", "Basis Data", "Perancangan dan pengelolaan basis data."),
    ("IF-104", "Jaringan Komputer", "Dasar-dasar jaringan komputer."),
]

CLASSES = [
    ("SD-3A", Semester.ODD, 2026),
    ("SD-3B", Semester.ODD, 2026),
    ("TI-3A", Semester.ODD, 2026),
    ("SD-4A", Semester.EVEN, 2025),
    ("TI-4A", Semester.EVEN, 2025),
    ("SD-3A", Semester.ODD_SHORT, 2025),
]

LECTURER_COUNT = 5
STUDENT_COUNT = 30


def get_or_create(session, model, lookup: dict, defaults: dict | None = None):
    instance = session.query(model).filter_by(**lookup).first()
    if instance:
        return instance, False
    instance = model(**{**lookup, **(defaults or {})})
    session.add(instance)
    session.flush()
    return instance, True


def seed():
    session = SessionLocal()
    hashed = hash_password(DEFAULT_PASSWORD)
    used_names: set[str] = set()

    try:
        admin, _ = get_or_create(
            session,
            User,
            lookup={"email": "admin@pens.ac.id"},
            defaults={
                "hashed_password": hashed,
                "role": UserRole.ADMIN,
                "name": "Admin Exam Manager",
                "must_change_password": False,
            },
        )

        lecturers = []
        for i in range(1, LECTURER_COUNT + 1):
            name = random_name(used_names)
            lecturer, _ = get_or_create(
                session,
                User,
                lookup={"email": f"dosen{i}@pens.ac.id"},
                defaults={
                    "hashed_password": hashed,
                    "role": UserRole.LECTURER,
                    "name": name,
                    "nip": f"19800101{2005 + i}01100{i}",
                },
            )
            lecturers.append(lecturer)

        students = []
        for i in range(1, STUDENT_COUNT + 1):
            name = random_name(used_names)
            student, _ = get_or_create(
                session,
                User,
                lookup={"email": f"mahasiswa{i}@pens.ac.id"},
                defaults={
                    "hashed_password": hashed,
                    "role": UserRole.STUDENT,
                    "name": name,
                    "nrp": f"31236000{i:02d}",
                },
            )
            students.append(student)

        courses = []
        for code, name, desc in COURSES:
            course, _ = get_or_create(
                session,
                Course,
                lookup={"code": code},
                defaults={"name": name, "description": desc},
            )
            courses.append(course)

        classes = []
        for name, semester, year in CLASSES:
            cls, _ = get_or_create(
                session,
                Class,
                lookup={"name": name, "semester": semester, "year": year},
            )
            classes.append(cls)

        session.commit()

        print(
            f"Seed completed: 1 admin, {len(lecturers)} lecturers, "
            f"{len(students)} students, {len(courses)} courses, {len(classes)} classes"
        )
        print(f"Default password for all dummy accounts: {DEFAULT_PASSWORD}")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
