#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from flask import Flask, request


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return """
<div id="result"></div>
    
<script type="text/javascript">
function callAjax(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            callback(xhr.responseText);
        }
    }
    
    xhr.send();
}

callAjax('/print_args?a=1&text_en=Hello World!&text_ru=Привет Мир!&ok=true', function(responseText) {
    document.getElementById("result").innerHTML = responseText;
});
</script>

<br>
<div>
    <a href="/print_args?a=1&b=2&c=abc">/print_args?a=1&b=2&c=abc</a>
</div>
"""


@app.route("/print_args")
def print_args():
    args = request.args
    print(args)

    text = '<table border="1px" width="300px">'
    text += "<caption>URL ARGUMENTS:<caption>"
    for k, v in args.items():
        text += f"<tr><td>{k}</td><td>{v}</td></tr>"
    text += "</table>"

    return text


if __name__ == "__main__":
    app.run()
