import csv
import io

from flask import (
    Blueprint,
    Response,
    render_template,
    request,
)
from flask_login import current_user, login_required

from lab5.app import app
from lab5.auth.rights import check_rights

visit_bp = Blueprint("visits", __name__, url_prefix="/visits")


@visit_bp.route("/")
@login_required
@check_rights(["view_all_visits", "view_own_visits"])
def index():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if per_page not in [10, 30, 50]:
        per_page = 10

    user_id = None if current_user.is_admin else current_user.id

    logs, pagination = app.store.visit.get_visits(
        page=page, per_page=per_page, user_id=user_id
    )

    return render_template(
        "visits.html",
        logs=logs,
        pagination=pagination,
        is_admin=current_user.is_admin,
        per_page=per_page,
    )


@visit_bp.route("/pages")
@login_required
@check_rights(["view_all_visits"])
def pages_report():
    pages_stats = app.store.visit.get_page_stats()

    return render_template("pages_report.html", pages_stats=pages_stats)


@visit_bp.route("/users")
@login_required
@check_rights(["view_all_visits"])
def users_report():
    users_stats = app.store.visit.get_user_stats()

    return render_template("users_report.html", users_stats=users_stats)


@visit_bp.route("/export/pages")
@login_required
@check_rights(["view_all_visits"])
def export_pages():
    pages_stats = app.store.visit.get_page_stats()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["№", "Страница", "Количество посещений"])
    for idx, (path, count) in enumerate(pages_stats, 1):
        writer.writerow([idx, path, count])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=pages_report.csv"},
    )


@visit_bp.route("/export/users")
@login_required
@check_rights(["view_all_visits"])
def export_users():
    users_stats = app.store.visit.get_user_stats()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["№", "Пользователь", "Количество посещений"])

    for idx, (user_id, last_name, first_name, middle_name, count) in enumerate(
        users_stats, 1
    ):
        if user_id:
            full_name = f"{last_name} {first_name}" + (middle_name or "")
            writer.writerow([idx, full_name, count])
        else:
            writer.writerow([idx, "Неаутентифицированный пользователь", count])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=users_report.csv"},
    )
