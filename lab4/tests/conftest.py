from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING

import pytest
from flask import template_rendered
from sqlalchemy.orm import scoped_session

from lab4.app import app as application
from lab4.user.accessor import UserAccessor
from lab4.user.models import Role, User

if TYPE_CHECKING:
    from lab4.app import Application


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
def client(app, app_context, test_user):
    with app.test_client() as client:
        yield client


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
def test_role(user_accessor, db_session) -> Role:
    return user_accessor.create_role(
        {"name": "Test Role", "description": "Role for testing"}
    )


@pytest.fixture
def test_roles(user_accessor, db_session) -> list[Role]:
    user_accessor.create_role(
        {"name": "Test Role 1", "description": "Role 1 for testing"}
    )
    user_accessor.create_role(
        {"name": "Test Role 2", "description": "Role 2 for testing"}
    )

    return user_accessor.get_roles()


@pytest.fixture
def test_user(user_accessor: UserAccessor, test_role: Role, db_session) -> User:
    return user_accessor.create_user(
        {
            "login": "testuser",
            "password": user_accessor.hash_password("password123"),
            "last_name": "Test",
            "first_name": "User",
            "middle_name": "Middle",
            "role_id": test_role.id,
        }
    )


@pytest.fixture
def test_users(
    user_accessor: UserAccessor, test_roles: Role, db_session
) -> list[User]:
    user_accessor.create_user(
        {
            "login": "1testuser",
            "password": user_accessor.hash_password("password123"),
            "last_name": "Test 1",
            "first_name": "User",
            "middle_name": "Middle",
            "role_id": test_role.id,
        }
    )
    user_accessor.create_user(
        {
            "login": "2testuser",
            "password": user_accessor.hash_password("password123"),
            "last_name": "Test 2",
            "first_name": "User",
            "middle_name": "Middle",
            "role_id": test_role.id,
        }
    )

    return user_accessor.get_users()


@pytest.fixture
def authenticated_client(client):
    client.post(
        "/login",
        data={
            "login": "testuser",
            "password": "password123",
            "remember_me": "on",
        },
    )
    return client
