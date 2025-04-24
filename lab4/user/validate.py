import re


def validate_login(login: str) -> str | None:
    if not login:
        return "Поле не может быть пустым"
    if len(login) < 5:
        return "Логин должен содержать не менее 5 символов"
    if not re.fullmatch(r"[a-zA-Z0-9]+", login):
        return "Логин должен содержать только латинские буквы и цифры"
    return None


allowed_special_chars = r"~!\?@#$%^&*_\-+()\[\]{}><\/|\"\'.,:;"


def validate_password(password: str) -> str | None:  # noqa: PLR0911
    if not password:
        return "Поле не может быть пустым"
    if len(password) < 8:
        return "Пароль должен содержать не менее 8 символов"
    if len(password) > 128:
        return "Пароль не должен превышать 128 символов"
    if " " in password:
        return "Пароль не должен содержать пробелов"
    if not re.search(r"[A-ZА-Я]", password):
        return "Пароль должен содержать как минимум одну заглавную букву"
    if not re.search(r"[a-zа-я]", password):
        return "Пароль должен содержать как минимум одну строчную букву"
    if not re.search(r"[0-9]", password):
        return "Пароль должен содержать как минимум одну цифру"
    for ch in password:
        if not (ch.isalpha() or ch.isdigit() or ch in allowed_special_chars):
            return f"Недопустимый символ в пароле: {ch}"
    return None


def validate_required_field(value: str, field_name: str) -> str | None:
    if not value or not value.strip():
        return "Поле не может быть пустым"
    return None
