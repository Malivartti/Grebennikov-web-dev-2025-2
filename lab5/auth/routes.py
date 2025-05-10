from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab5.app import Application


def register_routes(app: "Application"):
    from lab5.auth.views import change_password, login, logout

    app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
    app.add_url_rule("/logout", "logout", logout)
    app.add_url_rule(
        "/change_password",
        "change_password",
        change_password,
        methods=["GET", "POST"],
    )
