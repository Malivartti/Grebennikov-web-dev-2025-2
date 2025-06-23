import os

from dotenv import load_dotenv

from exam.user.types import Right, RoleName

dotenv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env")
load_dotenv(dotenv_path, override=True)

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

REMEMBER_COOKIE_PATH = "/exam"
SESSION_COOKIE_PATH = "/exam"
SESSION_COOKIE_NAME = "exam_session"

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "static", "uploads"
)

role_rights = {
    RoleName.ADMIN: {
        Right.ANIMAL_VIEW,
        Right.ANIMAL_CREATE,
        Right.ANIMAL_UPDATE,
        Right.ANIMAL_DELETE,
        Right.ADOPTION_MANAGE,
    },
    RoleName.MODER: {
        Right.ANIMAL_VIEW,
        Right.ANIMAL_CREATE,
        Right.ANIMAL_UPDATE,
        Right.ADOPTION_MANAGE,
    },
    RoleName.USER: {Right.ANIMAL_VIEW, Right.ADOPTION_CREATE},
    RoleName.GUEST: {Right.ANIMAL_VIEW},
}
