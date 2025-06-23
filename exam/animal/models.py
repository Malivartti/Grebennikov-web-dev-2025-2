from typing import TYPE_CHECKING

from sqlalchemy import (
    TEXT,
    VARCHAR,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from exam.animal.types import AnimalStatus, Sex
from exam.base.base_sqlalchemy import Base
from exam.utils import sanitize_and_render_markdown, strip_markdown_to_text

if TYPE_CHECKING:
    from exam.adoption.models import Adoption


class Animal(Base):
    __tablename__ = "animal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100))
    description: Mapped[str] = mapped_column(TEXT)
    age_months: Mapped[int] = mapped_column(Integer)
    breed: Mapped[str] = mapped_column(VARCHAR(100))
    sex: Mapped[Sex] = mapped_column(
        SQLEnum(
            Sex,
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        )
    )
    status: Mapped[AnimalStatus] = mapped_column(
        SQLEnum(
            AnimalStatus,
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        default=AnimalStatus.AVAILABLE,
    )

    @property
    def description_html(self) -> str:
        return sanitize_and_render_markdown(self.description)

    @property
    def description_preview(self) -> str:
        return strip_markdown_to_text(self.description)

    images: Mapped[list["Image"]] = relationship(
        "Image", back_populates="animal", cascade="all, delete-orphan"
    )
    adoptions: Mapped[list["Adoption"]] = relationship(
        "Adoption", back_populates="animal", cascade="all, delete-orphan"
    )


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(VARCHAR(100))
    mime_type: Mapped[str] = mapped_column(VARCHAR(50))
    animal_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("animal.id", ondelete="CASCADE")
    )

    animal: Mapped["Animal"] = relationship("Animal", back_populates="images")
