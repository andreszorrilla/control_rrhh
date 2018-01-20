/**
 * Created by lgamarra on 17/03/14.
 */

function configuracionAntiguedadList() {
    $.get("/configuraciones/antiguedad/", function (result) {
        $('#content').html(result);
    });
}

function configuracionAntiguedadCreateGet() {
    $.get("/configuraciones/antiguedad/create", function (data) {
        $('#content').html(data);
        $('#btn-antiguedad-list').click(configuracionAntiguedadList);
        configuracionAntiguedadCreatePost();
    });

}

function configuracionAntiguedadCreatePost() {
    $('#form-antiguedad').submit(function () {
        var data = $('#form-antiguedad').serialize();
        $.post('/configuraciones/antiguedad/create', data, function (result) {
            $('#content').html(result);
            $('#btn-antiguedad-list').click(configuracionAntiguedadList);
            configuracionAntiguedadCreatePost();
        });
        return false;
    });
}

function configuracionAntiguedadDetail(id) {
    $.get('/configuraciones/antiguedad/detail/' + id, function (result) {
        $('#content').html(result);
        $('#btn-antiguedad-list').click(configuracionAntiguedadList);

    });
}

function configuracionAntiguedadUpdateGet(id) {
    $.get('/configuraciones/antiguedad/update/' + id, function (result) {
        $('#content').html(result);
        $('#btn-antiguedad-list').click(configuracionAntiguedadList);
        configuracionAntiguedadUpdatePost();
    });
}

function configuracionAntiguedadUpdatePost() {
    $('#form-antiguedad').submit(function () {
        var id = $('#antiguedad-id').val();
        var data = $('#form-antiguedad').serialize();
        $.post('/configuraciones/antiguedad/update/' + id, data, function (result) {
                $('#content').html(result);
                $('#btn-antiguedad-list').click(configuracionAntiguedadList);
                configuracionAntiguedadUpdatePost();
        });
        return false;
    });
}

function configuracionAntiguedadDeleteModal(id) {
    $('#id-antiguedad').val(id);
    $('.modal-delete').modal('show');
    configuracionAntiguedadDeleteConfirm();
}

function configuracionAntiguedadDeleteConfirm() {
    $('#form-delete-confirm').submit(function () {
        var data = $('#form-delete-confirm').serialize();
        var id = $('#id-antiguedad').val();
        $.post('/configuraciones/antiguedad/delete/' + id, data, function (result) {
            $('.modal-delete').modal('hide');
            $('.modal-delete').on('hidden.bs.modal', function (e) {
                $('#content').html(result);
            })
        });
        return false;
    });
}

function configuracionAntiguedadPagination(page) {
    $.get("/configuraciones/antiguedad/?page=" + page, function (result) {
        $('#content').html(result);
    });


}
