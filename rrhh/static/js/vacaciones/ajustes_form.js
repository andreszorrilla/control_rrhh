var x;


$("#id_anho").on("change", function(){

	var anho = $( this ).val();
	var id_funcionario = $("#id_id_funcionario").val();

	$.ajax({
			url: '/vacaciones/ajustes/detail/get_dias_libres/',
			type: 'get',
			data: {
				id_funcionario: id_funcionario,
				anho: anho
			},
			dataType: "json",
		    success: function(data){
		    	x = data;
		    	if( typeof(data.cantidad_dias) == "undefined" ){
		    		$("#id_libres").val("");
		    		$('#modal-message').modal({
						keyboard: false
					});
		    	}
		    	else
		    		$("#id_libres").val(data.cantidad_dias);
		    },
		    error: function(){
		    	alert("Error");
		    }		    
	});
});