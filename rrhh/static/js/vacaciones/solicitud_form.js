/**
 * Created by lgamarra on 15/04/14.
 */


var feriadosAjax;
var x;
var d; 
function containsDate(date, arrayDates){
    var i;
    var fecha;
    for (var i = 0; i < arrayDates.length; i++) {
        fecha = new Date(arrayDates[i].fields.fecha) ;
        fecha.setDate(fecha.getDate() + 1)

        if ( date.getMonth() == fecha.getMonth() && date.getDate() == fecha.getDate() ){
            return true;
        }
    };
    return false;
}


$(function () {

    feriadosAjax = $.ajax({
        url: "/licencias/feriado/json",
        dataType: "json",
        success: function(data){
            x = data;    
            //fechas de vacaciones cargadas en el datepicker
            var fechas_cargadas = $("#id_dias").val();
            $('#dias_datepicker').parent(this).attr('data-date', fechas_cargadas);
            //datepicker para cargar dias de vacaciones
            $('#dias_datepicker').parent(this).datepicker({
                multidate: true,
                multidateSeparator: ";",
                daysOfWeekDisabled: [],
                clearBtn: true,
                todayBtn: "linked",
                todayHighlight: true,
                beforeShowDay: function(date){
                    d = date;
                    return{
                        enabled: !containsDate(date, data)
                    }
                } 
                
            }).on('changeDate', function (ev) {
                $('#id_cantidad_dias').val(ev.dates.length);
                $('#id_dias').val("");
                var dates = [];
                //obtiene todas las fechas selecionadas
                for (var i = 0; i < ev.dates.length; i++) {
                    dates[i] = ev.format(i);
                }
                //ordena las fechas
                dates.sort(function (a, b) {
                    var aa = a.split('/').reverse().join(),
                        bb = b.split('/').reverse().join();
                    return aa < bb ? -1 : (aa > bb ? 1 : 0);
                });
                //imprime las fechas seleccionadas
                for (var i = 0; i < dates.length; i++) {
                    if (i == 0)
                        $('#id_dias').val(dates[i]);
                    else
                        $('#id_dias').val($('#id_dias').val() + ";" + dates[i]);
                }
                //imprime la cantidad de dias seleccionados
                $('#id_cantidad_de_dias').val(dates.length);

            });

        },
        error: function(){
            alert("data[0]");
        }
    });

    $('#id_documento').focus();
    if ($('#id_fecha').val() == '') {
        var fecha_hoy = (moment().format('DD/MM/YYYY'));
        $('#id_fecha').val(fecha_hoy);
    }

    //fecha de hoy seleccionada en el datepicker
    //date picker para la fecha de solicitud
    $('#fecha_datepicker').parent(this).attr('data-date', $('#id_fecha').val());
    $('#fecha_datepicker').parent(this).datepicker({
        todayHighlight: true,
        todayBtn: "linked",
        
    }).on('changeDate', function (ev) {
        $('#id_fecha').val(ev.format(0));
        $('id_fecha_inicio').val(ev.format(0));
    });
    

    //desactiva el enter del formulario
    $("form").bind("keypress", function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    });

    //busqueda de funcionario
    $("#id_documento").keyup(function (e) {
        if (e.keyCode == 13) {
            solicitudBuscarFuncionario();
        }
    });

    $('#buscar_documento').parent(this).click(solicitudBuscarFuncionario);

    $('.modal-funcionario-notfound').on('shown.bs.modal', function () {
        $('#btn-modal-aceptar').focus();
    });
    $('.modal-funcionario-notfound').on('hidden.bs.modal', function () {
        $('#id_documento').focus();
    });


});

function solicitudBuscarFuncionario() {
    var documento = $('#id_documento').val();
    $.ajax({
        data: {
            documento: documento
        },
        url: '/vacaciones/solicitud/buscar_funcionario',
        type: 'get',
        success: function (data) {
            var funcionario = data.funcionario;
            $("#id_funcionario").val(funcionario.fields.nombre + ' ' + funcionario.fields.apellido);
            $("#id_id_id_funcionario").val(funcionario.pk);

            $("#id_dias_restantes").val(data.total_libres);

        },
        error: function (data) {
            $('.modal-funcionario-notfound').modal('show');
            $("#id_funcionario").val("");
            $("#id_id_id_funcionario").val("");
            $("#id_dias_restantes").val("");
        }
    })
}
