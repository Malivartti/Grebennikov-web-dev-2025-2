from typing import TYPE_CHECKING

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from exam.adoption.accessor import AdoptionAccessor
from exam.animal.accessor import AnimalAccessor
from exam.base.base_sqlalchemy import Base
from exam.file.accessor import FileAccessor
from exam.user.accessor import UserAccessor

if TYPE_CHECKING:
    from exam.app import Application


class Store:
    def __init__(self, db: SQLAlchemy):
        self.user = UserAccessor(db)
        self.animal = AnimalAccessor(db)
        self.file = FileAccessor()
        self.adoption = AdoptionAccessor(db)


def setup_store(app: "Application"):
    db = SQLAlchemy(app, model_class=Base)
    migrate = Migrate(app, db)  # noqa: F841

    app.store = Store(db)
