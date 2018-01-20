$(function(){
	$(".has-icon").find(".form-control-feedback").each(function(){
		var label_id = $(this).attr("label_id");
		console.log(label_id);
		if (label_id == "id_username"){
			$(this).addClass("glyphicon-user");
		}
		if (label_id == "id_password"){
			$(this).addClass("glyphicon-asterisk");
		}
	});
});


alert("hola");