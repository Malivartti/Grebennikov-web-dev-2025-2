from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from lab5.context_processor import setup_context_processor
from lab5.mw import setup_middlewares

from .config import setup_config
from .login_manager import setup_login_manager
from .routes import setup_routes
from .store.store import Store, setup_store


class Application(Flask):
    def __init__(self, import_name, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)
        self.store: Store | None = None
        self.db: SQLAlchemy | None = None
        self.login_manager: LoginManager | None = None


app = Application(__name__)

setup_config(app)
setup_store(app)
setup_login_manager(app)
setup_middlewares(app)
setup_routes(app)
setup_context_processor(app)
