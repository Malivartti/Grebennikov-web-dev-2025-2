from functools import wraps
from typing import TYPE_CHECKING, cast

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from exam.config import role_rights
from exam.user.schemas import UserCreate
from exam.user.types import RoleName

if TYPE_CHECKING:
    from exam.app import Application

    current_app = cast(Application, current_app)


bp = Blueprint("auth", __name__, url_prefix="/auth")


def setup_login_manager(app: "Application"):
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = (
        "Для доступа к данной странице необходимо "
        "пройти процедуру аутентификации."
    )
    login_manager.login_message_category = "warning"
    login_manager.user_loader(
        lambda user_id: app.store.user.get_user_by_id(user_id=user_id)
    )
    login_manager.init_app(app)


def check_rights(  # noqa: C901
    required_rights, user_id: int | None = None
):
    def has_rights() -> bool:
        if not current_user.is_authenticated:
            return False
        user_rights = role_rights.get(RoleName(current_user.role.name), [])

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
                    (
                        "Для доступа к данной странице необходимо "
                        "пройти процедуру аутентификации"
                    ),
                    "warning",
                )
                next_url = request.script_root + request.path
                return redirect(url_for("login", next=next_url))

            if not has_rights():
                flash(
                    "У вас недостаточно прав для выполнения данного действия",
                    "warning",
                )
                return redirect(url_for("animal.index"))
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


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login and password:
            user = current_app.store.user.get_user_by_login(login=login)
            if user and user.check_password(password):
                login_user(user)
                flash("Вы успешно аутентифицированы.", "success")
                next_url = request.args.get("next")
                return redirect(next_url or url_for("main.index"))
        flash("Введены неверные логин и/или пароль.", "danger")
    return render_template("auth/login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        middle_name = request.form.get("middle_name")
        role_id = current_app.store.user.get_role_by_name(
            role_name=RoleName.USER
        ).id

        if not all([login, password, confirm_password, first_name, last_name]):
            flash("Все обязательные поля должны быть заполнены.", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Пароли не совпадают.", "danger")
            return render_template(
                "auth/register.html",
            )

        if len(password) < 8:
            flash("Пароль должен содержать минимум 8 символов.", "danger")
            return render_template(
                "auth/register.html",
            )

        existing_user = current_app.store.user.get_user_by_login(login=login)
        if existing_user:
            flash("Пользователь с таким логином уже существует.", "danger")
            return render_template(
                "auth/register.html",
            )

        try:
            user_data = UserCreate(
                login=login,
                password=password,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                role_id=role_id,
            )

            current_app.store.user.create_user(user_in=user_data)
            flash(
                "Регистрация прошла успешно! Теперь вы можете войти в систему.",
                "success",
            )
            return redirect(url_for("auth.login"))

        except Exception as e:
            flash(f"Ошибка при регистрации: {e}", "danger")

    return render_template("auth/register.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
