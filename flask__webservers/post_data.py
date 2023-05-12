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
function callAjax(url, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200){
            callback(xhr.responseText);
        }
    }
    
    xhr.send(data);
}

var data = "HelloWorld!\\nПриветМир!";

callAjax('/print_data', data, function(responseText) {
    document.getElementById("result").innerHTML = responseText;
});
</script>
"""


@app.route("/print_data", methods=["POST"])
def print_data():
    data = request.data
    print("data:", data)

    return data


if __name__ == "__main__":
    app.run()
