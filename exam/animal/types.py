from enum import StrEnum


class Sex(StrEnum):
    MALE = "male"
    FEMALE = "female"


sex_label: dict[Sex, str] = {Sex.MALE: "Мужской", Sex.FEMALE: "Женский"}


class AnimalStatus(StrEnum):
    AVAILABLE = "available"
    ADOPTION = "adoption"
    ADOPTED = "adopted"


animal_status_label: dict[AnimalStatus, str] = {
    AnimalStatus.AVAILABLE: "Доступен для усыновления",
    AnimalStatus.ADOPTION: "В процессе усыновления",
    AnimalStatus.ADOPTED: "Усыновлен",
}
