from typing import TYPE_CHECKING

from lab5.auth.rights import check_rights

if TYPE_CHECKING:
    from .app import Application


def setup_context_processor(app: "Application"):
    @app.context_processor
    def utility_processor():
        return {"check_rights": check_rights}
