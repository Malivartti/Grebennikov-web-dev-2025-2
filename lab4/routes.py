from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import Application


def setup_routes(app: "Application"):
    import lab4.auth.routes
    import lab4.user.routes

    lab4.auth.routes.register_routes(app)
    lab4.user.routes.register_routes(app)
