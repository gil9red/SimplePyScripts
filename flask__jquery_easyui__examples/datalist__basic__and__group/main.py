#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://www.jeasyui.com/demo/main/index.php?plugin=DataList&theme=default
# SOURCE: http://www.jeasyui.com/documentation/datalist.php


import logging
from flask import Flask, render_template_string, jsonify


app = Flask(__name__, static_folder="../static")
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string(
        """\
<html>
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>DataList__basic__and__group</title>

    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/default/easyui.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/icon.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/color.css') }}">
    
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/jquery.min.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/jquery.easyui.min.js') }}"></script>
</head>
<body>
    <div style="margin:20px 0"></div>
    <div class="easyui-layout" style="width:50%;height:500px">
        <div data-options="region:'west'" style="width:50%;">
            <!-- lines -- линии между элементами -->
            <ul class="easyui-datalist" title="Basic DataList" lines="true">
                <li value="AL">Alabama</li>
                <li value="AK">Alaska</li>
                <li value="AZ">Arizona</li>
                <li value="AR">Arkansas</li>
                <li value="CA">California</li>
                <li value="CO">Colorado</li>
                <li value="CT">Connecticut</li>
                <li value="DE">Delaware</li>
                <li value="FL">Florida</li>
                <li value="GA">Georgia</li>
                <li value="HI">Hawaii</li>
                <li value="ID">Idaho</li>
                <li value="IL">Illinois</li>
                <li value="IN">Indiana</li>
                <li value="IA">Iowa</li>
                <li value="KS">Kansas</li>
                <li value="KY">Kentucky</li>
                <li value="LA">Louisiana</li>
                <li value="ME">Maine</li>
                <li value="MD">Maryland</li>
                <li value="MA">Massachusetts</li>
                <li value="MI">Michigan</li>
                <li value="MN">Minnesota</li>
                <li value="MS">Mississippi</li>
                <li value="MO">Missouri</li>
                <li value="MT">Montana</li>
                <li value="NE">Nebraska</li>
                <li value="NV">Nevada</li>
                <li value="NH">New Hampshire</li>
                <li value="NJ">New Jersey</li>
                <li value="NM">New Mexico</li>
                <li value="NY">New York</li>
                <li value="NC">North Carolina</li>
                <li value="ND">North Dakota</li>
                <li value="OH">Ohio</li>
                <li value="OK">Oklahoma</li>
                <li value="OR">Oregon</li>
                <li value="PA">Pennsylvania</li>
                <li value="RI">Rhode Island</li>
                <li value="SC">South Carolina</li>
                <li value="SD">South Dakota</li>
                <li value="TN">Tennessee</li>
                <li value="TX">Texas</li>
                <li value="UT">Utah</li>
                <li value="VT">Vermont</li>
                <li value="VA">Virginia</li>
                <li value="WA">Washington</li>
                <li value="WV">West Virginia</li>
                <li value="WI">Wisconsin</li>
                <li value="WY">Wyoming</li>
            </ul>
        </div>
        
        <div data-options="region:'center'" style="width:50%;">
            <div id="dl1"></div>
        </div>
    </div>
    <div style="margin:20px 0"></div>
    <div class="easyui-layout" style="width:50%;height:500px">
        <div data-options="region:'west'" style="width:50%;">
            <div id="dl2"></div>
        </div>
        <div data-options="region:'center'" style="width:50%;">
            <div>Clicked:</div>
            <textarea id="alltext" style="width:100%;height:100%"></textarea>
        </div>
    </div>
    
    <script type="text/javascript">
        $('document').ready(function() {
            $('#dl1').datalist({
                title: "Group DataList (JS+AJAX)",
                url: 'datalist_data.json',
                method: 'get',
                groupField: 'group',
                lines: true
            });
            
            var group_list = [
                {"group":"Printer","text":"Epson WorkForce 845"},
                {"group":"Printer","text":"Canon PIXMA MG5320"},
                {"group":"Printer","text":"HP Deskjet 1000 Printer"},
                {"group":"Firewall","text":"Cisco RV110W-A-NA-K9"},
                {"group":"Firewall","text":"ZyXEL ZyWALL USG50"},
                {"group":"Firewall","text":"NETGEAR FVS318"},
                {"group":"Keyboard","text":"Logitech Keyboard K120"},
                {"group":"Keyboard","text":"Microsoft Natural Ergonomic Keyboard 4000"},
                {"group":"Keyboard","text":"Logitech Wireless Touch Keyboard K400"},
                {"group":"Keyboard","text":"Logitech Gaming Keyboard G110"},
                {"group":"Camera","text":"Nikon COOLPIX L26 16.1 MP"},
                {"group":"Camera","text":"Canon PowerShot A1300"},
                {"group":"Camera","text":"Canon PowerShot A2300"}
            ];
            $('#dl2').datalist({
                title: "Group DataList (JS+JSON)",
                data: group_list,
                method: 'get',
                groupField: 'group',
                lines: true,
                onClickRow: function(index, row) {
                    console.log("click: " + index + ": '" + row.text + "' -> " + JSON.stringify(row));
                    $('#alltext').append(row.text + "\\n");
                }
            });
        });
    </script>
</body>
</html>
    """
    )


@app.route("/datalist_data.json")
def get_datalist_data():
    return jsonify([
        {"text": "Epson WorkForce 845", "group": "Printer"},
        {"text": "Canon PIXMA MG5320", "group": "Printer"},
        {"text": "HP Deskjet 1000 Printer", "group": "Printer"},
        {"text": "Cisco RV110W-A-NA-K9", "group": "Firewall"},
        {"text": "ZyXEL ZyWALL USG50", "group": "Firewall"},
        {"text": "NETGEAR FVS318", "group": "Firewall"},
        {"text": "Logitech Keyboard K120", "group": "Keyboard"},
        {"text": "Microsoft Natural Ergonomic Keyboard 4000", "group": "Keyboard"},
        {"text": "Logitech Wireless Touch Keyboard K400", "group": "Keyboard"},
        {"text": "Logitech Gaming Keyboard G110", "group": "Keyboard"},
        {"text": "Nikon COOLPIX L26 16.1 MP", "group": "Camera"},
        {"text": "Canon PowerShot A1300", "group": "Camera"},
        {"text": "Canon PowerShot A2300", "group": "Camera"},
    ])


if __name__ == "__main__":
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
