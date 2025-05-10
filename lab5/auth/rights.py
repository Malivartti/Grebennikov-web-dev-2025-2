from functools import wraps

from flask import flash, redirect, request, url_for
from flask_login import current_user

role_rights = {
    "Администратор": {
        "create_user",
        "edit_user",
        "view_user",
        "delete_user",
        "view_all_visits",
    },
    "Пользователь": {"edit_self", "view_self", "view_own_visits"},
    None: {"edit_self", "view_self", "view_own_visits"},
}


def check_rights(  # noqa: C901
    required_rights, user_id: int | None = None
):
    def has_rights() -> bool:
        if not current_user.is_authenticated:
            return False

        user_rights = role_rights.get(current_user.role, [])

        target_user_id = user_id
        if (
            target_user_id is None
            and hasattr(request, "view_args")
            and request.view_args
            and "user_id" in request.view_args
        ):
            target_user_id = request.view_args["user_id"]

        for right in required_rights:
            has_right = right in user_rights
            is_self_right = right.endswith("_self")

            if has_right and not is_self_right:
                return True

            if (
                has_right
                and is_self_right
                and target_user_id == current_user.id
            ):
                return True

        return False

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash(
                    "Для доступа к данной странице необходимо "
                    "пройти процедуру аутентификации",
                    "warning",
                )
                next_url = request.script_root + request.path
                return redirect(url_for("login", next=next_url))

            if not has_rights():
                flash(
                    "У вас недостаточно прав доступа.",
                    "warning",
                )
                return redirect(url_for("index"))
            return func(*args, **kwargs)

        return wrapper

    if callable(required_rights):
        raise ValueError(
            "Используйте @check_rights([...]) или check_rights([...])"
        )

    class RightsChecker:
        def __call__(self, *args, **kwargs):
            if args and callable(args[0]):
                return decorator(args[0])
            return has_rights()

        def __bool__(self):
            return has_rights()

    return RightsChecker()
