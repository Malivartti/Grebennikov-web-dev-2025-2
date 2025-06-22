import os

from dotenv import load_dotenv

load_dotenv("./.env", override=True)

SECRET_KEY = os.getenv("SECRET_KEY")

db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_port = os.getenv("MYSQL_PORT")
db_name = os.getenv("MYSQL_DATABASE")

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_PATH = "/"  # TODO change to /exam before deploy
SESSION_COOKIE_PATH = "/"  # TODO
SESSION_COOKIE_NAME = "exam_session"

role_rights = {
    "администратор": {},
    "модератор": {},
    "пользователь": {},
    None: {},
}
