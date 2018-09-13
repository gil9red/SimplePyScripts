#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://www.jeasyui.com/tutorial/index.php
# SOURCE: http://www.jeasyui.com/tutorial/app/crud.php


from flask import Flask, render_template_string, jsonify
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string("""\
<html>
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>generate_table</title>
    
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/default/easyui.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/icon.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/color.css') }}">
    
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/jquery.min.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/jquery.easyui.min.js') }}"></script>
    
</head>
<body>
    <table id="dg" title="My Users" class="easyui-datagrid" style="width:400px;height:233px"
            url="get_table"
            toolbar="#toolbar"
            rownumbers="true" fitColumns="true" singleSelect="true">
        <thead>
            <tr>
                <th field="firstname" width="25%">First Name</th>
                <th field="lastname" width="25%">Last Name</th>
                <th field="phone" width="25%">Phone</th>
                <th field="email" width="25%">Email</th>
            </tr>
        </thead>
    </table>
    <div id="toolbar">
        <a href="#" class="easyui-linkbutton" iconCls="icon-add" plain="true" onclick="newUser()">New User</a>
        <a href="#" class="easyui-linkbutton" iconCls="icon-edit" plain="true" onclick="editUser()">Edit User</a>
        <a href="#" class="easyui-linkbutton" iconCls="icon-remove" plain="true" onclick="destroyUser()">Remove User</a>
    </div>
    
    <div id="dlg" class="easyui-dialog" style="width:400px;height:280px;padding:10px 20px"
            closed="true" buttons="#dlg-buttons">
        <div class="ftitle">User Information</div>
        <form id="fm" method="post" novalidate>
            <div class="fitem">
                <label>First Name:</label>
                <input name="firstname" class="easyui-textbox" required="true">
            </div>
            <div class="fitem">
                <label>Last Name:</label>
                <input name="lastname" class="easyui-textbox" required="true">
            </div>
            <div class="fitem">
                <label>Phone:</label>
                <input name="phone" class="easyui-textbox">
            </div>
            <div class="fitem">
                <label>Email:</label>
                <input name="email" class="easyui-textbox" validType="email">
            </div>
        </form>
    </div>
    <div id="dlg-buttons">
        <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="saveUser()" style="width:90px">Save</a>
        <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="javascript:$('#dlg').dialog('close')" style="width:90px">Cancel</a>
    </div>
    
    <script type="text/javascript">
        function newUser() {
            $('#dlg').dialog('open').dialog('setTitle','New User');
            $('#fm').form('clear');
            url = 'save_user.php';
        }
        
        function editUser() {
            var row = $('#dg').datagrid('getSelected');
            if (row){
                $('#dlg').dialog('open').dialog('setTitle','Edit User');
                $('#fm').form('load',row);
                url = 'update_user.php?id='+row.id;
            }
        }
        
        function saveUser(){
            $('#fm').form('submit',{
                url: url,
                onSubmit: function(){
                    return $(this).form('validate');
                },
                success: function(result){
                    var result = eval('('+result+')');
                    if (result.errorMsg){
                        $.messager.show({
                            title: 'Error',
                            msg: result.errorMsg
                        });
                    } else {
                        $('#dlg').dialog('close');        // close the dialog
                        $('#dg').datagrid('reload');    // reload the user data
                    }
                }
            });
        }
        
        function destroyUser(){
            var row = $('#dg').datagrid('getSelected');
            if (row){
                $.messager.confirm('Confirm','Are you sure you want to destroy this user?',function(r){
                    if (r){
                        $.post('destroy_user.php',{id:row.id},function(result){
                            if (result.success){
                                $('#dg').datagrid('reload');    // reload the user data
                            } else {
                                $.messager.show({    // show error message
                                    title: 'Error',
                                    msg: result.errorMsg
                                });
                            }
                        },'json');
                    }
                });
            }
        }
    </script>
    
    <style type="text/css">
        #fm{
            margin:0;
            padding:10px 30px;
        }
        .ftitle{
            font-size:14px;
            font-weight:bold;
            padding:5px 0;
            margin-bottom:10px;
            border-bottom:1px solid #ccc;
        }
        .fitem{
            margin-bottom:5px;
        }
        .fitem label{
            display:inline-block;
            width:80px;
        }
        .fitem input{
            width:160px;
        }
    </style>
    
</body>
</html>
    """)


@app.route("/get_table", methods=['POST', 'GET'])
def get_table():
    # TODO: replace sqlite
    items = [
        {'id': '3', 'firstname': 'fname1', 'lastname': 'lname1', 'phone': '(000)000-0000', 'email': 'name1@gmail.com'},
        {'id': '4', 'firstname': 'fname2', 'lastname': 'lname2', 'phone': '(000)000-0000', 'email': 'name2@gmail.com'},
        {'id': '5', 'firstname': 'fname3', 'lastname': 'lname3', 'phone': '(000)000-0000', 'email': 'name3@gmail.com'},
        {'id': '7', 'firstname': 'fname4', 'lastname': 'lname4', 'phone': '(000)000-0000', 'email': 'name4@gmail.com'},
        {'id': '8', 'firstname': 'fname5', 'lastname': 'lname5', 'phone': '(000)000-0000', 'email': 'name5@gmail.com'},
        {'id': '9', 'firstname': 'fname6', 'lastname': 'lname6', 'phone': '(000)000-0000', 'email': 'name6@gmail.com'},
        {'id': '10', 'firstname': 'fname7', 'lastname': 'lname7', 'phone': '(000)000-0000', 'email': 'name7@gmail.com'},
        {'id': '11', 'firstname': 'fname8', 'lastname': 'lname8', 'phone': '(000)000-0000', 'email': 'name8@gmail.com'},
        {'id': '12', 'firstname': 'fname9', 'lastname': 'lname9', 'phone': '(000)000-0000', 'email': 'name9@gmail.com'},
        {'id': '13', 'firstname': 'fname10', 'lastname': 'lname10', 'phone': '(000)000-0000', 'email': 'name10@gmail.com'},
        {'id': '14', 'firstname': 'fname11', 'lastname': 'lname11', 'phone': '(000)000-0000', 'email': 'name11@gmail.com'},
        {'id': '15', 'firstname': 'fname12', 'lastname': 'lname12', 'phone': '(000)000-0000', 'email': 'name12@gmail.com'},
    ]

    return jsonify(items)


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(
        port=5000,

        # :param threaded: should the process handle each request in a separate
        #                  thread?
        # :param processes: if greater than 1 then handle each request in a new process
        #                   up to this maximum number of concurrent processes.
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
