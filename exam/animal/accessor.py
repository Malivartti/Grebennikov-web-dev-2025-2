from dataclasses import asdict
from typing import Any

from flask import current_app
from sqlalchemy import and_, desc, func, or_
from sqlalchemy.orm import joinedload

from exam.adoption.models import Adoption
from exam.adoption.types import AdoptionStatus
from exam.animal.models import Animal, Image
from exam.animal.schemas import AnimalListParams, CreateAnimal, UpdateAnimal
from exam.animal.types import AnimalStatus
from exam.base.base_accessor import BaseAccessor


class AnimalAccessor(BaseAccessor):
    def get_animals(self, *, params: AnimalListParams) -> dict[str, Any]:
        adoption_count_subquery = (
            self.session.query(func.count(Adoption.id))
            .filter(Adoption.animal_id == Animal.id)
            .scalar_subquery()
        )

        query = self.session.query(
            Animal, adoption_count_subquery.label("adoption_count")
        ).options(joinedload(Animal.images))

        filters = []
        if params.search:
            search_filter = or_(
                Animal.name.ilike(f"%{params.search}%"),
                Animal.description.ilike(f"%{params.search}%"),
                Animal.breed.ilike(f"%{params.search}%"),
            )
            filters.append(search_filter)

        if params.sex:
            filters.append(Animal.sex == params.sex)

        if params.status:
            filters.append(Animal.status == params.status)

        if filters:
            query = query.filter(and_(*filters))

        query = query.order_by(
            desc(Animal.status == AnimalStatus.AVAILABLE),
            Animal.id.desc(),
        )

        total_count = query.count()
        results = (
            query.offset((params.page - 1) * params.per_page)
            .limit(params.per_page)
            .all()
        )

        animals_with_counts = []
        for animal, adoption_count in results:
            animal.adoption_count = adoption_count or 0
            animals_with_counts.append(animal)

        return {"data": animals_with_counts, "count": total_count}

    def get_animal_by_id(self, *, animal_id: int) -> Animal:
        return (
            self.session.query(Animal)
            .options(joinedload(Animal.images))
            .filter(Animal.id == animal_id)
            .first()
        )

    def create_animal(self, *, create_animal: CreateAnimal) -> Animal:
        animal = Animal(**asdict(create_animal))
        self.session.add(animal)
        self.session.commit()
        return animal

    def create_animal_with_images(
        self, *, create_animal: CreateAnimal, images_data: list
    ) -> Animal:
        try:
            animal = Animal(**asdict(create_animal))
            self.session.add(animal)
            self.session.flush()

            for image_data in images_data:
                image_data["animal_id"] = animal.id
                image = Image(**image_data)
                self.session.add(image)

            self.session.commit()

            self.session.refresh(animal)

        except Exception as e:
            self.session.rollback()
            current_app.logger.exception(
                "Ошибка при создании животного с изображениями"
            )
            raise e
        else:
            return animal

    def update_animal(self, *, update_animal: UpdateAnimal) -> Animal:
        animal = self.get_animal_by_id(animal_id=update_animal.id)
        if not animal:
            return None

        for k, v in asdict(update_animal).items():
            if k != "id":
                setattr(animal, k, v)
        self.session.commit()
        return animal

    def update_animal_status(self, *, animal_id: int) -> None:
        animal = self.get_animal_by_id(animal_id=animal_id)
        if not animal:
            return

        accepted_adoption = (
            self.session.query(Adoption)
            .filter(
                and_(
                    Adoption.animal_id == animal_id,
                    Adoption.status == AdoptionStatus.ACCEPTED,
                )
            )
            .first()
        )

        if accepted_adoption:
            animal.status = AnimalStatus.ADOPTED
        else:
            pending_adoption = (
                self.session.query(Adoption)
                .filter(
                    and_(
                        Adoption.animal_id == animal_id,
                        Adoption.status == AdoptionStatus.PENDING,
                    )
                )
                .first()
            )

            if pending_adoption:
                animal.status = AnimalStatus.ADOPTION
            else:
                animal.status = AnimalStatus.AVAILABLE

        self.session.commit()

    def delete_animal(self, *, animal_id: int) -> bool:
        animal = self.get_animal_by_id(animal_id=animal_id)
        if not animal:
            return False

        try:
            filenames = [image.filename for image in animal.images]

            self.session.delete(animal)
            self.session.commit()

            if filenames:
                file_accessor = current_app.store.file
                delete_results = file_accessor.delete_files(filenames=filenames)

                if delete_results["failed"]:
                    current_app.logger.warning(
                        "Животное удалено из БД, "
                        "но не удалось удалить файлы: %s",
                        delete_results["failed"],
                    )

        except Exception as e:
            self.session.rollback()
            current_app.logger.exception(
                "Ошибка при удалении животного %s", animal_id
            )
            raise e
        else:
            return True

    def delete_image(self, *, image_id: int) -> bool:
        image = self.session.query(Image).filter(Image.id == image_id).first()
        if not image:
            return False

        try:
            filename = image.filename

            self.session.delete(image)
            self.session.commit()

            file_accessor = current_app.store.file
            file_deleted = file_accessor.delete_file(filename=filename)

            if not file_deleted:
                current_app.logger.warning(
                    "Запись изображения %s удалена из БД, но файл %s не найден",
                    image_id,
                    filename,
                )

        except Exception:
            self.session.rollback()
            current_app.logger.exception(
                "Ошибка при удалении изображения %s", image_id
            )
            return False
        else:
            return True
