import pytest

@pytest.fixture
def authenticated_client(client):
    client.post('/login', data={
        'login': 'user',
        'password': 'qwerty',
        'remember_me': 'on'
    })
    return client

def test_counter_increments_per_session(client):
    """Проверка счетчика посещений"""
    response = client.get('/counter')
    assert response.status_code == 200
    assert '1' in response.text

    response = client.get('/counter')
    assert response.status_code == 200
    assert '2' in response.text

def test_successful_login(client, captured_templates):
    """Проверка успешной аутентификации"""
    with captured_templates as templates:
        response = client.post('/login', data={
            'login': 'user',
            'password': 'qwerty'
        }, follow_redirects=True)
        assert response.status_code == 200

        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'index.html'
        assert 'success' in response.text

def test_successful_login_redirects_to_index(client):
    """Проверка перенаправления после успешной аутентификации"""
    response = client.post('/login', data={
        'login': 'user',
        'password': 'qwerty'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.location == '/'

def test_failed_login_shows_error(client, captured_templates):
    """Проверка неудачной аутентификации"""
    with captured_templates as templates:
        response = client.post('/login', data={
            'login': 'user',
            'password': 'wrong'
        })
        assert response.status_code == 200

        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'auth.html'
        assert 'Пользователь не найден' in response.text

def test_secret_page_access_authenticated(authenticated_client, captured_templates):
    """Проверка доступа к секретной странице для аутентифицированного пользователя"""
    with captured_templates as templates:
        response = authenticated_client.get('/secret')
        assert response.status_code == 200

        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'secret.html'


def test_secret_page_redirects_unauthenticated(client, captured_templates):
    """Проверка доступа к секретной странице для неаутентифицированного пользователя"""
    with captured_templates as templates:
        response = client.get('/secret', follow_redirects=True)
        assert response.status_code == 200

        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'auth.html'
        assert 'Для доступа к данной странице необходимо пройти процедуру аутентификации' in response.text

def test_redirect_to_secret_after_login(client, captured_templates):
    """Проверка перенаправления на секретную страницу после аутентификации"""
    with captured_templates as templates:
        response = client.get('/secret', follow_redirects=True)
        assert response.status_code == 200

        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'auth.html'
        assert 'Для доступа к данной странице необходимо пройти процедуру аутентификации' in response.text

        path = response.request.path
        query_string = response.request.query_string.decode()
        full_path = f"{path}?{query_string}" if query_string else path
        print(full_path)
        response = client.post(full_path, data={
            'login': 'user',
            'password': 'qwerty',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert len(templates) == 2
        template, _ = templates[1]
        assert template.name == 'secret.html'

def test_remember_me_sets_cookie(client):
    """Проверка работы запомнить меня"""
    response = client.post('/login', data={
        'login': 'user',
        'password': 'qwerty',
        'remember_me': 'on'
    })
    assert 'Set-Cookie' in response.headers
    assert 'remember_token' in response.headers['Set-Cookie']


def test_navbar_links_unauthenticated(client):
    """Проверка отображения ссылок в навбаре для неаутентифицированного пользователя"""
    response = client.get('/')
    assert response.status_code == 200

    assert 'href="/login"' in response.text
    assert 'href="/secret"' not in response.text

def test_navbar_links_authenticated(authenticated_client):
    """Проверка отображения ссылок в навбаре для аутентифицированного пользователя"""
    response = authenticated_client.get('/')
    assert response.status_code == 200

    assert 'href="/secret"' in response.text
    assert 'href="/logout"' in response.text

def test_logout_redirects_to_index(authenticated_client, captured_templates):
    """Проверка выхода из аккаунта"""
    with captured_templates as templates:
        response = authenticated_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

        assert len(templates) == 1
        assert templates[0][0].name == 'index.html'

        response = authenticated_client.get('/')
        assert 'href="/secret"' not in response.text

def test_counter_independent_sessions(app):
    """Проверка уникальности счетчика для разных сессий"""
    client1 = app.test_client()
    client2 = app.test_client()

    _ = client1.get('/counter')
    response2 = client1.get('/counter')
    assert 'Вы посетили эту страницу 2 раз(а)!' in response2.text
    

    response3 = client2.get('/counter')
    assert 'Вы посетили эту страницу 1 раз(а)!' in response3.text