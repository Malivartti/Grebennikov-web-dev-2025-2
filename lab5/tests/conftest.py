from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING

import pytest
from flask import template_rendered
from sqlalchemy.orm import scoped_session

from lab5.app import app as application
from lab5.user.accessor import UserAccessor
from lab5.user.models import Role, User
from lab5.visit.accessor import VisitAccessor

if TYPE_CHECKING:
    from lab5.app import Application


def pytest_configure(config):
    config.addinivalue_line(
        "filterwarnings", "ignore::pytest.PytestConfigWarning"
    )


@pytest.fixture
def app() -> "Generator[Application]":
    origin_session_cookie_path = application.config.get("SESSION_COOKIE_PATH")
    origin_remember_cookie_path = application.config.get("REMEMBER_COOKIE_PATH")

    application.config.update(
        {
            "TESTING": True,
            "SESSION_COOKIE_PATH": "/",
            "REMEMBER_COOKIE_PATH": "/",
        }
    )

    yield application

    application.config["TESTING"] = False
    application.config["SESSION_COOKIE_PATH"] = origin_session_cookie_path
    application.config["REMEMBER_COOKIE_PATH"] = origin_remember_cookie_path


@pytest.fixture
def app_context(app: "Application"):
    with app.app_context():
        yield


@pytest.fixture
def db_connection(app: "Application", app_context):
    connection = app.db.engine.connect()
    yield connection
    connection.close()


@pytest.fixture
def db_session(app: "Application", app_context, db_connection):
    transaction = db_connection.begin()

    session_factory = app.db.sessionmaker(bind=db_connection)
    session = scoped_session(session_factory)

    original_session = app.db.session
    app.db.session = session

    yield session

    session.close()
    transaction.rollback()

    app.db.session = original_session


@pytest.fixture
@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def user_accessor(app: "Application", app_context) -> UserAccessor:
    return app.store.user


@pytest.fixture
def visit_accessor(app: "Application", app_context) -> VisitAccessor:
    return app.store.visit


@pytest.fixture
def admin_role(user_accessor, db_session) -> Role:
    admin_role = user_accessor.get_role_by_name("Администратор")
    if admin_role:
        return admin_role

    return user_accessor.create_role(
        {"name": "Администратор", "description": "Администратор"}
    )


@pytest.fixture
def ordinary_role(user_accessor, db_session) -> Role:
    admin_role = user_accessor.get_role_by_name("Пользователь")
    if admin_role:
        return admin_role

    return user_accessor.create_role(
        {"name": "Пользователь", "description": "Пользователь"}
    )


@pytest.fixture
def admin_user(
    user_accessor: UserAccessor, admin_role: Role, db_session
) -> User:
    return user_accessor.create_user(
        {
            "login": "test-admin",
            "password": user_accessor.hash_password("password123"),
            "last_name": "Admin",
            "first_name": "User",
            "role_id": admin_role.id,
        }
    )


@pytest.fixture
def ordinary_user(
    user_accessor: UserAccessor, ordinary_role: Role, db_session
) -> User:
    return user_accessor.create_user(
        {
            "login": "test-ordinary",
            "password": user_accessor.hash_password("password123"),
            "last_name": "Ordinary",
            "first_name": "User",
            "role_id": ordinary_role.id,
        }
    )


@pytest.fixture
def no_role_user(
    user_accessor: UserAccessor, ordinary_role: Role, db_session
) -> User:
    return user_accessor.create_user(
        {
            "login": "no-role",
            "password": user_accessor.hash_password("password123"),
            "last_name": "No role",
            "first_name": "User",
            "role_id": None,
        }
    )


@pytest.fixture
def client(app, app_context):
    with app.test_client() as client:
        yield client


@pytest.fixture
def admin_client(client, admin_user: User):
    client.post(
        "/login",
        data={
            "login": admin_user.login,
            "password": "password123",
            "remember_me": "on",
        },
    )
    return client


@pytest.fixture
def ordinary_client(client, ordinary_user: User):
    client.post(
        "/login",
        data={
            "login": ordinary_user.login,
            "password": "password123",
            "remember_me": "on",
        },
    )
    return client
