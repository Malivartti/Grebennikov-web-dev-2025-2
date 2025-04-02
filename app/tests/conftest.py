from datetime import datetime
import pytest
from flask import template_rendered
from contextlib import contextmanager
from app.app import application

@pytest.fixture
def app():
    return application

@pytest.fixture
def client(app):
    return app.test_client()

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
def posts_list():
    return [
        {
            'title': 'Заголовок поста',
            'text': 'Текст поста',
            'author': 'Иванов Иван Иванович',
            'date': datetime(2025, 3, 10),
            'image_id': '123.jpg',
            'comments': []
        }
    ]

@pytest.fixture
def posts_list_with_comments():
    return [
        {
            'title': 'Заголовок поста',
            'text': 'Текст поста',
            'author': 'Иванов Иван Иванович',
            'date': datetime(2025, 3, 10),
            'image_id': '123.jpg',
            'comments': [
                {
                    'author': 'Кристофер Васкес',
                    'text': 'Отнесите их домой.',
                    'replies': [
                        {
                            'author': 'Мэри Кеннеди',
                            'text': 'Когда-нибудь отвезу ее позже на перерыв.',
                        }
                    ]
                }
            ]
        }
    ]