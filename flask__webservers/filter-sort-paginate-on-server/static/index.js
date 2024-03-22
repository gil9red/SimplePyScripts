$(function() {
    new DataTable('table', {
        ajax: 'api/get_items',
        rowId: 'id',
        serverSide: true,
        processing: true,
        lengthMenu: [
            [5, 10, 25, 50, -1],
            ["5 records", "10 records", "25 records", "50 records", "All records"]
        ],
        columns: [
            { name: 'id', data: 'id', title: 'Id', },
            { name: 'name', data: 'name', title: 'Name' },
            { name: 'description', data: 'description', title: 'Description', },
            { name: 'command', data: 'command', title: 'Command', }
        ],
        order: [
            // Сортировка по убыванию id
            [0, "desc"],
        ],
    });
});
