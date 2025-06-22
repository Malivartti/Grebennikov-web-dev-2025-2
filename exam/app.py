from flask import Flask

from exam.auth import setup_login_manager
from exam.routes import setup_routes
from exam.store import Store, setup_store


class Application(Flask):
    def __init__(self, import_name, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)
        self.store: Store | None = None


app = Application(__name__)
app.config.from_pyfile("config.py")
setup_store(app)
setup_login_manager(app)
setup_routes(app)
