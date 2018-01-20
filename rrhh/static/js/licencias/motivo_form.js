$(function () {
	/*$("input[name='imputable']").on("change", function(){
		if ( $(this).val() == "True" ){
			$("#div_id_tipo_motivo").hide();
			$("#div_id_duracion").hide();
			$("#id_duracion").val(0);
		}
		else{
			$("#div_id_tipo_motivo").show();
			$("#div_id_duracion").show();
		}
});/*/
	$("#id_tipo_motivo").on("change", function(){
		var cond = $(this).val() == "permiso";
		$("#id_duracion").attr("disabled", cond);
		$("#id_duracion").val("");

	});
});


