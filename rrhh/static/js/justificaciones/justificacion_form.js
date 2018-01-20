


$(function () {

    $("form").bind("keypress", function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    });
    


    $("#id_documento").keyup(function (e) {
        if (e.keyCode == 13) {
            buscarFuncionario();
        }
    });

    $("#id_tipo_marcacion").on("change", function(){
        changeHour();
    });

    $("#id_tipo_justificacion").on("change", function(){
        var tipo_justificacion  = $("#id_tipo_justificacion").val(); // om o fdh (Omision de marcacion o Fuera de hora)
        if (tipo_justificacion == "fdh"){
            $("#div_id_motivo_justificacion").show()
        }
        else{
            $("#id_motivo_justificacion").val("");
            $("#div_id_motivo_justificacion").hide()
        }

    })
});


function buscarFuncionario(){
    var documento = $('#id_documento').val();
    $.ajax({
        data: {
            documento: documento
        },
        url: '/vacaciones/solicitud/buscar_funcionario',
        type: 'get',
        success: function (data) {
            var funcionario = data.funcionario;
            $("#id_funcionario_nombre_completo").val(funcionario.fields.nombre + ' ' + funcionario.fields.apellido);
            $("#id_funcionario").val(funcionario.pk);
        },
        error: function (data) {
            $('.modal-funcionario-notfound').modal('show');
            $("#id_funcionario_nombre_completo").val("");
            $("#id_funcionario").val("");
        }
    })
}


function getFormattedDate(date) {
  var year = date.getFullYear();

  var month = (1 + date.getMonth()).toString();
  month = month.length > 1 ? month : '0' + month;

  var day = date.getDate().toString();
  day = day.length > 1 ? day : '0' + day;
  
  return day + '/' + month + '/' + year;
}

function changeHour(){
    var tipo_justificacion  = $("#id_tipo_justificacion").val(); // om o fdh (Omision de marcacion o Fuera de hora)
    var tipo_marcacion      = $("#id_tipo_marcacion").val();     // e o s (Entreda o salida)
    var date = new Date();
    var val = "";
    if ( tipo_marcacion == "e" ){
        val = getFormattedDate(date) + " 07:15";
        $("#id_fecha_hora").val( val );
    }
    else{
        if ( tipo_marcacion == "s" ){
            val = getFormattedDate(date) + " 15:00";
            $("#id_fecha_hora").val( val );
        }
        else
            $("#id_fecha_hora").val( "" );
    }
}
