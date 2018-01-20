$(function(){
	$(".a-anular").click(function(){
		var link = $(this).attr("link");
		$(".modal-anular").find("#form-anular-confirm").attr("action", link);
		$(".modal-anular").modal();
	});


	$(".modal-anular").on("hidden.bs.modal", function(){		
		$(".modal-anular").find("#form-anular-confirm").attr("action", "");
	});


	$('.input-daterange input').each(function() {
		$(this).datepicker();
	});

	$('.btn-print').click(function(){
	    window.print();
	});
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




