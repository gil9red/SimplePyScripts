var socket = io();

function create_task_el(msg) {
    let task_el = $("#" + msg.id);
    if (task_el.length != 0) {
        return task_el;
    }

    let template = `
        <div id="${msg.id}" class="task" data-status="${msg.status}">
            <table>
                <tr><td>Command:</td><td class="task-command">${msg.command}</td></tr>
                <tr><td>Id:</td><td class="task-id">${msg.id}</td></tr>
                <tr><td>Status:</td><td class="task-status">${msg.status}</td></tr>
                <tr><td>Process id:</td><td class="task-process-id">${msg.process_id}</td></tr>
                <tr><td>Process return code:</td><td class="task-process-return-code">${msg.process_return_code}</td></tr>
                <tr><th>STDOUT</th><th>STDERR</th></tr>
                <tr>
                    <td><textarea class="log-out"></textarea></td>
                    <td><textarea class="log-err"></textarea></td>
                </tr>
            </table>
        </div>
    `;
    task_el = $(template)
    $("#tasks").append(task_el);
    return task_el;
}

function add_to_log(log, text) {
    log.append(text);
    log[0].scrollTop = log[0].scrollHeight;
}

socket.on('update_task', function(msg, callback) {
    console.log("msg:", msg);

    let task_el = create_task_el(msg);

    if (msg.command != null) {
        task_el.find(".task-command").text(msg.command);
    }

    if (msg.status != null) {
        task_el.find(".task-status").text(msg.status);
        task_el.attr("data-status", msg.status);
    }

    if (msg.process_id != null) {
        task_el.find(".task-process-id").text(msg.process_id);
    }

    if (msg.process_return_code != null) {
        task_el.find(".task-process-return-code").text(msg.process_return_code);
        task_el.attr("data-process-return-code", msg.process_return_code);
    }

    if (msg.stdout_add != null) {
        let log = task_el.find(".log-out");
        add_to_log(log, msg.stdout_add);
    }
    if (msg.stderr_add != null) {
        let log = task_el.find(".log-err");
        add_to_log(log, msg.stderr_add);
    }

    if (callback) {
        callback();
    }
});

function run() {
    socket.emit('run', {command: $("#commands").val()});
}