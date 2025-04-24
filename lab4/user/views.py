from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from lab4.app import app
from lab4.user.validate import (
    validate_login,
    validate_password,
    validate_required_field,
)


def index():
    users = app.store.user.get_users()

    for user in users:
        user.full_name = (
            f"{user.last_name or ''} "
            f"{user.first_name} {user.middle_name or ''}"
        ).strip()

    return render_template(
        "index.html",
        users=users,
        is_authenticated=current_user.is_authenticated,
    )


def user_view(user_id):
    user = app.store.user.get_user_by_id(user_id)
    if not user:
        flash("Пользователь не найден", "danger")
        return redirect(url_for("index"))

    return render_template("user_view.html", user=user)


@login_required
def user_upsert(user_id: int | None = None):  # noqa: C901, PLR0912
    user = None
    if user_id:
        user = app.store.user.get_user_by_id(user_id)
        if not user:
            flash("Пользователь не найден", "danger")
            return redirect(url_for("index"))

    roles = app.store.user.get_roles()

    if request.method == "POST":
        form_data = {
            "last_name": request.form.get("last_name"),
            "first_name": request.form.get("first_name"),
            "middle_name": request.form.get("middle_name"),
            "role_id": request.form.get("role_id"),
        }

        errors = {}
        if not user_id:
            form_data["login"] = request.form.get("login")
            form_data["password"] = request.form.get("password")

            login_error = validate_login(request.form.get("login"))
            if login_error:
                errors["login"] = login_error

            password_error = validate_password(request.form.get("password"))
            if password_error:
                errors["password"] = password_error

        for field in ["last_name", "first_name"]:
            error = validate_required_field(request.form.get(field), field)
            if error:
                errors[field] = error

        if errors:
            return render_template(
                "user_upsert.html",
                user=user,
                form_data=form_data,
                roles=roles,
                errors=errors,
            )

        if form_data["role_id"]:
            form_data["role_id"] = int(form_data["role_id"])
        else:
            form_data["role_id"] = None

        try:
            if user:  # Редактирование существующего пользователя
                app.store.user.update_user(user_id, form_data)
                flash("Данные пользователя успешно обновлены", "success")
            else:  # Создание нового пользователя
                login = request.form.get("login")
                password = request.form.get("password")

                existing_user = app.store.user.get_user_by_login(login)
                if existing_user:
                    flash(
                        "Пользователь с таким логином уже существует", "danger"
                    )
                    return render_template(
                        "user_upsert.html",
                        user=user,
                        form_data=request.form,
                        roles=roles,
                    )

                form_data["password"] = app.store.user.hash_password(password)

                app.store.user.create_user(form_data)
                flash("Пользователь успешно создан", "success")

        except (
            Exception
        ) as err:  # Если не удалось создать, обновить пользователя
            flash(str(err), "danger")
            return render_template(
                "user_upsert.html",
                user=user,
                form_data=request.form,
                roles=roles,
            )

        return redirect(url_for("index"))

    return render_template("user_upsert.html", user=user, roles=roles)


@login_required
def user_delete(user_id: int):
    try:
        app.store.user.delete_user(user_id)
        flash("Пользователь успешно удален", "success")
    except Exception as err:
        flash(str(err), "danger")

    return redirect(url_for("index"))
