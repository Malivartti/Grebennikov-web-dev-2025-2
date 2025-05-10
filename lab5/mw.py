from typing import TYPE_CHECKING

from flask import request
from flask_login import current_user

if TYPE_CHECKING:
    from .app import Application


def setup_middlewares(app: "Application"):
    @app.before_request
    def log_visit():
        if request.method == "GET" and (
            not request.path.startswith("/static/") and request.endpoint
        ):
            user_id = current_user.id if current_user.is_authenticated else None
            app.store.visit.add_visit(request.path, user_id)
