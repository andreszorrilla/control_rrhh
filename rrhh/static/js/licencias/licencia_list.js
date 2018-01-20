/**
 * Created by lgamarra on 15/04/14.
 */
$('.a-anular').click(function () {
    $('.modal-anular').modal('show');
    $('#id-anular').val($(this).data("id"));

});

$('#form-anular-confirm').submit(function () {
    var data = $('#form-anular-confirm').serialize();
    var id = $('#id-anular').val();
    $.get('../solicitud/anular/' + id, data, function (result) {
        $('.modal-anular').modal('hide');
        $('.modal-anular').on('hidden.bs.modal', function (e) {
            location.reload();
        })
    });
    return false;
});


$('#input-filtro').on('input', function() {
    var url = cambiarQueryUrl('filtro', $(this).val());
    $.get(url, function(data){
        var tabla = $(data).find('.table').html();
        var paginador = $(data).find('.pagination');
        $(".table").html(tabla);
        $(".pagination").html(paginador);
    });
});


