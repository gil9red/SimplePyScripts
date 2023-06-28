#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/3753314/5909792


import cherrypy


class Root(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def update(self):
        input_json = cherrypy.request.json
        print("input_json:", input_json)
        # do_something_with(input_json)

        return "Updated %r." % (input_json,)

    @cherrypy.expose
    def index(self):
        return """
<html>
    <head>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    </head>
    <body>
        <script type='text/javascript'>
            function Update() {
                $.ajax({
                  type: 'POST',
                  url: "update",
                  contentType: "application/json",
                  processData: false,
                  data: $('#update_box').val(),
                  success: function(data) {alert(data);},
                  error: function(data) {alert('Error:' + data);},
                  dataType: "text"
                });
            }
        </script>
    
        <input type='textbox' id='update_box' value='{"a": 2, "b": 3}' size='100' />
        <input type='submit' value='Update' onClick='Update(); return false' />
    </body>
</html>
"""


if __name__ == "__main__":
    cherrypy.quickstart(Root())
