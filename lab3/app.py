import random
from flask import Flask, render_template, abort, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from faker import Faker
from functools import lru_cache
from urllib.parse import urlparse

fake = Faker()

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации'
login_manager.login_message_category = 'warning'

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

def get_users():
    return [
        {
            'id': '1',
            'login': 'user',
            'password': 'qwerty'
        }
    ]

class User(UserMixin):
    def __init__(self, user_id, login):
        self.id = user_id
        self.login = login


@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user_id == user['id']:
            return User(user['id'], user['login'])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'

        if login and password:
            for user in get_users():
                if user['login'] == login and user['password'] == password:
                    user = User(user['id'], user['login'])
                    login_user(user, remember=remember_me)
                    flash('Вы успешно аутентифицированны', 'success')

                    next_page = request.args.get('next')
                    if next_page:
                        parsed = urlparse(next_page)
                        if parsed.scheme or parsed.netloc:
                            return redirect(url_for('index'))
                        print(next_page)
                        return redirect(next_page)
                    return redirect(url_for('index'))
            return render_template('auth.html', error="Пользователь не найден")

    return render_template('auth.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

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

@app.route('/counter')
def counter():
    if not session.get('counter'):
        session['counter'] = 0
    session['counter'] += 1

    return render_template('counter.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404