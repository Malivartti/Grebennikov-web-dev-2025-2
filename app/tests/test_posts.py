# ----------------------------------- INDEX -----------------------------------

def test_index_page_template(client, captured_templates):
    with captured_templates as templates:
        response = client.get('/')
        assert response.status_code == 200

        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'index.html'

def test_index_page_invalide_method(client):
    response = client.post('/')
    assert response.status_code == 405

# ----------------------------------- END INDEX -----------------------------------

# ----------------------------------- POSTS -----------------------------------

def test_posts_page_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
        
        response = client.get('/posts')
        assert response.status_code == 200
        
        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'posts.html'


def test_posts_page_args(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)

        response = client.get('/posts')
        assert response.status_code == 200
        
        _, context = templates[0]
        assert context['title'] == 'Посты'

        posts = context['posts']
        assert len(posts) == len(posts_list)
        for i in range(len(posts)):
            assert posts[i] == posts_list[i]

def test_posts_page_insert(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)

        response = client.get('/posts')
        assert response.status_code == 200
        
        _, context = templates[0]
        assert context['title'] == 'Посты'

        posts = context['posts']
        assert len(posts) == len(posts_list)
        for i in range(len(posts)):
            received_post = posts[i]
            assert received_post['text'] in response.text
            assert received_post['author'] in response.text
            assert received_post['image_id'] in response.text

def test_posts_page_insert_date_fromat(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)

        response = client.get('/posts')
        assert response.status_code == 200
        
        _, context = templates[0]
        assert context['title'] == 'Посты'

        posts = context['posts']
        assert len(posts) == len(posts_list)
        for i in range(len(posts)):
            assert posts[i]['date'].strftime('%d.%m.%Y') in response.text


# ----------------------------------- END POSTS -----------------------------------

# ----------------------------------- POST -----------------------------------

def test_post_page_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
        
        id = 0
        response = client.get(f'/posts/{id}')
        assert response.status_code == 200
        
        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'post.html'

def test_post_page_args(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
        
        id = 0
        response = client.get(f'/posts/{id}')
        assert response.status_code == 200

        _, context = templates[0]
        transfered_post = posts_list[id]
        assert context['title'] == transfered_post['title']
        assert context['post'] == transfered_post

def test_post_page_insert(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
        
        id = 0
        response = client.get(f'/posts/{id}')
        assert response.status_code == 200
        
        _, context = templates[0]
        assert context['title'] in response.text
        assert context['post']['text'] in response.text
        assert context['post']['author'] in response.text
        assert context['post']['image_id'] in response.text

def test_post_page_insert_data_format(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
        
        id = 0
        response = client.get(f'/posts/{id}')
        assert response.status_code == 200

        _, context = templates[0]
        assert context['post']['date'].strftime('%d.%m.%Y') in response.text

def test_post_page_non_existent_id(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
        
        id = 10
        response = client.get(f'/posts/{id}')
        assert response.status_code == 404


def test_post_page_invalide_id(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)

    id = 'abc'
    response = client.get(f'/posts/{id}')
    assert response.status_code == 404

def test_post_page_insert_comments(client, captured_templates, mocker, posts_list_with_comments):
    with captured_templates as templates:
        mocker.patch("app.posts_list", return_value=posts_list_with_comments, autospec=True)
        
        id = 0
        response = client.get(f'/posts/{id}')
        assert response.status_code == 200

        _, context = templates[0]
        received_post_comments = context['post']['comments']
        for i in range(len(received_post_comments)):
            assert received_post_comments[i]['author'] in response.text
            assert received_post_comments[i]['text'] in response.text

            for j in range(len(received_post_comments[i]['replies'])):
                assert received_post_comments[i]['replies'][j]['author'] in response.text
                assert received_post_comments[i]['replies'][j]['text'] in response.text
        

# ----------------------------------- END POST -----------------------------------

# ----------------------------------- ABOUT -----------------------------------

def test_about_page_template(client, captured_templates):
    with captured_templates as templates:
        response = client.get('/about')
        assert response.status_code == 200
        
        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'about.html'

def test_about_page_args(client, captured_templates):
    with captured_templates as templates:
        response = client.get('/about')
        assert response.status_code == 200
        
        _, context = templates[0]
        assert context['title'] == 'Об авторе'

def test_about_page_insert(client, captured_templates):
    with captured_templates as templates:
        response = client.get('/about')
        assert response.status_code == 200

        _, context = templates[0]
        assert context['title'] in response.text

# ----------------------------------- END ABOUT -----------------------------------
