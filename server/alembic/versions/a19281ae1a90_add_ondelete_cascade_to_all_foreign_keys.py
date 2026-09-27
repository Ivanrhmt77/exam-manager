"""add_ondelete_cascade_to_all_foreign_keys

Revision ID: a19281ae1a90
Revises: c2e2e7df65f3
Create Date: 2026-09-27 16:29:36.542695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a19281ae1a90'
down_revision: Union[str, Sequence[str], None] = 'c2e2e7df65f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # class_students
    op.drop_constraint(op.f('class_students_user_id_fkey'), 'class_students', type_='foreignkey')
    op.drop_constraint(op.f('class_students_class_id_fkey'), 'class_students', type_='foreignkey')
    op.create_foreign_key('class_students_user_id_fkey', 'class_students', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('class_students_class_id_fkey', 'class_students', 'classes', ['class_id'], ['id'], ondelete='CASCADE')

    # classes
    op.drop_constraint(op.f('classes_user_course_id_fkey'), 'classes', type_='foreignkey')
    op.create_foreign_key('classes_user_course_id_fkey', 'classes', 'user_courses', ['user_course_id'], ['id'], ondelete='CASCADE')

    # user_courses
    op.drop_constraint(op.f('user_courses_user_id_fkey'), 'user_courses', type_='foreignkey')
    op.drop_constraint(op.f('user_courses_course_id_fkey'), 'user_courses', type_='foreignkey')
    op.create_foreign_key('user_courses_user_id_fkey', 'user_courses', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('user_courses_course_id_fkey', 'user_courses', 'courses', ['course_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    # user_courses
    op.drop_constraint('user_courses_course_id_fkey', 'user_courses', type_='foreignkey')
    op.drop_constraint('user_courses_user_id_fkey', 'user_courses', type_='foreignkey')
    op.create_foreign_key('user_courses_course_id_fkey', 'user_courses', 'courses', ['course_id'], ['id'])
    op.create_foreign_key('user_courses_user_id_fkey', 'user_courses', 'users', ['user_id'], ['id'])

    # classes
    op.drop_constraint('classes_user_course_id_fkey', 'classes', type_='foreignkey')
    op.create_foreign_key('classes_user_course_id_fkey', 'classes', 'user_courses', ['user_course_id'], ['id'])

    # class_students
    op.drop_constraint('class_students_class_id_fkey', 'class_students', type_='foreignkey')
    op.drop_constraint('class_students_user_id_fkey', 'class_students', type_='foreignkey')
    op.create_foreign_key('class_students_class_id_fkey', 'class_students', 'classes', ['class_id'], ['id'])
    op.create_foreign_key('class_students_user_id_fkey', 'class_students', 'users', ['user_id'], ['id'])
