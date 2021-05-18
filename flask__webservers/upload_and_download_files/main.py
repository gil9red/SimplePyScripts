#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os

from flask import Flask, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            # Функция secure_filename не дружит с не ascii-символами, поэтому
            # файлы русскими словами не называть
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Функция url_for('uploaded_file', filename=filename) возвращает строку вида: /uploads/<filename>
            return redirect(url_for('uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


# Пример обработчика, возвращающий файлы из папки app.config['UPLOAD_FOLDER'] для путей uploads и files.
# т.е. не нужно давать специальное название, чтобы получить файл в flask
# @app.route('/uploads/<filename>')
@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # Localhost
    app.run()
