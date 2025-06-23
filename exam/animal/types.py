from enum import StrEnum, auto


class Sex(StrEnum):
    MALE = auto()
    FEMALE = auto()


sex_label: dict[Sex, str] = {Sex.MALE: "Мужской", Sex.FEMALE: "Женский"}


class AnimalStatus(StrEnum):
    AVAILABLE = auto()
    ADOPTION = auto()
    ADOPTED = auto()


animal_status_label: dict[AnimalStatus, str] = {
    AnimalStatus.AVAILABLE: "Доступен для усыновления",
    AnimalStatus.ADOPTION: "В процессе усыновления",
    AnimalStatus.ADOPTED: "Усыновлен",
}
