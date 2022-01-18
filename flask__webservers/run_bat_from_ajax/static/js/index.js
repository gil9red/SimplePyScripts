$(document).ready(function() {
    $('button.os_startfile').click(function() {
        let script_name = $(this).text();
        console.log(script_name);

        $.ajax({
            url: '/os_startfile/' + script_name,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                console.log(data);
            }
        });
    });

    $('button.subprocess').click(function() {
        let script_name = $(this).text();
        console.log(script_name);

        $.ajax({
            url: '/subprocess/' + script_name,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $('#subprocess_result').text(data.result);
            }
        });
    });
});
