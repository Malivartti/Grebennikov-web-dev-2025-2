# ----------------------------------- ARGS -----------------------------------

def test_args_page_displays_url_params(client):
    """Проверка отображения параметров URL"""
    response = client.get('/args?param1=value1&param2=value2')
    assert response.status_code == 200

    assert '<td>param1</td>' in response.text
    assert '<td>value1</td>' in response.text

    assert '<td>param2</td>' in response.text
    assert '<td>value2</td>' in response.text

def test_args_page_displays_without_url_params(client):
    """Проверка отображения отсутствующих параметров URL"""
    response = client.get('/args')
    assert response.status_code == 200

    assert '<td>' not in response.text
    assert '</td>' not in response.text

# ----------------------------------- END ARGS -----------------------------------

# ----------------------------------- HEADERS -----------------------------------

def test_headers_page_displays_request_headers(client):
    """Проверка отображения заголовков запроса"""
    headers = {'User-Agent': 'Test-Agent', 'Custom-Header': 'Test-Value'}
    response = client.get('/headers', headers=headers)
    assert response.status_code == 200

    assert '<td>User-Agent</td>' in response.text
    assert '<td>Test-Agent</td>' in response.text

    assert '<td>Custom-Header</td>' in response.text
    assert '<td>Test-Value</td>' in response.text

# ----------------------------------- END HEADERS -----------------------------------

# ----------------------------------- COOKIES -----------------------------------

def test_cookies_set_new_cookie(client):
    """Проверка установки нового cookie"""
    response = client.get('/cookies')
    assert response.status_code == 200

    assert 'Set-Cookie' in response.headers
    assert 'name=Ilya' in response.headers['Set-Cookie']

def test_cookies_delete_existing_cookie(client):
    """Проверка удаления существующего cookie"""
    client.set_cookie('name', 'Ilya')
    response = client.get('/cookies')
    assert response.status_code == 200

    assert 'Set-Cookie' in response.headers
    assert 'name=; Expires=' in response.headers['Set-Cookie']

# ----------------------------------- END COOKIES -----------------------------------

# ----------------------------------- FORM -----------------------------------

def test_form_page_displays_post_data(client):
    """Проверка отображения параметров формы после отправки"""
    form_data = {'field1': 'value1', 'field2': 'value2'}
    response = client.post('/form', data=form_data)
    assert response.status_code == 200

    assert '<td>field1</td>' in response.text
    assert '<td>value1</td>' in response.text

    assert '<td>field2</td>' in response.text
    assert '<td>value2</td>' in response.text

def test_form_page_displays_without_post_data(client):
    """Проверка отображения отсутствующих параметров формы после отправки"""
    response = client.post('/form')
    assert response.status_code == 200

    assert '<td>' not in response.text
    assert '</td>' not in response.text

# ----------------------------------- END FORM -----------------------------------

# ----------------------------------- PHONE -----------------------------------

def test_phone_valid_11_digits_with_plus(client):
    """Проверка валидации номера с +7 и 11 цифрами"""
    response = client.post('/phone', data={'phone': '+71234567890'})
    assert response.status_code == 200
    assert '8-123-456-78-90' in response.text
    assert 'is-invalid' not in response.text

def test_phone_valid_11_digits_with_8(client):
    """Проверка валидации номера с 8 и 11 цифрами"""
    response = client.post('/phone', data={'phone': '81234567890'})
    assert response.status_code == 200
    assert '8-123-456-78-90' in response.text
    assert 'is-invalid' not in response.text

def test_phone_valid_10_digits(client):
    """Проверка валидации номера с 10 цифрами"""
    response = client.post('/phone', data={'phone': '1234567890'})
    assert response.status_code == 200
    assert '8-123-456-78-90' in response.text
    assert 'is-invalid' not in response.text

def test_phone_with_special_chars(client):
    """Проверка валидации номера со спецсимволами"""
    response = client.post('/phone', data={'phone': '+7 (123) 456-78-90'})
    assert response.status_code == 200
    assert '8-123-456-78-90' in response.text
    assert 'is-invalid' not in response.text

def test_phone_invalid_length_short(client):
    """Проверка ошибки при недостаточном количестве цифр"""
    response = client.post('/phone', data={'phone': '+712345678'})
    assert response.status_code == 200
    assert 'Недопустимый ввод. Неверное количество цифр.' in response.text
    assert 'is-invalid' in response.text
    assert 'invalid-feedback' in response.text

def test_phone_invalid_length_long(client):
    """Проверка ошибки при избыточном количестве цифр"""
    response = client.post('/phone', data={'phone': '+7123456789012'})
    assert response.status_code == 200
    assert 'Недопустимый ввод. Неверное количество цифр.' in response.text
    assert 'is-invalid' in response.text
    assert 'invalid-feedback' in response.text

def test_phone_invalid_chars(client):
    """Проверка ошибки при недопустимых символах"""
    response = client.post('/phone', data={'phone': '+71234abc7890'})
    assert response.status_code == 200
    assert 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.' in response.text
    assert 'is-invalid' in response.text
    assert 'invalid-feedback' in response.text

def test_phone_empty_input(client):
    """Проверка обработки пустого ввода"""
    response = client.post('/phone', data={'phone': ''})
    assert response.status_code == 200
    assert 'is-invalid' not in response.text
    assert '8-' not in response.text

def test_phone_formatted_output(client):
    """Проверка форматирования корректного номера"""
    response = client.post('/phone', data={'phone': '8(123)4567890'})
    assert response.status_code == 200
    assert '8-123-456-78-90' in response.text
    assert 'is-invalid' not in response.text

# ----------------------------------- END PHONE -----------------------------------