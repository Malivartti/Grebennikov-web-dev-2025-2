from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab5.app import Application


def register_routes(app: "Application"):
    from lab5.visit.views import visit_bp

    app.register_blueprint(visit_bp)
