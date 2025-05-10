from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab5.app import Application


def register_routes(app: "Application"):
    from lab5.user.views import (
        index,
        user_create,
        user_delete,
        user_update,
        user_view,
    )

    app.add_url_rule("/", "index", index)
    app.add_url_rule("/users/<int:user_id>", "user_view", user_view)
    app.add_url_rule(
        "/users/create", "user_create", user_create, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/users/<int:user_id>/edit",
        "user_edit",
        user_update,
        methods=["GET", "POST"],
    )
    app.add_url_rule("/users/<int:user_id>/delete", "user_delete", user_delete)
