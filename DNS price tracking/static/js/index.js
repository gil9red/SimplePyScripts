// SOURCE: https://gist.github.com/nosp4mSnippets/5846729
// Wait for final event example during resize
var waitForFinalEvent = (function () {
  var timers = {};
  return function (callback, ms, uniqueId) {
    if (!uniqueId) {
      uniqueId = "Don't call this twice without a uniqueId";
    }
    if (timers[uniqueId]) {
      clearTimeout (timers[uniqueId]);
    }
    timers[uniqueId] = setTimeout(callback, ms);
  };
})();

const SEARCH_DATA_VISIBLE = [
    { field : 'visible', value : true, operator : 'is' }
];
const SEARCH_DATA_FAVORITE = [
    { field : 'favorite', value : true, operator : 'is' }
];

function showOnlyVisibleProducts() {
    w2ui.products.search(SEARCH_DATA_VISIBLE);
}

function showOnlyFavoriteProducts() {
    w2ui.products.search(SEARCH_DATA_FAVORITE);
}

function showFavoriteTotals() {
    let prices_dns = [];
    let prices_tp = [];

    let items = w2ui.products.find({ favorite: true });
    for (const i of items) {
        let product = w2ui.products.get(i);

        if (product.price_dns != null) {
            prices_dns.push(product.price_dns);
        }
        if (product.price_techopoint != null) {
            prices_tp.push(product.price_techopoint);
        }
    }

    // DNS
    let total_DNS_favorites_prices = $('#favorite_totals .dns_prices');
    if (prices_dns.length == 1) {
        total_DNS_favorites_prices.text(prices_dns[0]);

    } else if (prices_dns.length > 1) {
        total_DNS_favorites_prices.text(
            prices_dns.join(' + ') + ' = ' + prices_dns.reduce((a, b) => a + b, 0)
        );
    }

    let total_tp_favorites_prices = $('#favorite_totals .techopoint_prices');
    if (prices_tp.length == 1) {
        total_tp_favorites_prices.text(prices_tp[0]);
    } else if (prices_tp.length > 1) {
        total_tp_favorites_prices.text(
            prices_tp.join(' + ') + ' = ' + prices_tp.reduce((a, b) => a + b, 0)
        );
    }

    // Diff
    let total_diff = $('#favorite_totals .diff');
    total_diff.text(
        prices_dns.reduce((a, b) => a + b, 0)
        - prices_tp.reduce((a, b) => a + b, 0)
    );

    $('#favorite_totals').show();
}

function getLastSelectedProduct() {
    // Get last saved row
    let product_id;
    if (localStorage.product_id) {
        product_id = localStorage.product_id;
    } else {
        product_id = w2ui.products.records[0].recid;
    }

    return product_id;
}

function selectLastProduct() {
    let product_id = getLastSelectedProduct();
    w2ui.products.select(product_id);
}

// Плагин, что рисует отметки на элементах, что выделены в таблице #prices
Chart.pluginService.register({
    afterDraw: function(chartInstance) {
        let ctx = chartInstance.chart.ctx;

        let items = [];
        for (const i of w2ui.prices.getSelection()) {
            items.push(w2ui.prices.get(i).datetime);
        }

        ctx.fillStyle = 'red';
        ctx.lineWidth = 5;
        ctx.strokeStyle = ctx.fillStyle;

        chartInstance.data.datasets.forEach(function (dataset) {
            for (let i = 0; i < dataset.data.length; i++) {
                // Проверяем, что точка относится к элементу, выделенному в таблице
                let datetime = dataset.data[i].x;
                if (!items.includes(datetime)) {
                    continue;
                }

                let model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;

                ctx.beginPath();
                ctx.arc(model.x, model.y, 3, 0, 2 * Math.PI, false);
                ctx.fill();
                ctx.stroke();
            }
        });
    }
});


$(function () {
    $('#products').w2grid({
        name: 'products',
        show: {
            footer: true,
        },
        multiSelect: false,
        columns: [
            { field: 'recid', caption: 'ID', size: '35px', sortable: true },
            { field: 'title', caption: 'Title', size: '80%', sortable: true },
            { field: 'price_dns', caption: 'DNS', size: '70px', sortable: true, render: 'float' },
            { field: 'price_techopoint', caption: 'TP', size: '70px', sortable: true, render: 'float' },
            { field: 'link', caption: 'Link', size: '50px',
                render: function(record) {
                    return `
                    <a href="${record.link_dns}" target="_blank" title="${record.link_dns}">
                        <img src="${DNS_PNG}" alt="DNS">
                    </a>
                    <a href="${record.link_techopoint}" target="_blank" title="${record.link_techopoint}">
                        <img src="${TECHNOPOINT_PNG}" alt="TechnoPoint">
                    </a>`;
                },
            },
            { field: 'favorite', caption: '<div style="text-align: center">⭐</div>', size: '30px', hidden: true,
                editable: { type: 'checkbox' }
            },
            { field: 'visible', caption: '<div style="text-align: center">👁️</div>', size: '30px',
                style: 'text-align: center', hidden: true,
                editable: { type: 'checkbox' }
            },
        ],
        sortData: [ { field: 'recid', direction: 'asc' } ],
        records: PRODUCTS,
        searchData: SEARCH_DATA_VISIBLE,

        onClick: function(event) {
            // Не даем убирать выделение при повторном клике на выделенную строку
            var sel = this.getSelection();
            if (sel.length >= 1 && sel[0] == event.recid) {
                event.preventDefault();
                return;
            }

            // Не выполняем отображение цен при клике на колонки favorite или visible
            if (event.column != 5 && event.column != 6) {
                event.onComplete = function() {
                    // Сохранение последнего выделенного товара
                    localStorage.product_id = event.recid;

                    // Заполнение цен
                    w2ui.prices.clear();
                    w2ui.prices.add(PRODUCT_BY_PRICES[`${event.recid}`]);

                    // Рисование графика
                    fill_chart(w2ui.prices.records);
                }
            }
        },
        onSave: function(event) {
            // Checked favorite
            let favorites = localStorage.favorites == null ?
                [] : JSON.parse(localStorage.favorites);
            let invisible = localStorage.invisible == null ?
                [] : JSON.parse(localStorage.invisible);

            for (const value of event.changes) {
                if (value.favorite != undefined) {
                    // Если флаг стоит и значения нет среди сохраненных
                    if (value.favorite && !favorites.includes(value.recid)) {
                        favorites.push(value.recid);

                    // Если флаг убран и значение есть среди сохраненных
                    } else if (!value.favorite && favorites.includes(value.recid)) {
                        const index = favorites.indexOf(value.recid);
                        favorites.splice(index, 1);
                    }
                }

                if (value.visible != undefined) {
                    // Если флаг стоит и значение есть среди сохраненных
                    if (value.visible && invisible.includes(value.recid)) {
                        const index = invisible.indexOf(value.recid);
                        invisible.splice(index, 1);

                    // Если флаг убран и значения нет среди сохраненных
                    } else if (!value.visible && !invisible.includes(value.recid)) {
                        invisible.push(value.recid);
                    }
                }
            }

            localStorage.favorites = JSON.stringify(favorites);
            localStorage.invisible = JSON.stringify(invisible);
        },
        onRender: function(event) {
            event.onComplete = function() {
                // Даем время другим компонентам на рендеринг (#prices и #lineChart)
                // После кликом выделяем товар, что вызовет подгрузку цен и рисование графика
                setTimeout(() => {
                    let product_id = getLastSelectedProduct();
                    this.click(product_id);
                }, 100)
            }
        }
    });

    $('#prices').w2grid({
        name: 'prices',
        show: {
            footer: true,
        },
        sortData: [
            { field: 'recid', direction: 'desc' },
        ],
        columns: [
            { field: 'recid', caption: 'ID', size: '50px', hidden: true },
            { field: 'datetime', caption: 'Datetime', size: '100px', render: 'date:dd/mm/yyyy' },
            { field: 'price_dns', caption: 'DNS', size: '30%', render: 'float' },
            { field: 'price_techopoint', caption: 'TP', size: '30%', render: 'float' },
        ],
        onSelect: function(event) {
            event.onComplete = function () {
                if (LINE_CHART != null) {
                    LINE_CHART.update();
                }
            }
        }
    });

    // Layout
    var pstyle = 'border: 1px solid #dfdfdf; padding: 5px;';
    $('#layout').w2layout({
        name: 'layout',
        panels: [
            { type: 'main', style: pstyle, content: 'products', resizable: true },
            { type: 'right', size: '280px', style: pstyle, content: 'prices' },
            { type: 'bottom', size: '1000px', style: pstyle, content: 'bottom', resizable: true },
        ],
        onRender: function(event) {
            if (localStorage.layout_sizes == null) {
                return;
            }

            event.onComplete = function() {
                let layout_sizes = JSON.parse(localStorage.layout_sizes);
                this.sizeTo('bottom', layout_sizes['bottom']);
            }
        },
        onResizing: function(event) {
            let layout = this;
            waitForFinalEvent(
                function() {
                    let layout_sizes = {
                        bottom: layout.get('bottom').height,
                    };
                    localStorage.layout_sizes = JSON.stringify(layout_sizes);
                },
                1000, "layout.onResizing"
            );
        },
    });

    w2ui.layout.content('main', w2ui.products);
    w2ui.layout.content('right', w2ui.prices);
    w2ui.layout.content('bottom', `
        <div id="bottom">
            <div style="float: left; margin-right: 20px;">
                <input type="checkbox" id="cb_favorite" autocomplete="off">
                <label for="cb_favorite">Show favorite</label>

                <input type="checkbox" id="cb_visible" autocomplete="off">
                <label for="cb_visible">Visibility setting</label>
            </div>

            <div id="cb_toggle" style="float: left; display: none">
                <input type="checkbox" id="cb_toggle_favorite" autocomplete="off">
                <label for="cb_toggle_favorite">Toggle favorite</label>

                <input type="checkbox" id="cb_toggle_visible" autocomplete="off">
                <label for="cb_toggle_visible">Toggle visibility</label>
            </div>

            <div id="favorite_totals" style="float: left; display: none">
                <table>
                    <tr><td><b>Total DNS prices:</b></td><td class="dns_prices"></td></tr>
                    <tr><td><b>Total Technopoint prices:</b></td><td class="techopoint_prices"></td></tr>
                    <tr><td><b>Diff DNS and Technopoint:</b></td><td class="diff"><td></tr>
                </table>
            </div>

            <canvas id="lineChart"></canvas>
        </div>
    `);

    $('#cb_favorite').change(function() {
        if (this.checked) {
            w2ui.products.showColumn('favorite');
            showOnlyFavoriteProducts();
            selectLastProduct();
            showFavoriteTotals();

        } else {
            w2ui.products.hideColumn('favorite');
            w2ui.products.save();
            showOnlyVisibleProducts();
            selectLastProduct();
            $('#favorite_totals').hide();
        }
    });

    $('#cb_visible').change(function() {
        if (this.checked) {
            w2ui.products.showColumn('visible', 'favorite');
            w2ui.products.searchReset();
            selectLastProduct();
            $('#cb_toggle').show();

        } else {
            w2ui.products.hideColumn('visible', 'favorite');
            w2ui.products.save();
            showOnlyVisibleProducts();
            selectLastProduct();
            $('#cb_toggle').hide();
        }
    });

    $('#cb_toggle_favorite').change(function() {
        w2ui.products.set({ favorite: this.checked });
    });

    $('#cb_toggle_visible').change(function() {
        w2ui.products.set({ visible: this.checked });
    });

    // Save state legend to localStorage
    var legendClickHandler = function(e, legendItem) {
        // SOURCE: https://www.chartjs.org/docs/latest/configuration/legend.html
        var index = legendItem.datasetIndex;
        var ci = this.chart;
        var meta = ci.getDatasetMeta(index);

        // See controller.isDatasetVisible comment
        meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;

        // We hid a dataset ... rerender the chart
        ci.update();
        //

        // Save to localStorage
        let legend_hidden;
        if (localStorage.legend_hidden != null) {
            legend_hidden = JSON.parse(localStorage.legend_hidden);
        } else {
            legend_hidden = {};
        }
        legend_hidden[index] = meta.hidden;
        localStorage.legend_hidden = JSON.stringify(legend_hidden);
    };

    var LINE_CHART = null;

    function fill_chart(records) {
        let labels = [];
        let data_dns = [];
        let data_tp = [];

        for (const value of records) {
            // Наличие хотя бы одной из двух цен будет причиной для добавление метки на графике
            if (value.price_dns || value.price_techopoint) {
                let date_iso = value.datetime;
                labels.push(date_iso);

                if (value.price_dns) {
                    data_dns.push({
                        x: date_iso,
                        y: value.price_dns
                    });
                }

                if (value.price_techopoint) {
                    data_tp.push({
                        x: date_iso,
                        y: value.price_techopoint
                    });
                }
            }
        }

        let ctx = document.getElementById("lineChart").getContext("2d");

        if (LINE_CHART != null) {
            LINE_CHART.destroy();
        }

        LINE_CHART = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'DNS',
                        lineTension: 0,
                        borderColor: "rgb(246, 139, 31)",
                        data: data_dns,
                    },
                    {
                        label: 'TP',
                        lineTension: 0,
                        borderColor: "rgb(68, 44, 110)",
                        data: data_tp,
                    },
                ],
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'month',
                            tooltipFormat: 'DD/MM/YYYY HH:mm:ss',
                            displayFormats: {
                               month: 'DD/MM/YYYY',
                            }
                        },
                        distribution: 'linear'
                    }]
                },
                legend: {
                    onClick: legendClickHandler,
                }
            }
        });

        // По умолчанию, цены технопоинта не показывать
        LINE_CHART.data.datasets[1].hidden = true;
        LINE_CHART.update();

        // Read from localStorage
        if (localStorage.legend_hidden != null) {
            let legend_hidden = JSON.parse(localStorage.legend_hidden);
            for (const [key, value] of Object.entries(legend_hidden)) {
                LINE_CHART.data.datasets[key].hidden = value;
            }
            LINE_CHART.update();
        }
    }
});
