from enum import StrEnum


class RoleName(StrEnum):
    ADMIN = "администратор"
    MODER = "модератор"
    USER = "пользователь"
    GUEST = "гость"


class Right(StrEnum):
    ANIMAL_VIEW = "animal_view"
    ANIMAL_CREATE = "animal_create"
    ANIMAL_UPDATE = "animal_update"
    ANIMAL_DELETE = "animal_delete"
    ADOPTION_CREATE = "adoption_create"
    ADOPTION_MANAGE = "adoption_manage"
