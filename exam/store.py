from typing import TYPE_CHECKING

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from exam.base.base_sqlalchemy import Base

if TYPE_CHECKING:
    from exam.app import Application


class Store:
    def __init__(self, db: SQLAlchemy):
        from exam.animal.accessor import AnimalAccessor
        from exam.user.accessor import UserAccessor

        self.user = UserAccessor(db)
        self.animal = AnimalAccessor(db)


def setup_store(app: "Application"):
    db = SQLAlchemy(app, model_class=Base)
    migrate = Migrate(app, db)  # noqa: F841

    with app.app_context():
        db.create_all()

    app.store = Store(db)
