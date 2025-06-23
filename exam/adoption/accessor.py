from typing import TYPE_CHECKING, cast

from flask import current_app
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from exam.adoption.models import Adoption
from exam.adoption.types import AdoptionStatus
from exam.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from exam.app import Application

    current_app = cast(Application, current_app)


class AdoptionAccessor(BaseAccessor):
    def get_adoptions_by_animal_id(
        self, *, animal_id: int, page: int = 1, per_page: int = 5
    ) -> dict:
        query = (
            self.session.query(Adoption)
            .options(joinedload(Adoption.user))
            .filter(Adoption.animal_id == animal_id)
            .order_by(Adoption.submission_date.desc())
        )

        total_count = query.count()
        adoptions = query.offset((page - 1) * per_page).limit(per_page).all()

        return {"data": adoptions, "count": total_count}

    def get_user_adoption_for_animal(
        self, *, user_id: int, animal_id: int
    ) -> Adoption:
        return (
            self.session.query(Adoption)
            .filter(
                and_(
                    Adoption.user_id == user_id, Adoption.animal_id == animal_id
                )
            )
            .first()
        )

    def create_adoption(
        self, *, animal_id: int, user_id: int, contact: str
    ) -> Adoption:
        adoption = Adoption(
            animal_id=animal_id,
            user_id=user_id,
            contact=contact,
            status=AdoptionStatus.PENDING,
        )
        self.session.add(adoption)
        self.session.commit()

        current_app.store.animal.update_animal_status(animal_id=animal_id)

        return adoption

    def accept_adoption(self, *, adoption_id: int) -> bool:
        adoption = self.session.get(Adoption, adoption_id)
        if not adoption:
            return False

        try:
            adoption.status = AdoptionStatus.ACCEPTED

            self.session.query(Adoption).filter(
                and_(
                    Adoption.animal_id == adoption.animal_id,
                    Adoption.id != adoption_id,
                    Adoption.status == AdoptionStatus.PENDING,
                )
            ).update({Adoption.status: AdoptionStatus.REJECTED_ADOPTED})

            current_app.store.animal.update_animal_status(
                animal_id=adoption.animal_id
            )

            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e
        else:
            return True

    def reject_adoption(self, *, adoption_id: int) -> bool:
        adoption = self.session.get(Adoption, adoption_id)
        if not adoption:
            return False

        try:
            adoption.status = AdoptionStatus.REJECTED
            self.session.commit()

            current_app.store.animal.update_animal_status(
                animal_id=adoption.animal_id
            )

        except Exception as e:
            self.session.rollback()
            raise e
        else:
            return True
