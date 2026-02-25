#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from flask import Flask, request


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index() -> str:
    return """
<div id="result"></div>
<br>

<form method="POST" action="/print_data" 
    onsubmit="return submitForm(this, function(responseText) { document.getElementById('result').innerHTML = responseText; });">
    <input name="name" value="Виктор">
    <input name="surname" value="Цой">
    <p><input type="submit" value="Отправить"></p>
</form>

<script type="text/javascript">
function submitForm(form, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action, true);
            
    // Создать объект для формы
    var formData = new FormData(form);
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200){
            callback(xhr.responseText);
        }
    }
    
    xhr.send(formData);
    return false;
}

</script>
"""


@app.route("/print_data", methods=["POST"])
def print_data():
    data = request.data
    print("data:", data)

    form = request.form
    print("form:", form)

    return form["name"] + " " + form["surname"]


if __name__ == "__main__":
    app.run()
