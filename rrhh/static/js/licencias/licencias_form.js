var a;


$(document).ready(function(){

    $('#id_fecha_inicio, #id_fecha_fin, #id_fechas').filter(
        function(){
            return $(this).val() == ''
        })
        .closest('.form-group:not(.has-error)').hide();

    var size =  $('#id_fecha_inicio, #id_fecha_fin, #id_fechas').closest('.form-group').filter(function() {
                    return $(this).is(":visible");
                }).size()

    /*
    if (size == 0){
        //$("#id_motivo").val('');
    }
    */
});

$(function () {
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
        todayBtn: "linked"
    }).on('changeDate', function (ev) {
        var dias, fecha_final;
        $('#id_fecha_inicio').val(ev.format(0));
        dias = $('#id_cantidad_dias').val();

        if (dias != ""){
            sumarFecha( parseInt(dias), $("#id_fecha_inicio").val() );
        }
    });


    //fechas de vacaciones cargadas en el datepicker
    var fechas_cargadas = $("#id_fechas").val();
    $('#fechas_datepicker').parent(this).attr('data-date', fechas_cargadas);
    //datepicker para cargar dias de vacaciones

    $.ajax({
        url: "/licencias/feriado/json",
        dataType: "json",
        success: function(data){
            datepickerFechas(data);
        },
        error: function(){
            alert("data[0]");
        }
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

    $('#documento_search').parent(this).click(solicitudBuscarFuncionario);

    $('.modal-funcionario-notfound').on('shown.bs.modal', function () {
        $('#btn-modal-aceptar').focus();
    });
    $('.modal-funcionario-notfound').on('hidden.bs.modal', function () {
        $('#id_documento').focus();
    });


    
    $("#id_fecha_inicio").on("change", function(){
        var dias = $("id_cantidad_dias").val();
        sumarFecha( parseInt(dias), $(this).val() );
    })

    $("#id_cantidad_dias").on('change', function(){
        var fecha = $("#id_fecha_inicio").val();
        var cantidad_dias = $(this).val();
        if (fecha != ""){
            sumarFecha( parseInt(cantidad_dias), fecha);                    
        } 
    });

    $("#id_motivo").on('change', function(){
    	var motivo;
        motivo = $("#id_motivo").val();

        if (motivo == ""){
            $('#id_cantidad_dias').val("");
        }

        $.ajax({
    		url: '/licencias/obtener_motivo',
        	type: 'get',
        	data: {id_motivo: motivo},
        	dataType: "json",
        	success: function (data) {
                var fecha, fecha_final;
                a = data;


                if (data["tipo_motivo"] != "permiso"){
                    $("#id_cantidad_dias").val(data["cantidad_dias"]);
                    $("#id_tipo_documento").val("licencia");
                }
                else{
                    $("#id_cantidad_dias").val("");
                    $("#id_tipo_documento").val("permiso");
                }


                if (data["tipo_motivo"] == "corridos"){
                    $("#fechas_datepicker").val("");
                    $("#div_id_fechas").hide();
                    $("#div_id_fecha_inicio").show();
                    $("#div_id_fecha_fin").show();
                }

                else{
                    $("#fechas_datepicker").val("");
                    $("#div_id_fechas").show();
                    $("#div_id_fecha_inicio").hide();
                    $("#div_id_fecha_fin").hide();
                    
                }


                /*
                if (data["imputable"]){
                    $("#id_tipo_documento").val("permiso");
                }
                else{
                    $("#id_tipo_documento").val("licencia");
                }

                $("#id_fecha_fin").attr("readonly", !data["imputable"]);

                $("#id_cantidad_dias").attr("readonly", !data["imputable"]);
                $('#id_cantidad_dias').val(data.cantidad_dias);
                    

                fecha = $("#id_fecha_inicio").val();
                if (fecha != ""){
                    sumarFecha( parseInt(data.cantidad_dias), fecha);                    
                } */

	        },
	        error: function (data) {
	        	
	        }
    	});
    });


    $("#fecha_fin_datepicker").parent(this).datepicker({
        todayHighlight: true,
        todayBtn: "linked",
        minDate: -1, maxDate: "+1M +10D"
    }).on('changeDate', function (ev) {
        var dias, fecha_final, fecha;
        var doc;

        doc = $("#id_tipo_documento").val();
        fecha = $("#id_fecha_inicio").val();

        if (doc == "licencia") {
            return;
        };

        $('#id_fecha_fin').val(ev.format(0));

        if (fecha != "" && ev.format(0) != ""){
            $("#id_cantidad_dias").val( restaFechas(fecha, ev.format(0)) );
        }
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
            $("#id_nombre_funcionario").val(funcionario.fields.nombre + ' ' + funcionario.fields.apellido);
            $("#id_id_funcionario").val(funcionario.pk);
            $("#id_funcionario").val(funcionario.pk);

        },
        error: function (data) {
            $('.modal-funcionario-notfound').modal('show');
            $("#id_funcionario").val("");
            $("#id_id_funcionario").val("");
            $("#id_cantidad_dias_restantes").val("");
        }
    })
}
/*
function sumarFecha(d, fecha){
    var Fecha = new Date();
    var sFecha = fecha || (Fecha.getDate() + "/" + (Fecha.getMonth() +1) + "/" + Fecha.getFullYear());
    var sep = sFecha.indexOf('/') != -1 ? '/' : '-'; 
    var aFecha = sFecha.split(sep);
    var fecha = aFecha[2]+'/'+aFecha[1]+'/'+aFecha[0];
    fecha= new Date(fecha);
    fecha.setDate(fecha.getDate()+parseInt(d));
    var anno=fecha.getFullYear();
    var mes= fecha.getMonth()+1;
    var dia= fecha.getDate();
    mes = (mes < 10) ? ("0" + mes) : mes;
    dia = (dia < 10) ? ("0" + dia) : dia;
    var fechaFinal = dia+sep+mes+sep+anno;
    return (fechaFinal);
}*/

function sumarFecha(dias, fecha){
    var motivo_text = $("#id_motivo option:selected").text();
    var text = motivo_text.split(" ").pop().slice(0,-1);
    var fecha_obtenida = "";
    if (text != "" && text != "--------"){
        $.ajax({
            url: '/licencias/crear_fecha_final',
            type: 'get',
            data: {dias: dias, fecha: fecha, tipo_motivo: text},
            dataType: "json",
            success: function (data) {
                $("#id_fecha_fin").val( data["fecha_fin"] );
            }
        });
    }
    return fecha_obtenida;
}


function restaFechas(f1,f2){
    var aFecha1 = f1.split('/'); 
    var aFecha2 = f2.split('/'); 
    var fFecha1 = Date.UTC(aFecha1[2],aFecha1[1]-1,aFecha1[0]); 
    var fFecha2 = Date.UTC(aFecha2[2],aFecha2[1]-1,aFecha2[0]); 
    var dif = fFecha2 - fFecha1;
    var dias = Math.floor(dif / (1000 * 60 * 60 * 24)); 
    return dias;
}

open("")

function containsDate(date, arrayDates){
    var i;
    var fecha;
    for (var i = 0; i < arrayDates.length; i++) {
        fecha = new Date(arrayDates[i].fields.fecha) ;
        fecha.setDate(fecha.getDate() + 1)

        if ( date.getMonth() == fecha.getMonth() && date.getDate() == fecha.getDate() ){
            console.log(date.toString() + "--> " + date.getMonth() + " - " + date.getDate());
            console.log(fecha.toString() + "--> " + fecha.getMonth() + " - " + fecha.getDate());
            return true;
        }
    };
    return false;
}


function datepickerFechas(datesArray){
    $('#fechas_datepicker').parent(this).datepicker({
        multidate: true,
        multidateSeparator: ";",
        daysOfWeekDisabled: [], // PARA DESHABILITARD DOMINGO, AGREGAR CERO AL ARRAY
        clearBtn: true,
        todayBtn: "linked",
        todayHighlight: true,
        beforeShowDay: function(date){
            return{
                enabled: !containsDate(date, datesArray)
            }
        } 
    }).on('changeDate', function (ev) {

        $('#id_fechas').val(ev.dates.length);
        $('#id_fechas').val("");

        var dates = [];
        var dias = $("#id_cantidad_dias").val();        


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
                $('#id_fechas').val(dates[i]);
            else
                $('#id_fechas').val($('#id_fechas').val() + ";" + dates[i]);
        }

        //imprime la cantidad de dias seleccionados
        if ( $("#id_tipo_documento").val() == "permiso" ) {
            $('#id_cantidad_dias').val(dates.length);
        };

    });
}