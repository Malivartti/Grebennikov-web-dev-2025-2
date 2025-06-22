from dataclasses import dataclass

from flask_login import UserMixin
from sqlalchemy import TEXT, VARCHAR, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from exam.base.base_sqlalchemy import Base


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    description: Mapped[str] = mapped_column(TEXT)


class User(Base, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(VARCHAR(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255))
    last_name: Mapped[str] = mapped_column(VARCHAR(100))
    first_name: Mapped[str] = mapped_column(VARCHAR(100))
    middle_name: Mapped[str | None] = mapped_column(VARCHAR(100), nullable=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role.id"))

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    role: Mapped["Role"] = relationship("Role")


@dataclass
class UserCreate:
    login: str
    password: str
    last_name: str
    first_name: str
    middle_name: str | None
    role_id: int
