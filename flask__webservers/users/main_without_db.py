#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

# pip install flask
import flask

# pip install flask-login
# TODO: Bug fix:
#     pip install Werkzeug==2.3.7
import flask_login


LOGIN = os.environ.get("ADMIN_LOGIN", "foo@bar.example")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "secret")

# Our mock database.
USERS = {
    LOGIN: {
        "password": PASSWORD,
    },
}


app = flask.Flask(__name__)
app.secret_key = "super secret string"  # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    @classmethod
    def create(cls, login: str) -> "User":
        user = User()
        user.id = login
        return user


# Если авторизован
@login_manager.user_loader
def user_loader(email):
    if email not in USERS:
        return

    return User.create(email)


# Если не авторизован
@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in USERS:
        return

    return User.create(email)


@app.route("/")
def index():
    return flask.render_template_string(
        """
<!DOCTYPE html>
<html>
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
      {% if not current_user.is_authenticated %}
      <li><a href="/login">Login</a></li>
      {% else %}
      <li><a href="/logout">Logout</a></li>
      {% endif %}
    </ul>
  </nav>
  {% if current_user.is_authenticated %}
  <h1>You are logged as {{ current_user.id }}</h1>
  <a href="/protected">Protected</a>
  {% else %}
  <h1>You are not logged in</h1>
  {% endif %}
</body>
</html>
    """
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return """
            <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
            </form>
        """

    email = flask.request.form["email"]
    if email in USERS and flask.request.form["password"] == USERS[email]["password"]:
        user = User.create(email)
        flask_login.login_user(user)
        return flask.redirect(flask.url_for("index"))

    return "Bad login"


@app.route("/protected")
@flask_login.login_required
def protected():
    return f"Logged in as: {flask_login.current_user.id}"


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized", 401


if __name__ == "__main__":
    app.debug = True
    app.run(port=10101)
