#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://www.jeasyui.com/tutorial/index.php
# SOURCE: http://www.jeasyui.com/tutorial/app/crud.php


from flask import Flask, render_template_string, jsonify
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


import sqlite3


def create_connect(fields_as_dict=False):
    connect = sqlite3.connect('test_games.sqlite')

    if fields_as_dict:
        connect.row_factory = sqlite3.Row

    return connect


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
    <table id="dg" title="My games" class="easyui-datagrid" style="width:40%;height:600px"
            url="get_table"
            toolbar="#toolbar"
            rownumbers="true" fitColumns="true" singleSelect="true">
        <thead>
            <tr>
                <th field="name" width="25%">Name</th>
                <th field="price" width="25%">Price</th>
                <th field="append_date" width="25%">Append Date</th>
            </tr>
        </thead>
    </table>
    <div id="toolbar">
        <a href="#" class="easyui-linkbutton" iconCls="icon-add" plain="true" onclick="addGame()">Add Game</a>
        <a href="#" class="easyui-linkbutton" iconCls="icon-edit" plain="true" onclick="editGame()">Edit Game</a>
        <a href="#" class="easyui-linkbutton" iconCls="icon-remove" plain="true" onclick="deleteGame()">Remove Game</a>
    </div>
    
    <div id="dlg" class="easyui-dialog" style="width:400px;height:280px;padding:10px 20px"
            closed="true" buttons="#dlg-buttons">
        <div class="ftitle">Game</div>
        <form id="fm" method="post" novalidate>
            <div class="fitem">
                <label>Name:</label>
                <input name="name" class="easyui-textbox" required="true">
            </div>
            <div class="fitem">
                <label>Price:</label>
                <input name="price" class="easyui-textbox" required="true">
            </div>
            <div class="fitem">
                <label>Append Date:</label>
                <input name="append_date" class="easyui-textbox" disabled="true">
            </div>
        </form>
    </div>
    <div id="dlg-buttons">
        <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="saveGame()" style="width:90px">Save</a>
        <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="javascript:$('#dlg').dialog('close')" style="width:90px">Cancel</a>
    </div>
    
    <script type="text/javascript">
        function addGame() {
            $('#dlg').dialog('open').dialog('setTitle','Add Game');
            $('#fm').form('clear');
            url = 'save_game.php';
        }
        
        function editGame() {
            var row = $('#dg').datagrid('getSelected');
            if (row){
                $('#dlg').dialog('open').dialog('setTitle','Edit Game');
                $('#fm').form('load',row);
                url = 'update_game.php?id='+row.id;
            }
        }
        
        function saveGame(){
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
                        $('#dlg').dialog('close');      // close the dialog
                        $('#dg').datagrid('reload');    // reload the Game data
                    }
                }
            });
        }
        
        function deleteGame(){
            var row = $('#dg').datagrid('getSelected');
            if (row){
                $.messager.confirm('Confirm','Are you sure you want to delete this Game?',function(r){
                    if (r){
                        $.post('delete_Game.php',{id:row.id},function(result){
                            if (result.success){
                                $('#dg').datagrid('reload');    // reload the Game data
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


# TODO: support addGame(), editGame(), deleteGame()


@app.route("/get_table", methods=['POST', 'GET'])
def get_table():
    with create_connect(fields_as_dict=True) as connect:
        get_game_sql = '''
            SELECT id, name, price, append_date
            FROM game
            ORDER BY name
        '''
        items = list(map(dict, connect.execute(get_game_sql).fetchall()))

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
