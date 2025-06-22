from flask_sqlalchemy import SQLAlchemy


class BaseAccessor:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    @property
    def session(self):
        return self.db.session
