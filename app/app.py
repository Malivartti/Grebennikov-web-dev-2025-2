import random
from flask import Flask, render_template, abort, make_response, request
from faker import Faker
from functools import lru_cache
from lib.validate import validate_phone

fake = Faker()

app = Flask(__name__)
application = app

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for i in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list())

@app.route('/posts/<int:index>')
def post(index):
    posts = posts_list()
    if (index >= len(posts) or index < 0):
        abort(404)
    p = posts[index]
    print(p)
    return render_template('post.html', title=p['title'], post=p)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.route('/args')
def args():
    return render_template('args.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html'))
    if 'name' not in request.cookies:
        resp.set_cookie('name', 'Ilya')
    else:
        resp.set_cookie('name', expires=0)
    return resp

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error = None
    formatted_phone = None

    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        
        if phone:
            is_valid, result = validate_phone(phone)
            if not is_valid:
                error = result
            else:
                formatted_phone = result
            
    return render_template('phone.html', error=error, formatted_phone=formatted_phone)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
