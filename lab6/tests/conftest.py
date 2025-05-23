import os
from contextlib import contextmanager
from io import BytesIO

import pytest
from flask import template_rendered, url_for
from sqlalchemy.orm import scoped_session

from lab6.app import create_app
from lab6.app.models import Category, Course, Image, Review, User, db
from lab6.app.repositories.category_repository import CategoryRepository
from lab6.app.repositories.course_repository import CourseRepository
from lab6.app.repositories.image_repository import ImageRepository
from lab6.app.repositories.review_repository import ReviewRepository


def pytest_configure(config):
    config.addinivalue_line(
        "filterwarnings", "ignore::pytest.PytestConfigWarning"
    )


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        {
            "TESTING": True,
            "SESSION_COOKIE_PATH": "/",
            "REMEMBER_COOKIE_PATH": "/",
        }
    )

    return app


@pytest.fixture
def app_db():
    return db


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def db_connection(app, app_context, app_db):
    connection = app_db.engine.connect()
    yield connection
    connection.close()


@pytest.fixture
def db_session(app, app_context, app_db, db_connection):
    transaction = db_connection.begin()

    session_factory = app_db.sessionmaker(bind=db_connection)
    session = scoped_session(session_factory)

    original_session = app_db.session
    app_db.session = session

    yield session

    session.close()
    transaction.rollback()

    app_db.session = original_session


@pytest.fixture
@contextmanager
def captured_templates(app, app_context):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def category_repository(app_db) -> CategoryRepository:
    return CategoryRepository(app_db)


@pytest.fixture
def image_repository(app_db) -> ImageRepository:
    return ImageRepository(app_db)


@pytest.fixture
def course_repository(app_db) -> CourseRepository:
    return CourseRepository(app_db)


@pytest.fixture
def review_repository(app_db) -> ReviewRepository:
    return ReviewRepository(app_db)


@pytest.fixture
def test_user(db_session, app_db) -> User:
    user = User(first_name="Test", last_name="User", login="test-user")
    user.set_password("password123")
    app_db.session.add(user)
    app_db.session.commit()
    return user


@pytest.fixture
def test_user2(db_session, app_db) -> User:
    user = User(first_name="Test 2", last_name="User", login="test-user-2")
    user.set_password("password123")
    app_db.session.add(user)
    app_db.session.commit()
    return user


@pytest.fixture
def test_category(db_session, app_db) -> Category:
    category = Category(name="Test Category")
    app_db.session.add(category)
    app_db.session.commit()
    return category


@pytest.fixture
def test_image(app, image_repository: "ImageRepository", db_session) -> Image:
    class MockFile:
        def __init__(self, content, filename, mimetype):
            self.stream = BytesIO(content)
            self.filename = filename
            self.mimetype = mimetype

        def read(self):
            return self.stream.getvalue()

        def seek(self, offset):
            self.stream.seek(offset)

        def save(self, path):
            with open(path, "wb") as f:
                f.write(self.read())

    mock_file = MockFile(
        content=b"test image content",
        filename="test_image.jpg",
        mimetype="image/jpeg",
    )

    img = image_repository.add_image(mock_file)
    yield img

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], img.storage_filename)
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def test_course(
    course_repository: "CourseRepository",
    test_user,
    test_category,
    test_image,
    db_session,
) -> Course:
    return course_repository.add_course(
        author_id=test_user.id,
        name="Test Course",
        category_id=test_category.id,
        short_desc="Description Course",
        full_desc="Full Description Course",
        background_image_id=test_image.id,
    )


@pytest.fixture
def test_review(
    review_repository: "ReviewRepository", test_user, test_course, db_session
) -> Review:
    return review_repository.create(
        user_id=test_user.id,
        course_id=test_course.id,
        rating=1,
        text="Bad Course",
    )


@pytest.fixture
def multiple_reviews(
    review_repository: "ReviewRepository", test_user, test_course, db_session
) -> list[Review]:
    ratings = [5, 2, 4, 1, 3, 0]
    texts = [
        "Excellent",
        "Unsatisfactory",
        "Good",
        "Bad",
        "Satisfactory",
        "Terrible",
    ]

    return [
        review_repository.create(
            user_id=test_user.id,
            course_id=test_course.id,
            rating=ratings[i],
            text=texts[i],
        )
        for i in range(len(ratings))
    ]


@pytest.fixture
def client(app, app_context):
    with app.test_request_context(), app.test_client() as client:
        yield client


@pytest.fixture
def test_client(client, test_user):
    client.post(
        url_for("auth.login"),
        data={
            "login": test_user.login,
            "password": "password123",
            "remember_me": "on",
        },
    )

    return client


@pytest.fixture
def test_client2(client, test_user2):
    client.post(
        url_for("auth.login"),
        data={
            "login": test_user2.login,
            "password": "password123",
            "remember_me": "on",
        },
    )

    return client
