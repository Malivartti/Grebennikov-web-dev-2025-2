from dataclasses import dataclass

from exam.animal.models import AnimalStatus, Sex


@dataclass
class AnimalListParams:
    page: int = 1
    per_page: int = 10
    search: str | None = None
    sex: Sex | None = None
    status: AnimalStatus | None = None


@dataclass
class CreateAnimal:
    name: str
    description: str
    age_months: int
    breed: str
    sex: Sex


@dataclass
class UpdateAnimal:
    id: int
    name: str
    description: str
    age_months: int
    breed: str
    sex: Sex
