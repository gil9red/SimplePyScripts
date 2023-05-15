#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)


TODOS = {
    "todo1": {"task": "build an API"},
    "todo2": {"task": "?????"},
    "todo3": {"task": "profit!"},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message=f"Todo {todo_id} doesn't exist")


parser = reqparse.RequestParser()
parser.add_argument("task")


class Index(Resource):
    def get(self):
        return {"total": len(TODOS)}


class Todo(Resource):
    """
    Shows a single todo item and lets you delete a todo item
    """

    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return dict(ok=True)

    def put(self, todo_id):
        args = parser.parse_args()
        task = {"task": args["task"]}
        TODOS[todo_id] = task
        return task, 201


class TodoList(Resource):
    """
    Shows a list of all todos, and lets you POST to add new tasks
    """

    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = f"todo{len(TODOS.keys()) + 1}"
        TODOS[todo_id] = {"task": args["task"]}
        return TODOS[todo_id], 201


api.add_resource(Index, "/")
api.add_resource(TodoList, "/todos")
api.add_resource(Todo, "/todos/<todo_id>")


if __name__ == "__main__":
    app.run(debug=True)
