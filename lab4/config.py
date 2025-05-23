import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from lab4.app import Application


def setup_config(app: "Application"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(current_dir, ".env")
    load_dotenv(dotenv_path, override=True)

    db_user = os.getenv("MYSQL_USER")
    db_password = os.getenv("MYSQL_PASSWORD")
    db_host = os.getenv("MYSQL_HOST")
    db_port = os.getenv("MYSQL_PORT")
    db_name = os.getenv("MYSQL_DATABASE")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = (
        "2ad8d52a848cf094ec501e8b51271610ef378e42cc8171e8654c10f40dd36088"
    )
    app.config["REMEMBER_COOKIE_PATH"] = "/lab4"
    app.config["SESSION_COOKIE_PATH"] = "/lab4"
    app.config["SESSION_COOKIE_NAME"] = "lab4_session"
