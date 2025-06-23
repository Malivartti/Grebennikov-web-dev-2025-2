from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for,
)

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return redirect(url_for("animal.index"))


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
