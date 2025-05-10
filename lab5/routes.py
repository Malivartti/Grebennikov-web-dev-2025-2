from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import Application


def setup_routes(app: "Application"):
    import lab5.auth.routes
    import lab5.user.routes
    import lab5.visit.routes

    lab5.auth.routes.register_routes(app)
    lab5.user.routes.register_routes(app)
    lab5.visit.routes.register_routes(app)
