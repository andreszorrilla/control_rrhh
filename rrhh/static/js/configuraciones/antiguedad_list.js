/**
 * Created by lgamarra on 15/04/14.
 */

$('.btn-borrar').click(function () {
    $('.modal-delete').modal('show');
    $('#id-borrar').val($(this).data("id"));
});

$('#form-delete-confirm').submit(function () {
    var data = $('#form-delete-confirm').serialize();
    var id = $('#id-borrar').val();
    $.post('delete/' + id, data, function (result) {
        $('.modal-delete').modal('hide');
        $('.modal-delete').on('hidden.bs.modal', function (e) {
            location.reload();
        })
    });
    return false;
});
