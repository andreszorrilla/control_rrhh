/**
 * Created by Leonel on 17/03/14.
 */
$(document).ready(function () {
    $('#menu').metisMenu();
    $.fn.datepicker.defaults.format = "dd/mm/yyyy";
    $.fn.datepicker.defaults.language = "es";
    $('[data-toggle="tooltip"]').tooltip();

    $('.btn-back').click(function(){
        window.history.back();
    });


});

/**
 * Cambia el valor de una clave en un query url
 * @param clave
 * @param valor
 * @returns {string} url resultante
 */
function cambiarQueryUrl(clave, valor){

    var query = window.location.search.substring(1);
    var vars = query.split("&");
    var objUrl = {}
    vars.forEach(function(v){
        var key_value = v.split("=");
        objUrl[key_value[0]] = key_value[1];
    });

    objUrl[clave] = valor
    objUrl['page'] = 1
    var new_url = '?';
    for(var i in objUrl){
        new_url +=  i + '=' + objUrl[i] + "&" ;
    }
    var new_url = new_url.substring(0, new_url.length-1);
    history.pushState('', '', new_url);
    return new_url;
}