$(function(){
    $('#fecha_datepicker').parent(this).datepicker({
            clearBtn: true,
            todayBtn: "linked"
    }).on('changeDate', function (ev) {
        $('#id_fecha').val(ev.format(0));
    });
});