
$(function () {
    $('.input-daterange input').each(function() {
        $(this).datepicker();
    });


    $("#btn-submit").click(function(){
        //$("form#form-marcacion-filter").submit();

        $.ajax({
            type: 'get',
            url: $('form#form-marcacion-filter').attr('action'),
            data: $('form#form-marcacion-filter').serialize(),
            success: function(data){
                var result = $(data).find("#panel-marcaciones");
                $("#panel-marcaciones").html(result);
            }
        });
    });



    $('.btn-print').click(function(){
        // var text = "Solicitud y Autorización de Vacaciones SPVL/RRHH/01";
        // $(".report-title").html( text.toUpperCase() );
        window.print();
    });

});