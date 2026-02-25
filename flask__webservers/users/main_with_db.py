#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/


import os

from typing import Optional

# pip install flask==3.0.0
import flask

# pip install flask-login==0.6.2
import flask_login

# pip install flask-sqlalchemy==3.1.1
# TODO: Bug fix for flask-login==0.6.2 - flask-sqlalchemy installed/updated Werkzeug
#     pip install Werkzeug==2.3.7
from flask_sqlalchemy import SQLAlchemy


# TODO: Убрать дублирование кода в шаблонах
# TODO: Не хранить пароль в чистом виде
# TODO: Сделать вариант примера с peewee


app = flask.Flask(__name__)
app.secret_key = "super secret string"  # Change this!
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///db.sqlite")

db = SQLAlchemy()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    @classmethod
    def get_by(cls, username: str) -> Optional["User"]:
        return cls.query.filter_by(
            username=username
        ).first()


db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def loader_user(user_id: int):
    return db.session.get(User, user_id)


@app.route("/")
def index():
    return flask.render_template_string("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Home</title>
    <style>
      h1 {
        color: green;
      }
    </style>
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/register">Create account</a></li>
        <li><a href="/protected">Protected</a></li>
        <li><a href="/logout">Logout</a></li>
      </ul>
    </nav>
  {% if current_user.is_authenticated %}
  <h1>You are logged as {{ current_user.username }}</h1>
  {% else %}
  <h1>You are not logged in</h1>
  {% endif %}
  </body>
</html>
    """)


@app.route('/register', methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        if User.get_by(username):
            return "There is already a user with this nickname"

        password = flask.request.form.get("password")

        user = User(
            username=username,
            password=password,
        )
        db.session.add(user)
        db.session.commit()

        return flask.redirect(flask.url_for("login"))

    return flask.render_template_string("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sign Up</title>
    <style>
      h1 {
        color: green;
      }
    </style>
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/register">Create account</a></li>
        <li><a href="/protected">Protected</a></li>
        <li><a href="/logout">Logout</a></li>
      </ul>
    </nav>
    <h1>Create an account</h1>
    <form action="#" method="post">
      <label for="username">Username:</label>
      <input type="text" name="username" />
      <label for="password">Password:</label>
      <input type="password" name="password" />
      <button type="submit">Submit</button>
    </form>
  </body>
</html>
    """)


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        user = User.get_by(username)
        if user and user.password == password:
            flask_login.login_user(user)
            return flask.redirect(flask.url_for("index"))

        return "Bad login"

    return flask.render_template_string("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login</title>
    <style>
        h1 {
          color: green;
        }
    </style>
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/register">Create account</a></li>
        <li><a href="/protected">Protected</a></li>
        <li><a href="/logout">Logout</a></li>
      </ul>
    </nav>
    <h1>Login to your account</h1>
    <form action="#" method="post">
      <label for="username">Username:</label>
      <input type="text" name="username" />
      <label for="password">Password:</label>
      <input type="password" name="password" />
      <button type="submit">Submit</button>
    </form>
  </body>
</html>
    """)


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))


@app.route("/protected")
@flask_login.login_required
def protected() -> str:
    return f"Logged in as: {flask_login.current_user.username}"


if __name__ == "__main__":
    app.debug = True
    app.run(port=10101)
