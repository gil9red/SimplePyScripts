// Licensed under the Apache License, Version 2.0.
// GitHub: https://github.com/silviubogan/jquery-autoclick-while-pressed
!function (a) {
    a.fn.autoclickWhilePressed = function (b) {
        var c = null,
        d = null,
        e = {
            intervalLength : 50,
            initialDelay : 300,
            eventToTrigger : "click"
        };

        if ("object" == typeof b)
            a.extend(e, b);

        var f = this;

        return this.on({
            'mousedown touchstart' : function () {
                d = setTimeout(function () {
                    c = setInterval(function () {
                        f.trigger(e.eventToTrigger)
                    }, e.intervalLength)
                }, e.initialDelay)
            },
            "mouseup mouseleave touchend" : function () {
                if (null !== d)
                    clearTimeout(d);

                if (null !== c)
                    clearInterval(c);
            }
        })
    }

}(jQuery);
