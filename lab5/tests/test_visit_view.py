import csv
from io import StringIO


def test_index_admin_client(admin_client, admin_user):
    admin_client.get(f"/users/{admin_user.id}")

    response = admin_client.get("/visits/", follow_redirects=True)

    assert response.status_code == 200
    assert f"{admin_user.first_name} {admin_user.last_name}" in response.text


def test_index_ordinary_client(ordinary_client, ordinary_user):
    ordinary_client.get(f"/users/{ordinary_user.id}")

    response = ordinary_client.get("/visits/", follow_redirects=True)

    assert response.status_code == 200
    assert (
        f"{ordinary_user.first_name} {ordinary_user.last_name}" in response.text
    )


def test_pages_report_admin_client(captured_templates, admin_client):
    with captured_templates as templates:
        response = admin_client.get("/visits/pages", follow_redirects=True)
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "pages_report.html"


def test_pages_report_regular_client(captured_templates, ordinary_client):
    with captured_templates as templates:
        response = ordinary_client.get("/visits/pages", follow_redirects=True)
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "У вас недостаточно прав доступа." in response.text


def test_users_report_admin_client(captured_templates, admin_client):
    with captured_templates as templates:
        response = admin_client.get("/visits/users", follow_redirects=True)
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "users_report.html"


def test_users_report_ordinary_client(captured_templates, ordinary_client):
    with captured_templates as templates:
        response = ordinary_client.get("/visits/users", follow_redirects=True)
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "У вас недостаточно прав доступа." in response.text


def test_export_pages_admin_client(admin_client, monkeypatch, visit_accessor):
    def mock_get_page_stats(*args, **kwargs):
        return [("/home", 100), ("/about", 50), ("/contact", 25)]

    monkeypatch.setattr(visit_accessor, "get_page_stats", mock_get_page_stats)

    response = admin_client.get("/visits/export/pages", follow_redirects=True)

    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment;filename=pages_report.csv"
    )

    content = response.data.decode("utf-8")
    csv_reader = csv.reader(StringIO(content))
    rows = list(csv_reader)

    assert rows[0] == ["№", "Страница", "Количество посещений"]

    assert rows[1] == ["1", "/home", "100"]
    assert rows[2] == ["2", "/about", "50"]
    assert rows[3] == ["3", "/contact", "25"]

    assert len(rows) == 4


def test_export_pages_ordinary_client(captured_templates, ordinary_client):
    with captured_templates as templates:
        response = ordinary_client.get(
            "/visits/export/pages", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "У вас недостаточно прав доступа." in response.text


def test_export_users_admin_client(admin_client, monkeypatch, visit_accessor):
    def mock_get_user_stats(*args, **kwargs):
        return [
            (1, "Иванов", "Иван", "Иванович", 150),
            (2, "Петров", "Петр", "Петрович", 75),
            (None, None, None, None, 200),
        ]

    monkeypatch.setattr(visit_accessor, "get_user_stats", mock_get_user_stats)

    response = admin_client.get("/visits/export/users", follow_redirects=True)

    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment;filename=users_report.csv"
    )

    content = response.data.decode("utf-8")
    csv_reader = csv.reader(StringIO(content))
    rows = list(csv_reader)

    assert rows[0] == ["№", "Пользователь", "Количество посещений"]

    assert rows[1] == ["1", "Иванов ИванИванович", "150"]
    assert rows[2] == ["2", "Петров ПетрПетрович", "75"]
    assert rows[3] == ["3", "Неаутентифицированный пользователь", "200"]

    assert len(rows) == 4


def test_export_users_ordinary_client(captured_templates, ordinary_client):
    with captured_templates as templates:
        response = ordinary_client.get(
            "/visits/export/users", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "У вас недостаточно прав доступа." in response.text
