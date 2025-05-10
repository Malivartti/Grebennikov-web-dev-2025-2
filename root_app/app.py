from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("index"))
