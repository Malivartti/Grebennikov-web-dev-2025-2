import pytest
from flask import Response
from flask_login import login_user

from lab5.auth.rights import check_rights
from lab5.auth.views import User


@pytest.mark.parametrize(
    "right",
    [
        "create_user",
        "edit_user",
        "view_user",
        "delete_user",
        "view_all_visits",
    ],
)
def test_admin_user_rights(app, admin_user, right):
    with app.test_request_context():
        login_user(User(admin_user))

        @check_rights([right])
        def admin_function():
            return "success"

        result = admin_function()
        assert result == "success"


@pytest.mark.parametrize("right", ["edit_self", "view_self", "view_own_visits"])
def test_ordinary_user_rights(app, ordinary_user, right):
    with app.test_request_context(f"/users/{ordinary_user.id}"):
        login_user(User(ordinary_user))

        @check_rights([right])
        def user_function():
            return "success"

        result = user_function()
        assert result == "success"


@pytest.mark.parametrize("right", ["edit_self", "view_self", "view_own_visits"])
def test_no_role_user_rights(app, no_role_user, right):
    with app.test_request_context(f"/users/{no_role_user.id}"):
        login_user(User(no_role_user))

        @check_rights([right])
        def user_function():
            return "success"

        result = user_function()
        assert result == "success"


def test_user_without_permission(app, ordinary_user):
    with app.test_request_context():
        login_user(User(ordinary_user))

        @check_rights(["view_user"])
        def user_function():
            return "success"

        result = user_function()
        assert isinstance(result, Response)
        assert result.status_code == 302


def test_user_without_auth(app):
    with app.test_request_context():

        @check_rights(["view_user"])
        def anonim_function():
            return "success"

        result = anonim_function()
        assert isinstance(result, Response)
        assert result.status_code == 302
