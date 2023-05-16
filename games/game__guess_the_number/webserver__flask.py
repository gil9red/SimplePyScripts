#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/44d89639620d326ea67f2dfb909545c508259911/game__guess_the_number.py


import logging
import random

from flask import Flask, render_template_string, request, redirect


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


GAME_DATA = {
    "ADMIN": {
        "max_n": None,
        "trying": None,
        "hidden_num": None,
        "num": None,
        "response": "",
        "end_game": False,
    }
}


def get_current_game_data():
    return GAME_DATA["ADMIN"]


@app.route("/")
def index():
    return render_template_string(
        """\
<html>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    
    <body>
        {% if not game_data['end_game'] %}
            {% if not game_data['max_n'] %}
            <form method="post" action="/set_max_n">
                <label>Введите максимальное значение диапазона N:
                    <input id="max_n" name="max_n" type="number" step="1" min="1" value="100"></input>
                </label>
                <p><input type="submit" value="Отправить"></p>
            </form>
    
            {% else %}
            <form method="post" action="/send_num">
                <p>Я загадал число "?"</p>
                <p>Количество попыток: {{ game_data['trying'] }}</p>
                
                <label>Введите число:
                    <input id="num" name="num" type="number" step="1" min="1" max="{{ game_data['max_n'] }}" value="1"></input>
                </label>
                <p><input type="submit" value="Отправить"></p>
            </form>
            {% endif %}
        {% endif %}
        
        {% if game_data['response'] %}
            <textarea readonly>{{ game_data['response'] }}</textarea>
        {% endif %}
        
        <form method="post" action="/new_game">
            <p><input type="submit" value="Новая игра"></p>
        </form>
        
        <br>
        <br>
        <div>{{ game_data }}</div>
        
    </body>
</html>""",
        game_data=get_current_game_data(),
    )


@app.route("/set_max_n", methods=["POST"])
def set_max_n():
    print(request.form)

    max_n = int(request.form["max_n"])
    trying = max_n // 10
    hidden_num = random.randint(1, max_n)

    game_data = get_current_game_data()
    game_data["max_n"] = max_n
    game_data["trying"] = trying
    game_data["hidden_num"] = hidden_num

    return redirect("/")


@app.route("/send_num", methods=["POST"])
def send_num():
    print(request.form)

    game_data = get_current_game_data()

    num = int(request.form["num"])
    hidden_num = int(game_data["hidden_num"])
    trying = int(game_data["trying"])

    if num == hidden_num:
        game_data["end_game"] = True
        game_data["response"] += "Победа!\n"
        return redirect("/")

    elif num > hidden_num:
        game_data["response"] += 'Неа, "?" < "{}"\n'.format(num)

    else:
        game_data["response"] += 'Неа, "?" > "{}"\n'.format(num)

    trying -= 1

    if trying == 0:
        game_data[
            "response"
        ] += "Закончились попытки. Проигрыш!\nЗагаданное число: {}".format(hidden_num)
        game_data["end_game"] = True
        return redirect("/")

    game_data["trying"] = trying

    return redirect("/")


@app.route("/new_game", methods=["POST"])
def new_game():
    print(request.form)

    game_data = get_current_game_data()
    for k in game_data:
        game_data[k] = None

    game_data["response"] = ""
    game_data["end_game"] = False

    return redirect("/")


if __name__ == "__main__":
    # Localhost
    app.debug = True
    app.run(port=10000)

    # # Public IP
    # app.run(host='0.0.0.0')
