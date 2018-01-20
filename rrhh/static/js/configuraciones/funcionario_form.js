/**
 * Created by lgamarra on 15/04/14.
 */
$(function () {
    actualizarLista();
    
    $('#id_nombre').focus();
    $('#fecha_ingreso_datepicker').parent(this).datepicker({autoclose: true}).on('changeDate', function (ev) {
        $('#id_fecha_ingreso').val(ev.format(0));
    });


    $('#fecha_nacimiento_datepicker').parent(this).datepicker({autoclose: true}).on('changeDate', function (ev) {
        $('#id_fecha_nacimiento').val(ev.format(0));
    });

    $("#id_seccion").on("change", function(){
    	actualizarLista();
    });
});



function actualizarLista(){
    var id = $("#id_seccion").val();
        $("#id_cargo").html("<option selected='selected'>---------</option>");
        if (id == ""){          
            return;
        }
        $.ajax({
            url: "/configuraciones/cargo/seccion/" + id,
            datatype: "json",
            success: function(data){
                var i;
                for (var i = 0; i < data.length; i++) {
                    $("#id_cargo").append("<option value='" + data[i].pk + "'>" + data[i].fields.nombre + "</i>")
                    //console.log(data[i].pk + "  " +data[i].fields.nombre);
                };
            }
        });
}