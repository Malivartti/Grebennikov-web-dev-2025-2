from werkzeug.middleware.dispatcher import DispatcherMiddleware

from exam.app import app as exam_app
from lab1.app import app as lab1_app
from lab2.app import app as lab2_app
from lab3.app import app as lab3_app
from lab4.app import app as lab4_app
from lab5.app import app as lab5_app
from lab6.app import create_app as create_lab6_app
from root_app.app import app as root_app

lab6_app = create_lab6_app()

app = DispatcherMiddleware(
    root_app,
    {
        "/lab1": lab1_app,
        "/lab2": lab2_app,
        "/lab3": lab3_app,
        "/lab4": lab4_app,
        "/lab5": lab5_app,
        "/lab6": lab6_app,
        "/exam": exam_app,
    },
)

application = app
