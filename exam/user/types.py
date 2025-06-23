from enum import StrEnum, auto


class RoleName(StrEnum):
    ADMIN = "администратор"
    MODER = "модератор"
    USER = "пользователь"
    GUEST = "гость"


class Right(StrEnum):
    ANIMAL_VIEW = auto()
    ANIMAL_CREATE = auto()
    ANIMAL_UPDATE = auto()
    ANIMAL_DELETE = auto()
    ADOPTION_CREATE = auto()
    ADOPTION_MANAGE = auto()
