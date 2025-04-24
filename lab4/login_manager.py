from typing import TYPE_CHECKING

from flask_login import LoginManager

if TYPE_CHECKING:
    from .app import Application


def setup_login_manager(app: "Application"):
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "login"
    login_manager.login_message = (
        "Для доступа к данной странице "
        "необходимо пройти процедуру аутентификации"
    )
    login_manager.login_message_category = "warning"
    app.login_manager = login_manager
