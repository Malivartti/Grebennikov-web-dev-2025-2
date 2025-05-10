from typing import TYPE_CHECKING

from flask_sqlalchemy import SQLAlchemy

if TYPE_CHECKING:
    from lab5.app import Application


class Store:
    def __init__(self, app: "Application"):
        from lab5.user.accessor import UserAccessor
        from lab5.visit.accessor import VisitAccessor

        self.user = UserAccessor(app)
        self.visit = VisitAccessor(app)


def setup_store(app: "Application"):
    app.db = SQLAlchemy(app)
    app.store = Store(app)

    with app.app_context():
        app.db.create_all()
