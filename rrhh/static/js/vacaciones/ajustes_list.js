/**
 * Created by leonel on 1/08/14.
 */
$('#input-filtro').on('input', function() {
    var url = cambiarQueryUrl('filtro', $(this).val());

    $.get(url, function(data){
        var tabla = $(data).find('.table').html();
        var paginador = $(data).find('.pagination');
        $(".table").html(tabla);
        $(".pagination").html(paginador);
    });
});
