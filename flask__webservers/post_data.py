#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, request
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return """
<div id="result"></div>
    
<script type="text/javascript">
function callAjax(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            callback(xmlhttp.responseText);
        }
    }
    xmlhttp.open("POST", url, true);
    xmlhttp.send(data);
}

callAjax('/print_data', "HelloWorld!\\nПриветМир!", function(responseText) {
    document.getElementById("result").innerHTML = responseText;
});
</script>
"""


@app.route("/print_data", methods=['POST'])
def print_data():
    data = request.data
    print('data:', data)

    return data


if __name__ == '__main__':
    app.debug = True
    app.run()
