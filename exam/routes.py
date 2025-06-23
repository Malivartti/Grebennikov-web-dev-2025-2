from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from exam.app import Application


def setup_routes(app: "Application"):
    import exam.animal.views
    import exam.auth
    import exam.main

    app.register_blueprint(exam.main.bp)
    app.register_blueprint(exam.auth.bp)
    app.register_blueprint(exam.animal.views.bp)
