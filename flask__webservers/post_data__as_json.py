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
    
<script type="text/javascript">
function callAjaxJson(url, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200){
            callback(xhr.responseText);
        }
    }
    
    xhr.send(data);
}

var json = JSON.stringify({
    name: "Виктор",
    surname: "Цой",
});

callAjaxJson('/print_data', json, function(responseText) {
    document.getElementById("result").innerHTML = responseText;
});
</script>
"""


@app.route("/print_data", methods=["POST"])
def print_data():
    data = request.data
    print("data:", data)

    json = request.json
    print("json:", json)

    return data


if __name__ == "__main__":
    app.run()
