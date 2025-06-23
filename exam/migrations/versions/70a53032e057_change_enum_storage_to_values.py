"""Change enum storage to values

Revision ID: 70a53032e057
Revises: 7e6a8fe95a88
Create Date: 2025-06-23 23:48:19.723245

"""

from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "70a53032e057"
down_revision = "7e6a8fe95a88"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "animal",
        "sex",
        existing_type=mysql.ENUM("MALE", "FEMALE"),
        type_=mysql.ENUM("male", "female"),
        existing_nullable=True,
    )

    op.alter_column(
        "animal",
        "status",
        existing_type=mysql.ENUM("AVAILABLE", "ADOPTION", "ADOPTED"),
        type_=mysql.ENUM("available", "adoption", "adopted"),
        existing_nullable=True,
    )

    op.execute("UPDATE animal SET sex = LOWER(sex)")
    op.execute("UPDATE animal SET status = LOWER(status)")

    op.alter_column(
        "adoption",
        "status",
        existing_type=mysql.ENUM(
            "PENDING", "ACCEPTED", "REJECTED", "REJECTED_ADOPTED"
        ),
        type_=mysql.ENUM("pending", "accepted", "rejected", "rejected_adopted"),
        existing_nullable=True,
    )

    op.execute("UPDATE adoption SET status = LOWER(status)")


def downgrade():
    op.execute("UPDATE animal SET sex = UPPER(sex)")
    op.execute("UPDATE animal SET status = UPPER(status)")
    op.execute("UPDATE adoption SET status = UPPER(status)")

    op.alter_column(
        "animal",
        "sex",
        existing_type=mysql.ENUM("male", "female"),
        type_=mysql.ENUM("MALE", "FEMALE"),
        existing_nullable=True,
    )

    op.alter_column(
        "animal",
        "status",
        existing_type=mysql.ENUM("available", "adoption", "adopted"),
        type_=mysql.ENUM("AVAILABLE", "ADOPTION", "ADOPTED"),
        existing_nullable=True,
    )

    op.alter_column(
        "adoption",
        "status",
        existing_type=mysql.ENUM(
            "pending", "accepted", "rejected", "rejected_adopted"
        ),
        type_=mysql.ENUM("PENDING", "ACCEPTED", "REJECTED", "REJECTED_ADOPTED"),
        existing_nullable=True,
    )
