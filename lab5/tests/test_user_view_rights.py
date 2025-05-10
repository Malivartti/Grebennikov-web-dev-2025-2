def test_create_user_admin_client(captured_templates, admin_client):
    with captured_templates as templates:
        response = admin_client.get("/users/create", follow_redirects=True)
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "user_upsert.html"


def test_create_user_ordinary_client(captured_templates, ordinary_client):
    with captured_templates as templates:
        response = ordinary_client.get("/users/create", follow_redirects=True)
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "У вас недостаточно прав доступа." in response.text


def test_create_user_anonymous_client(captured_templates, client):
    with captured_templates as templates:
        response = client.get("/users/create", follow_redirects=True)
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "auth.html"
        assert (
            "Для доступа к данной странице "
            "необходимо пройти процедуру аутентификации" in response.text
        )


def test_view_self_admin_client(captured_templates, admin_client, admin_user):
    with captured_templates as templates:
        response = admin_client.get(
            f"/users/{admin_user.id}", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "user_view.html"


def test_view_self_ordinary_client(
    captured_templates, ordinary_client, ordinary_user
):
    with captured_templates as templates:
        response = ordinary_client.get(
            f"/users/{ordinary_user.id}", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "user_view.html"


def test_view_any_user_admin_client(
    captured_templates, admin_client, ordinary_user
):
    with captured_templates as templates:
        response = admin_client.get(
            f"/users/{ordinary_user.id}", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "user_view.html"


def test_view_any_user_ordinary_client(
    captured_templates, ordinary_client, admin_user
):
    with captured_templates as templates:
        response = ordinary_client.get(
            f"/users/{admin_user.id}", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "У вас недостаточно прав доступа." in response.text


def test_view_any_user_anonymous_client(
    captured_templates, client, ordinary_user
):
    with captured_templates as templates:
        response = client.get(
            f"/users/{ordinary_user.id}", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "auth.html"
        assert (
            "Для доступа к данной странице "
            "необходимо пройти процедуру аутентификации" in response.text
        )


def test_edit_self_admin_client(captured_templates, admin_client, admin_user):
    with captured_templates as templates:
        response = admin_client.get(
            f"/users/{admin_user.id}/edit", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "user_upsert.html"
        assert (
            'select class="form-select" id="role_id" name="role_id" disabled'
            not in response.text
        )


def test_edit_self_ordinary_client(
    captured_templates, ordinary_client, ordinary_user
):
    with captured_templates as templates:
        response = ordinary_client.get(
            f"/users/{ordinary_user.id}/edit", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "user_upsert.html"
        assert (
            'select class="form-select" id="role_id" name="role_id" disabled'
            in response.text
        )


def test_edit_any_user_admin_client(
    captured_templates, admin_client, ordinary_user
):
    with captured_templates as templates:
        response = admin_client.get(
            f"/users/{ordinary_user.id}/edit", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "user_upsert.html"


def test_edit_any_user_ordinary_client(
    captured_templates, ordinary_client, admin_user
):
    with captured_templates as templates:
        response = ordinary_client.get(
            f"/users/{admin_user.id}/edit", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "У вас недостаточно прав доступа." in response.text


def test_edit_any_user_anonymous_client(
    captured_templates, client, ordinary_user
):
    with captured_templates as templates:
        response = client.get(
            f"/users/{ordinary_user.id}/edit", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "auth.html"
        assert (
            "Для доступа к данной странице "
            "необходимо пройти процедуру аутентификации" in response.text
        )


def test_delete_any_user_admin_client(
    captured_templates, admin_client, ordinary_user
):
    with captured_templates as templates:
        response = admin_client.get(
            f"/users/{ordinary_user.id}/delete", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"


def test_delete_any_user_ordinary_client(
    captured_templates, ordinary_client, admin_user
):
    with captured_templates as templates:
        response = ordinary_client.get(
            f"/users/{admin_user.id}/delete", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "У вас недостаточно прав доступа." in response.text


def test_delete_any_user_anonymous_client(
    captured_templates, client, ordinary_user
):
    with captured_templates as templates:
        response = client.get(
            f"/users/{ordinary_user.id}/delete", follow_redirects=True
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "auth.html"
        assert (
            "Для доступа к данной странице "
            "необходимо пройти процедуру аутентификации" in response.text
        )
