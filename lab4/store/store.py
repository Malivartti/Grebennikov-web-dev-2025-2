from typing import TYPE_CHECKING

from flask_sqlalchemy import SQLAlchemy

if TYPE_CHECKING:
    from lab4.app import Application


class Store:
    def __init__(self, app: "Application"):
        from lab4.user.accessor import UserAccessor

        self.user = UserAccessor(app)


def setup_store(app: "Application"):
    app.db = SQLAlchemy(app)
    app.store = Store(app)
