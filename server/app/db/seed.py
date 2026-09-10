"""Seed dummy data for local development.

Usage:
    python -m app.db.seed                      # seed everything
    python -m app.db.seed --only users          # seed users only
    python -m app.db.seed --only courses classes  # seed courses and classes only
"""

import argparse
import random

from datetime import time

from app.db.base import SessionLocal
from app.models.user import User, UserRole
from app.models.course import Course, CourseCategory, CourseDeliveryType
from app.models.user_course import UserCourse
from app.models.class_ import Class, Term, ClassStatus
from app.models.class_student import ClassStudent
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
    (
        "IF-101",
        "Pemrograman Web",
        "Dasar pengembangan aplikasi web.",
        3,
        CourseCategory.MPI,
        CourseDeliveryType.THEORETICAL,
    ),
    (
        "IF-102",
        "Struktur Data",
        "Struktur data dasar dan penerapannya.",
        3,
        CourseCategory.MPI,
        CourseDeliveryType.THEORETICAL,
    ),
    (
        "SD-201",
        "Workshop Data Mining",
        "Teknik ekstraksi pola dari data besar.",
        3,
        CourseCategory.MPP,
        CourseDeliveryType.WORKSHOP,
    ),
    (
        "SD-202",
        "Workshop Machine Learning",
        "Algoritma pembelajaran mesin.",
        3,
        CourseCategory.MPP,
        CourseDeliveryType.WORKSHOP,
    ),
    (
        "SD-203",
        "Workshop Neuro Computing",
        "Jaringan saraf tiruan dan penerapannya.",
        3,
        CourseCategory.MPP,
        CourseDeliveryType.WORKSHOP,
    ),
    (
        "SD-204",
        "Kecerdasan Buatan",
        "Konsep dasar AI dan penerapannya.",
        3,
        CourseCategory.MW,
        CourseDeliveryType.THEORETICAL,
    ),
    (
        "IF-103",
        "Praktikum Basis Data",
        "Perancangan dan pengelolaan basis data.",
        2,
        CourseCategory.MPI,
        CourseDeliveryType.PRACTICUM,
    ),
    (
        "IF-104",
        "Jaringan Komputer",
        "Dasar-dasar jaringan komputer.",
        2,
        CourseCategory.MPK,
        CourseDeliveryType.THEORETICAL,
    ),
]

DAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
TIME_SLOTS = [
    (time(7, 0), time(9, 30)),
    (time(9, 30), time(12, 0)),
    (time(13, 0), time(15, 30)),
    (time(15, 30), time(18, 0)),
]
ROOMS = ["TC-301", "TC-302", "TC-303", "SDT-101", "SDT-102", "Lab Jaringan"]

CLASS_INDEX_LABELS = "ABCDEFGH"

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


def seed_users(session, hashed: str, used_names: set[str]) -> tuple[list, list]:
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

    print(
        f"Users seeded: 1 admin, {len(lecturers)} lecturers, {len(students)} students"
    )
    return lecturers, students


def seed_courses(session) -> list:
    courses = []
    for code, name, desc, credits, category, delivery_type in COURSES:
        course, _ = get_or_create(
            session,
            Course,
            lookup={"code": code},
            defaults={
                "name": name,
                "description": desc,
                "credits": credits,
                "category": category,
                "delivery_type": delivery_type,
            },
        )
        courses.append(course)

    print(f"Courses seeded: {len(courses)} courses")
    return courses


def seed_user_courses(session) -> list:
    """Assign each course to a lecturer (round-robin)."""
    lecturers = (
        session.query(User).filter_by(role=UserRole.LECTURER, is_deleted=False).all()
    )
    courses = session.query(Course).filter_by(is_deleted=False).all()

    if not lecturers or not courses:
        print("UserCourses skipped: seed users & courses first")
        return []

    user_courses = []
    for i, course in enumerate(courses):
        lecturer = lecturers[i % len(lecturers)]
        uc, _ = get_or_create(
            session,
            UserCourse,
            lookup={"user_id": lecturer.id, "course_id": course.id},
        )
        user_courses.append(uc)

    print(f"UserCourses seeded: {len(user_courses)} lecturer-course assignments")
    return user_courses


def seed_classes(session) -> list:
    """Create classes for each user_course. First 3 get 2 classes (A, B), rest get 1 (A)."""
    user_courses = session.query(UserCourse).filter_by(is_deleted=False).all()

    if not user_courses:
        print("Classes skipped: seed user_courses first")
        return []

    classes = []
    schedule_slot = 0
    for i, uc in enumerate(user_courses):
        num_classes = 2 if i < 3 else 1
        term = Term.ODD if i % 2 == 0 else Term.EVEN
        for class_index in range(num_classes):
            day = DAYS[schedule_slot % len(DAYS)]
            start_time, end_time = TIME_SLOTS[schedule_slot % len(TIME_SLOTS)]
            room = ROOMS[schedule_slot % len(ROOMS)]
            schedule_slot += 1

            cls, _ = get_or_create(
                session,
                Class,
                lookup={"user_course_id": uc.id, "class_index": class_index},
                defaults={
                    "name": f"{uc.course.name} - Class {CLASS_INDEX_LABELS[class_index]}",
                    "academic_year": 2026,
                    "term": term,
                    "status": ClassStatus.ACTIVE,
                    "schedule_day": day,
                    "schedule_start_time": start_time,
                    "schedule_end_time": end_time,
                    "room": room,
                },
            )
            classes.append(cls)

    print(f"Classes seeded: {len(classes)} classes")
    return classes


def seed_class_students(session) -> list:
    """Distribute students across classes round-robin."""
    classes = session.query(Class).filter_by(is_deleted=False).all()
    students = (
        session.query(User).filter_by(role=UserRole.STUDENT, is_deleted=False).all()
    )

    if not classes or not students:
        print("ClassStudents skipped: seed classes & users first")
        return []

    enrollments = []
    per_class = max(1, len(students) // len(classes))
    idx = 0
    for cls in classes:
        for _ in range(per_class):
            student = students[idx % len(students)]
            idx += 1
            cs, _ = get_or_create(
                session,
                ClassStudent,
                lookup={"class_id": cls.id, "user_id": student.id},
            )
            enrollments.append(cs)

    print(f"ClassStudents seeded: {len(enrollments)} enrollments")
    return enrollments


SEEDERS = {
    "users": lambda session, hashed, used_names: seed_users(
        session, hashed, used_names
    ),
    "courses": lambda session, hashed, used_names: seed_courses(session),
    "user_courses": lambda session, hashed, used_names: seed_user_courses(session),
    "classes": lambda session, hashed, used_names: seed_classes(session),
    "class_students": lambda session, hashed, used_names: seed_class_students(session),
}


def seed(only: list[str] | None = None):
    targets = only or list(SEEDERS.keys())

    invalid = [t for t in targets if t not in SEEDERS]
    if invalid:
        raise ValueError(
            f"Unknown seed target(s): {invalid}. Valid options: {list(SEEDERS.keys())}"
        )

    session = SessionLocal()
    hashed = hash_password(DEFAULT_PASSWORD)
    used_names: set[str] = set()

    try:
        for target in targets:
            SEEDERS[target](session, hashed, used_names)

        session.commit()
        print(f"Seed completed for: {', '.join(targets)}")
        if "users" in targets:
            print(f"Default password for all dummy accounts: {DEFAULT_PASSWORD}")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seed dummy data for local development."
    )
    parser.add_argument(
        "--only",
        nargs="+",
        choices=list(SEEDERS.keys()),
        help="Seed only the specified table(s). If omitted, seeds everything.",
    )
    args = parser.parse_args()
    seed(only=args.only)
