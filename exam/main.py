from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
