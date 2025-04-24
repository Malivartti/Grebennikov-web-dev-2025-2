from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab4.app import Application


def register_routes(app: "Application"):
    from lab4.user.views import (
        index,
        user_delete,
        user_upsert,
        user_view,
    )

    app.add_url_rule("/", "index", index)
    app.add_url_rule("/users/<int:user_id>", "user_view", user_view)
    app.add_url_rule(
        "/users/create", "user_create", user_upsert, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/users/<int:user_id>/edit",
        "user_edit",
        user_upsert,
        methods=["GET", "POST"],
    )
    app.add_url_rule("/users/<int:user_id>/delete", "user_delete", user_delete)
