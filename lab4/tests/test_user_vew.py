def test_user_view_success(client, captured_templates, test_user):
    with captured_templates as templates:
        response = client.get(f"/users/{test_user.id}")

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]

        assert template.name == "user_view.html"
        assert "user" in context
        assert context["user"].id == test_user.id


def test_user_view_not_found(client, captured_templates, test_user):
    with captured_templates as templates:
        response = client.get(
            f"/users/{test_user.id + 1}", follow_redirects=True
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "Пользователь не найден" in response.text


def test_user_upsert_get_new(authenticated_client, captured_templates):
    with captured_templates as templates:
        response = authenticated_client.get("/users/create")

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]

        assert template.name == "user_upsert.html"
        assert context["user"] is None
        assert "roles" in context


def test_user_upsert_get_edit(
    authenticated_client, captured_templates, test_user
):
    with captured_templates as templates:
        response = authenticated_client.get(f"/users/{test_user.id}/edit")

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]

        assert template.name == "user_upsert.html"
        assert context["user"] is not None
        assert context["user"].id == test_user.id
        assert "roles" in context


def test_user_upsert_get_edit_not_found(
    authenticated_client, captured_templates, test_user
):
    with captured_templates as templates:
        response = authenticated_client.get(
            f"/users/{test_user.id + 1}/edit", follow_redirects=True
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "Пользователь не найден" in response.text


def test_user_upsert_post_create_success(
    authenticated_client, captured_templates, user_accessor, test_role
):
    with captured_templates as templates:
        login = "newuser"
        response = authenticated_client.post(
            "/users/create",
            data={
                "login": login,
                "password": "Password123",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "middle_name": "Отчество",
                "role_id": test_role.id,
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "Пользователь успешно создан" in response.text

        assert user_accessor.get_user_by_login(login) is not None


def test_user_upsert_post_create_duplicate_login(
    authenticated_client, captured_templates, test_user, test_role
):
    with captured_templates as templates:
        response = authenticated_client.post(
            "/users/create",
            data={
                "login": test_user.login,
                "password": "Password123",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "middle_name": "Отчество",
                "role_id": test_role.id,
            },
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "user_upsert.html"
        assert "Пользователь с таким логином уже существует" in response.text


def test_user_upsert_post_create_validation_errors(
    authenticated_client, captured_templates, user_accessor, test_role
):
    with captured_templates as templates:
        login = "us"
        response = authenticated_client.post(
            "/users/create",
            data={
                "login": login,
                "password": "weak",
                "last_name": "",
                "first_name": "",
                "role_id": test_role.id,
            },
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]

        assert template.name == "user_upsert.html"
        assert "errors" in context
        assert "login" in context["errors"]
        assert (
            context["errors"]["login"]
            == "Логин должен содержать не менее 5 символов"
        )
        assert "password" in context["errors"]
        assert "last_name" in context["errors"]
        assert context["errors"]["last_name"] == "Поле не может быть пустым"
        assert "first_name" in context["errors"]
        assert context["errors"]["first_name"] == "Поле не может быть пустым"

        assert user_accessor.get_user_by_login(login) is None


def test_user_upsert_post_edit_success(
    authenticated_client, captured_templates, test_user, user_accessor
):
    with captured_templates as templates:
        new_last_name = "Новая Фамилия"
        new_first_name = "Новое Имя"
        response = authenticated_client.post(
            f"/users/{test_user.id}/edit",
            data={
                "last_name": new_last_name,
                "first_name": new_first_name,
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "Данные пользователя успешно обновлены" in response.text

        user = user_accessor.get_user_by_id(test_user.id)
        assert user.last_name == new_last_name
        assert user.first_name == new_first_name


def test_user_upsert_post_edit_validation_errors(
    authenticated_client, captured_templates, test_user, user_accessor, test_role
):
    with captured_templates as templates:
        new_last_name = ""
        new_first_name = ""
        response = authenticated_client.post(
            f"/users/{test_user.id}/edit",
            data={
                "last_name": new_last_name,
                "first_name": new_first_name,
                "role_id": test_role.id,
            },
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]

        assert template.name == "user_upsert.html"
        assert "errors" in context
        assert "last_name" in context["errors"]
        assert "first_name" in context["errors"]

        user = user_accessor.get_user_by_id(test_user.id)
        assert user.last_name != new_last_name
        assert user.first_name != new_first_name


def test_user_delete_success(
    authenticated_client, captured_templates, user_accessor, test_user
):
    with captured_templates as templates:
        response = authenticated_client.get(
            f"/users/{test_user.id}/delete", follow_redirects=True
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "Пользователь успешно удален" in response.text

        assert user_accessor.get_user_by_id(test_user.id) is None


def test_user_delete_error(
    authenticated_client,
    captured_templates,
    monkeypatch,
    user_accessor,
    test_user,
):
    def mock_delete_user(user_id):
        raise Exception("Ошибка при удалении пользователя")

    monkeypatch.setattr(
        user_accessor,
        "delete_user",
        mock_delete_user,
    )

    with captured_templates as templates:
        response = authenticated_client.get(
            f"/users/{test_user.id}/delete", follow_redirects=True
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]

        assert template.name == "index.html"
        assert "Ошибка при удалении пользователя" in response.text

        assert user_accessor.get_user_by_id(test_user.id) is not None


def test_user_upsert_requires_authentication(client, test_user):
    response = client.get("/users/create", follow_redirects=True)

    assert response.status_code == 200
    assert (
        "Для доступа к данной странице необходимо "
        "пройти процедуру аутентификации" in response.text
    )

    response = client.get(f"/users/{test_user.id}/edit", follow_redirects=True)

    assert response.status_code == 200
    assert (
        "Для доступа к данной странице необходимо "
        "пройти процедуру аутентификации" in response.text
    )


def test_user_delete_requires_authentication(client, test_user):
    response = client.get(
        f"/users/{test_user.id}/delete", follow_redirects=True
    )

    assert response.status_code == 200
    assert (
        "Для доступа к данной странице необходимо "
        "пройти процедуру аутентификации" in response.text
    )
