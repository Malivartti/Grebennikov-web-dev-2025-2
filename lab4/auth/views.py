from urllib.parse import urlparse

from flask import flash, redirect, render_template, request, url_for
from flask_login import (
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from lab4.app import app
from lab4.user.models import User as UserModel
from lab4.user.validate import validate_password


class User(UserMixin):
    def __init__(self, user: UserModel):
        self.id = user.id
        self.login = user.login
        self.is_admin = user.role == "Администратор"


@app.login_manager.user_loader
def load_user(user_id):
    user = app.store.user.get_user_by_id(int(user_id))
    if user:
        return User(user)
    return None


def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me") == "on"

        if login and password:
            user = app.store.user.get_user_by_login(login)
            if user and app.store.user.verify_password(password, user.password):
                user = User(user)
                login_user(user, remember=remember_me)
                flash("Вы успешно аутентифицированны", "success")

                next_page = request.args.get("next")
                if next_page:
                    parsed = urlparse(next_page)
                    if parsed.scheme or parsed.netloc:
                        return redirect(url_for("index"))
                    return redirect(next_page)
                return redirect(url_for("index"))
            flash("Неверный логин или пароль", "danger")
            return render_template("auth.html")

    return render_template("auth.html")


def logout():
    logout_user()
    return redirect(url_for("index"))


@login_required
def change_password():
    errors = {}
    form_data = {}

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        form_data = {
            "old_password": old_password,
            "new_password": new_password,
            "confirm_password": confirm_password,
        }

        user = app.store.user.get_user_by_id(current_user.id)

        if not old_password:
            errors["old_password"] = "Поле не может быть пустым"
        elif not app.store.user.verify_password(old_password, user.password):
            errors["old_password"] = "Старый пароль введён неверно"

        password_error = validate_password(new_password)
        if password_error:
            errors["new_password"] = password_error

        if not confirm_password:
            errors["confirm_password"] = "Поле не может быть пустым"
        elif new_password != confirm_password:
            errors["confirm_password"] = "Пароли не совпадают"

        if not errors:
            try:
                hashed_password = app.store.user.hash_password(new_password)

                app.store.user.update_user(
                    current_user.id, {"password": hashed_password}
                )

                flash("Пароль успешно изменён", "success")
                return redirect(url_for("index"))
            except Exception as err:
                flash(str(err), "danger")

    return render_template(
        "change_password.html", errors=errors, form_data=form_data
    )
