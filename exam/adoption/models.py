from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import DATE, VARCHAR, Enum as SQLEnum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from exam.adoption.types import AdoptionStatus
from exam.base.base_sqlalchemy import Base
from exam.user.models import User

if TYPE_CHECKING:
    from exam.animal.models import Animal


class Adoption(Base):
    __tablename__ = "adoption"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    animal_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("animal.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    submission_date: Mapped[date] = mapped_column(DATE, default=date.today)
    status: Mapped[AdoptionStatus] = mapped_column(
        SQLEnum(
            AdoptionStatus,
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        default=AdoptionStatus.PENDING,
    )
    contact: Mapped[str] = mapped_column(VARCHAR(50))

    animal: Mapped["Animal"] = relationship("Animal")
    user: Mapped["User"] = relationship("User")
