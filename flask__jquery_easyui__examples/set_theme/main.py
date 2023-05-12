#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://www.jeasyui.com/tutorial/


import logging
from flask import Flask, render_template_string, request, jsonify


app = Flask(__name__, static_folder="../static")
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string(
        """\
<html>
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>set_theme</title>
</head>
<body>
    <iframe src="get_html" width="500px" height="350px">
        Ваш браузер не поддерживает плавающие фреймы!
    </iframe>
    
    <iframe src="get_html?theme=black" width="500px" height="350px">
        Ваш браузер не поддерживает плавающие фреймы!
    </iframe>
    
    <iframe src="get_html?theme=bootstrap" width="500px" height="350px">
        Ваш браузер не поддерживает плавающие фреймы!
    </iframe>
    
    <iframe src="get_html?theme=gray" width="500px" height="350px">
        Ваш браузер не поддерживает плавающие фреймы!
    </iframe>
    
    <iframe src="get_html?theme=material" width="500px" height="350px">
        Ваш браузер не поддерживает плавающие фреймы!
    </iframe>
    
    <iframe src="get_html?theme=material-teal" width="500px" height="350px">
        Ваш браузер не поддерживает плавающие фреймы!
    </iframe>
    
    <iframe src="get_html?theme=metro" width="500px" height="350px">
        Ваш браузер не поддерживает плавающие фреймы!
    </iframe>
</body>
</html>
    """
    )


@app.route("/get_html")
def get_html():
    theme = request.args.get("theme", "default")

    return render_template_string(
        """\
<html>
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>set_theme</title>
    <p>{{ theme }}<p>

    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/"""
        + theme
        + """/easyui.css') }}">
    
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/jquery.min.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/jquery.easyui.min.js') }}"></script>
</head>
<body>
    <table class="easyui-datagrid" title="Basic DataGrid" style="width:400px;height:250px"
            data-options="singleSelect:true,collapsible:true,url:'datagrid_data1.json',method:'get'">
        <thead>
            <tr>
                <th data-options="field:'itemid',width:80">Item ID</th>
                <th data-options="field:'productid',width:100">Product</th>
                <th data-options="field:'listprice',width:80,align:'right'">List Price</th>
                <th data-options="field:'unitcost',width:80,align:'right'">Unit Cost</th>
                <th data-options="field:'attr1',width:250">Attribute</th>
                <th data-options="field:'status',width:60,align:'center'">Status</th>
            </tr>
        </thead>
    </table>
    
    <script type="text/javascript">
        $('document').ready(function() {
            $('.easyui-datagrid').datagrid({
                onLoadSuccess: function(data) {
                    $(this).datagrid('selectRow', 0);
                }
            });
        });
    </script>
</body>
</html>
    """,
        theme=theme,
    )


@app.route("/datagrid_data1.json")
def get_datalist_data():
    return jsonify({
        "total": 28,
        "rows": [
            {
                "productid": "FI-SW-01",
                "productname": "Koi",
                "unitcost": "10.00",
                "status": "P",
                "listprice": "36.50",
                "attr1": "Large",
                "itemid": "EST-1",
            },
            {
                "productid": "K9-DL-01",
                "productname": "Dalmation",
                "unitcost": "12.00",
                "status": "P",
                "listprice": "18.50",
                "attr1": "Spotted Adult Female",
                "itemid": "EST-10",
            },
            {
                "productid": "RP-SN-01",
                "productname": "Rattlesnake",
                "unitcost": "12.00",
                "status": "P",
                "listprice": "38.50",
                "attr1": "Venomless",
                "itemid": "EST-11",
            },
            {
                "productid": "RP-SN-01",
                "productname": "Rattlesnake",
                "unitcost": "12.00",
                "status": "P",
                "listprice": "26.50",
                "attr1": "Rattleless",
                "itemid": "EST-12",
            },
            {
                "productid": "RP-LI-02",
                "productname": "Iguana",
                "unitcost": "12.00",
                "status": "P",
                "listprice": "35.50",
                "attr1": "Green Adult",
                "itemid": "EST-13",
            },
            {
                "productid": "FL-DSH-01",
                "productname": "Manx",
                "unitcost": "12.00",
                "status": "P",
                "listprice": "158.50",
                "attr1": "Tailless",
                "itemid": "EST-14",
            },
            {
                "productid": "FL-DSH-01",
                "productname": "Manx",
                "unitcost": "12.00",
                "status": "P",
                "listprice": "83.50",
                "attr1": "With tail",
                "itemid": "EST-15",
            },
            {
                "productid": "FL-DLH-02",
                "productname": "Persian",
                "unitcost": "12.00",
                "status": "P",
                "listprice": "23.50",
                "attr1": "Adult Female",
                "itemid": "EST-16",
            },
            {
                "productid": "FL-DLH-02",
                "productname": "Persian",
                "unitcost": "12.00",
                "status": "P",
                "listprice": "89.50",
                "attr1": "Adult Male",
                "itemid": "EST-17",
            },
            {
                "productid": "AV-CB-01",
                "productname": "Amazon Parrot",
                "unitcost": "92.00",
                "status": "P",
                "listprice": "63.50",
                "attr1": "Adult Male",
                "itemid": "EST-18",
            },
        ],
    })


if __name__ == "__main__":
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
