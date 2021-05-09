DEBUG = false;

function send_ajax(url, data, callbackFunc) {
    if (DEBUG) console.log(data);
    if (DEBUG) console.log(JSON.stringify(data));

    $.ajax({
        url: url,
        method: "POST",
        data: JSON.stringify(data),

        contentType: "application/json",
        dataType: "json",  // тип данных загружаемых с сервера

        success: function(response) {
            if (DEBUG) console.log(response);
            if (DEBUG) console.log(JSON.stringify(response));

            if (callbackFunc != null) {
                callbackFunc(url, data, response);
            }
        },
    });
}

function pointerEventToXY(e) {
    var out = {
        x : 0,
        y : 0
    };

    if (e.type.startsWith("touch")) {
        var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
        out.x = touch.pageX;
        out.y = touch.pageY;
    }

    if (e.type.startsWith("mouse")) {
        out.x = e.pageX;
        out.y = e.pageY;
    }

    out.x = Math.round(out.x);
    out.y = Math.round(out.y);
    return out;
};

function on_change_mouse_mode(is_joystick) {
    if (is_joystick == null) {
        is_joystick = $('#switch_mouse_mode').prop('checked');
    }

    localStorage.switch_mouse_mode = is_joystick;

    $('#joystick_wrapper').toggle(is_joystick);
    $('#mouse_area').toggle(!is_joystick);
}

function init_switch_stream_mode() {
    var CURRENT_URL_OR_DATA = null;
    var CURRENT_SCREENSHOT_TIME = 0;

    function set_stream_mode(value) {
        send_ajax('/set_stream_mode', {'value': value});
    }

    function set_screenshot_canvas(url_or_data) {
        if (CURRENT_URL_OR_DATA == url_or_data) {
            return;
        }

        CURRENT_URL_OR_DATA = url_or_data;

        let screenshot_canvas = $('#screenshot_canvas');
        screenshot_canvas.css('background-image', 'url(' + url_or_data + ')');
        screenshot_canvas.css('background-repeat', 'no-repeat');
        screenshot_canvas.css('background-size', 'contain');
        screenshot_canvas.css('background-position', 'center center');
    }

    let switch_stream_mode = $('#switch_stream_mode');

    let is_checked = switch_stream_mode.prop('checked');
    set_stream_mode(is_checked);

    switch_stream_mode.change(function() {
        set_stream_mode(this.checked);
    });

    // Периодический запрос скриншота при включенном режиме
    setInterval(
        () => {
            let is_checked = switch_stream_mode.prop('checked');
            if (is_checked) {
                send_ajax('/get_screenshot', null, (url, data, response) => {
                    // Контроль последовательности скриншотов, показываем всегда последний
                    // Это нужно из-за гонки потоков, из-за которой возможно получить старый
                    // скриншот позже текущего
                    if (response.time <= CURRENT_SCREENSHOT_TIME) {
                        return;
                    }
                    CURRENT_SCREENSHOT_TIME = response.time;

                    // Если на этом моменте флаг еще стоит
                    if (switch_stream_mode.prop('checked')) {
                        set_screenshot_canvas(response.img_base64);
                    }
                });
            } else {
                set_screenshot_canvas('');
            }
        },
        100
    );
}

function init_control_switch_mouse_mode() {
    // NOTE: On android Chrome not auto restore checked value after refresh page
    if (localStorage.switch_mouse_mode != null) {
        let checked = localStorage.switch_mouse_mode == "true";
        $('#switch_mouse_mode').bootstrapToggle(checked ? 'on' : 'off');
    }

    $('#switch_mouse_mode').change(function() {
        let is_joystick = $(this).prop('checked');
        on_change_mouse_mode(is_joystick);
    });

    let joystickEl = $('#joystick');
    joystickEl.width(joystickEl.parent().width());
    joystickEl.height(joystickEl.parent().height());

    // Actualize mouse mode
    on_change_mouse_mode();

    var joystick = nipplejs.create({
        zone: joystickEl.get(0),
        color: 'darkgreen',
    });
    let _press_pos = null;
    let _last_pos = null;
    let _joystick_timer = null;
    joystick.on('start end', function(e, data) {
        _press_pos = data.position;
        _last_pos = _press_pos;

        clearInterval(_joystick_timer);

        if (e.type == 'start') {
            _joystick_timer = setInterval(() => {
                let relative_x = Math.floor(_last_pos.x - _press_pos.x);
                let relative_y = Math.floor(_last_pos.y - _press_pos.y);
                if (relative_x == 0 && relative_y == 0) {
                    return;
                }

                console.log("joystick", _press_pos, _last_pos, (relative_x + 'x' + relative_y));

                var data = {"relative_x": relative_x, "relative_y": relative_y};
                send_ajax("/mouse_move", data);

            }, 100);
        }
    }).on('move', function(e, data) {
        _last_pos = data.position;
    });
}

function init_control_handlers() {
    function create_bubble(pos, size) {
        let bubble = $('<div class="bubble"></div>');
        bubble.css({
            left: pos.x - (size / 2),
            top: pos.y - (size / 2),
            width: size + 'px',
            height: size + 'px',
        });

        setTimeout(() => bubble.remove(), 2000);

        return bubble;
    }

    $("#mouse_left").click(function() {
        var data = {"button": "left"};
        send_ajax("/mouse_click", data);
    });

    $("#mouse_right").click(function() {
        var data = {"button": "right"};
        send_ajax("/mouse_click", data);
    });

    $(".key_control").click(function() {
        var data = {"key": $(this).attr("value")};
        send_ajax("/key_click", data);
    });

    $("#mouse_wheel_up").click(function() {
        var data = {"down": false};
        send_ajax("/scroll", data);
    });

    $("#mouse_wheel_down").click(function() {
        var data = {"down": true};
        send_ajax("/scroll", data);
    });

    $("#button_show_cursor_as_target").click(function() {
        send_ajax("/show_cursor_as_target");
    });

    $("#button_full_black_screen").click(function() {
        send_ajax("/full_black_screen");
    });

    // Глобальная переменная-флаг для работы c событиями touch
    let _is_touch = false;
    let _press_pos = null;
    let _last_send_pos = {x: null, y: null};
    let _last_time_send_pos = null;
    const _DELAY_BEFORE_SEND_POS = 75;

    let debug = false;
    if (debug) {
        let log = $("<div id='log'/>");
        $("#mouse_area").append(log);
    }
    let draw_bubble = true;

    $("#mouse_area").on("touchstart touchmove touchend mousemove mousedown mouseup mouseleave", function(e) {
        // https://developer.mozilla.org/en-US/docs/Web/API/Touch_events/Supporting_both_TouchEvent_and_MouseEvent
        if (_is_touch == false && e.type.startsWith("touch")) {
            _is_touch = true;
        }

        // События mouse тоже возможны при событиях touch, но нам желательно только с одним видом событий
        // работать, поэтому если были замечены touch-события, то mouse будут отменяться
        if (e.type.startsWith("mouse") && _is_touch) {
            e.preventDefault();
            return;
        }

        let pos = pointerEventToXY(e);

        if (debug) {
            log.text(JSON.stringify(pos));
            console.log(e.type, pos);
        }

        switch (e.type) {
            case "touchstart":
            case "mousedown": {
                _press_pos = pos;
                _last_send_pos.x = null;
                _last_send_pos.y = null;

                if (draw_bubble) {
                    $("#mouse_area").append(
                        create_bubble(pos, 40)
                    );
                }

                if (debug) {
                    console.log(e.type, _press_pos);
                }
                break;
            }

            case "touchend":
            case "mouseup":
            case "mouseleave":
            case "mouseout": {
                _press_pos = null;
                break;
            }

            case "touchmove":
            case "mousemove": {
                if (_press_pos == null) {
                    break;
                }

                if (_last_time_send_pos != null) {
                    if ((new Date() - _last_time_send_pos) < _DELAY_BEFORE_SEND_POS) {
                        break;
                    }
                }
                if (_last_send_pos.x == null || _last_send_pos.y == null) {
                    _last_send_pos.x = pos.x;
                    _last_send_pos.y = pos.y;
                }

                if (draw_bubble) {
                    $("#mouse_area").append(
                        create_bubble(pos, 40)
                    );
                }

                let relative_x = Math.floor(pos.x - _last_send_pos.x);
                let relative_y = Math.floor(pos.y - _last_send_pos.y);
                if (debug) {
                    console.log(e.type, _press_pos, pos, _last_send_pos, (relative_x + 'x' + relative_y));
                }

                _last_send_pos.x = pos.x;
                _last_send_pos.y = pos.y;
                _last_time_send_pos = new Date();

                let data = {relative_x: relative_x, relative_y: relative_y};
                send_ajax("/mouse_move", data);

                break;
            }
        }
    });
}

$(document).ready(function() {
    init_control_switch_mouse_mode();
    init_control_handlers();
    init_switch_stream_mode();
});
