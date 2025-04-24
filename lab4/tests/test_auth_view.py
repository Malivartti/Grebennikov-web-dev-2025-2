import pytest


def test_successful_login(client, captured_templates):
    with captured_templates as templates:
        response = client.post(
            "/login",
            data={
                "login": "testuser",
                "password": "password123",
                "remember_me": "on",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == "index.html"
        assert "success" in response.text


def test_successful_login_redirects_to_index(client):
    response = client.post(
        "/login",
        data={
            "login": "testuser",
            "password": "password123",
            "remember_me": "on",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.location == "/"


def test_failed_login_shows_error(client, captured_templates):
    with captured_templates as templates:
        response = client.post(
            "/login",
            data={"login": "user", "password": "wrong", "remember_me": "on"},
        )
        assert response.status_code == 200

        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == "auth.html"
        assert "Неверный логин или пароль" in response.text


def test_remember_me_sets_cookie(authenticated_client):
    response = authenticated_client.get("/")
    assert "Set-Cookie" in response.headers
    assert "session" in response.headers["Set-Cookie"]


def test_navbar_links_unauthenticated(client):
    response = client.get("/")
    assert response.status_code == 200

    assert 'href="/login"' in response.text
    assert 'href="/change_password"' not in response.text
    assert 'href="/logout"' not in response.text


def test_navbar_links_authenticated(authenticated_client):
    response = authenticated_client.get("/")
    assert response.status_code == 200

    assert 'href="/login"' not in response.text
    assert 'href="/change_password"' in response.text
    assert 'href="/logout"' in response.text


def test_logout_redirects_to_index(authenticated_client, captured_templates):
    with captured_templates as templates:
        response = authenticated_client.get("/logout", follow_redirects=True)
        assert response.status_code == 200

        assert len(templates) == 1
        assert templates[0][0].name == "index.html"

        response = authenticated_client.get("/")
        assert 'href="/change_password"' not in response.text


def test_change_password_get_request(authenticated_client, captured_templates):
    with captured_templates as templates:
        response = authenticated_client.get("/change_password")

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]

        assert template.name == "change_password.html"
        assert "errors" in context
        assert "form_data" in context
        assert not context["errors"]


def test_change_password_unauthenticated(client):
    response = client.get("/change_password", follow_redirects=True)

    assert response.status_code == 200
    assert "login" in response.request.path


def test_change_password_success(
    authenticated_client, test_user, user_accessor
):
    old_password_hash = test_user.password

    response = authenticated_client.post(
        "/change_password",
        data={
            "old_password": "password123",
            "new_password": "NewPassword123",
            "confirm_password": "NewPassword123",
        },
        follow_redirects=True,
    )

    updated_user = user_accessor.get_user_by_id(test_user.id)
    assert updated_user.password != old_password_hash
    assert user_accessor.verify_password(
        "NewPassword123", updated_user.password
    )

    assert response.status_code == 200
    assert "Пароль успешно изменён" in response.text


def test_change_password_wrong_old_password(
    authenticated_client, captured_templates
):
    with captured_templates as templates:
        response = authenticated_client.post(
            "/change_password",
            data={
                "old_password": "WrongPassword123",
                "new_password": "NewPassword123",
                "confirm_password": "NewPassword123",
            },
        )

        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == "change_password.html"
        assert "errors" in context
        assert "old_password" in context["errors"]
        assert (
            context["errors"]["old_password"] == "Старый пароль введён неверно"
        )


def test_change_password_empty_fields(authenticated_client, captured_templates):
    with captured_templates as templates:
        response = authenticated_client.post(
            "/change_password",
            data={
                "old_password": "",
                "new_password": "",
                "confirm_password": "",
            },
        )

        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == "change_password.html"
        assert "errors" in context
        assert "old_password" in context["errors"]
        assert "new_password" in context["errors"]
        assert "confirm_password" in context["errors"]
        assert context["errors"]["old_password"] == "Поле не может быть пустым"
        assert context["errors"]["new_password"] == "Поле не может быть пустым"
        assert (
            context["errors"]["confirm_password"] == "Поле не может быть пустым"
        )


def test_change_password_passwords_do_not_match(
    authenticated_client, captured_templates
):
    with captured_templates as templates:
        response = authenticated_client.post(
            "/change_password",
            data={
                "old_password": "password123",
                "new_password": "NewPassword123",
                "confirm_password": "DifferentPassword123",
            },
        )

        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == "change_password.html"
        assert "errors" in context
        assert "confirm_password" in context["errors"]
        assert context["errors"]["confirm_password"] == "Пароли не совпадают"


def test_change_password_invalid_new_password(
    authenticated_client, captured_templates
):
    with captured_templates as templates:
        response = authenticated_client.post(
            "/change_password",
            data={
                "old_password": "password123",
                "new_password": "weak",
                "confirm_password": "weak",
            },
        )

        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == "change_password.html"
        assert "errors" in context
        assert "new_password" in context["errors"]
        assert (
            context["errors"]["new_password"]
            == "Пароль должен содержать не менее 8 символов"
        )


def test_change_password_form_data_preserved(
    authenticated_client, captured_templates
):
    with captured_templates as templates:
        response = authenticated_client.post(
            "/change_password",
            data={
                "old_password": "password123",
                "new_password": "NewPassword123",
                "confirm_password": "DifferentPassword123",
            },
        )

        assert response.status_code == 200
        _, context = templates[0]
        assert "form_data" in context
        assert context["form_data"]["old_password"] == "password123"
        assert context["form_data"]["new_password"] == "NewPassword123"
        assert (
            context["form_data"]["confirm_password"] == "DifferentPassword123"
        )


@pytest.mark.parametrize(
    ("password", "expected_error"),
    [
        (
            "nouppercaseletter123",
            "Пароль должен содержать как минимум одну заглавную букву",
        ),
        (
            "NOLOWERCASELETTER123",
            "Пароль должен содержать как минимум одну строчную букву",
        ),
        ("NoDigitsHere", "Пароль должен содержать как минимум одну цифру"),
        ("Password With Spaces123", "Пароль не должен содержать пробелов"),
        ("P" * 129, "Пароль не должен превышать 128 символов"),
    ],
)
def test_change_password_validates_password_requirements(
    authenticated_client, captured_templates, password, expected_error
):
    with captured_templates as templates:
        response = authenticated_client.post(
            "/change_password",
            data={
                "old_password": "password123",
                "new_password": password,
                "confirm_password": password,
            },
        )

        assert response.status_code == 200
        _, context = templates[0]
        assert "errors" in context
        assert "new_password" in context["errors"]
        assert expected_error == context["errors"]["new_password"]
