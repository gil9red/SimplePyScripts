#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

from flask import Flask, render_template_string
from common import get_crash_statistics_list_db


app = Flask(__name__)


@app.route('/')
def index():
    headers = ["Дата", "ДТП", "Погибли", "Погибло детей", "Ранены", "Ранено детей"]
    rows = get_crash_statistics_list_db()
    rows.reverse()

    data_labels = []
    data_dtp = []
    data_died = []
    data_children_died = []
    data_wounded = []
    data_wounded_children = []

    for date, dtp, died, children_died, wounded, wounded_children in rows:
        x = DT.datetime.strptime(date, '%d.%m.%Y').date().isoformat()
        data_labels.append(x)

        data_dtp.append({
            "x": x,
            "y": int(dtp)
        })

        data_died.append({
            "x": x,
            "y": int(died)
        })

        data_children_died.append({
            "x": x,
            "y": int(children_died)
        })

        data_wounded.append({
            "x": x,
            "y": int(wounded)
        })

        data_wounded_children.append({
            "x": x,
            "y": int(wounded_children)
        })

    return render_template_string("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>{{ title }}</title>

    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='bootstrap-4.3.1/bootstrap.min.css') }}">

    <script src="{{ url_for('static', filename='js/jquery-3.1.1.min.js') }}"></script>
    <script src="{{ url_for('static', filename='bootstrap-4.3.1/bootstrap.min.js') }}"></script>
    <script src="{{ url_for('static', filename='chart_js_2.8.0/Chart.bundle.min.js') }}"></script>
</head>
<body>
<div class="container-fluid">
    <h2 class="text-center"><a href="https://гибдд.рф/">{{ title }}</a></h2>

    <div class="row">
        <div class="col-5">
            <table class="table table-hover">
                <thead class="thead-dark">
                    <tr>
                    {% for header in headers %}
                        <th>{{ header }}</th>
                    {% endfor %}
                    </tr>
                </thead>
                <tbody>
                {% for row in rows %}
                    <tr>
                        {% for value in row %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
        <div class="col">
            <canvas id="lineChart"></canvas>
        </div>
    </div>
</div>
<script>
    $(document).ready(function() {
        let data_dtp = {{ data_dtp | safe }}
        let data_died = {{ data_died | safe }};
        let data_children_died = {{ data_children_died | safe }};
        let data_wounded = {{ data_wounded | safe }};
        let data_wounded_children = {{ data_wounded_children | safe }};
        
        var ctx = document.getElementById("lineChart").getContext("2d");
        var lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ data_labels | safe }},
                datasets: [
                    {
                        label: 'ДТП',
                        lineTension: 0,
                        borderColor: "red",
                        data: data_dtp,
                    },
                    {
                        label: 'Погибли',
                        lineTension: 0,
                        borderColor: "rgb(246, 139, 31)",
                        data: data_died,
                    },
                    {
                        label: 'Погибло детей',
                        lineTension: 0,
                        borderColor: "rgb(68, 44, 110)",
                        data: data_children_died,
                    },
                    {
                        label: 'Ранены',
                        lineTension: 0,
                        borderColor: "blue",
                        data: data_wounded,
                    },
                    {
                        label: 'Ранено детей',
                        lineTension: 0,
                        borderColor: "green",
                        data: data_wounded_children,
                    },
                ],
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'DD/MM/YYYY',
                            displayFormats: {
                               day: 'DD/MM/YY'
                            }
                        },
                        distribution: 'linear'
                    }]
                }
            }
        });
    });
</script>
</body>
</html>
    """, title="АВАРИЙНОСТЬ НА ДОРОГАХ РОССИИ", headers=headers, rows=rows,
    data_labels=data_labels,
    data_dtp=data_dtp,
    data_died=data_died,
    data_children_died=data_children_died,
    data_wounded=data_wounded,
    data_wounded_children=data_wounded_children
)


if __name__ == "__main__":
    app.debug = True

    # Localhost
    app.run(
        # Включение поддержки множества подключений
        threaded=True,
        port=10009,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
