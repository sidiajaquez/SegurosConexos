$(document).on('ready',inicio);

function inicio(){ //Inicializacion de variables y funciones
	$.ajaxSetup({
		beforeSend: function(xhr, settings){
			if (settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});	
	
	$('#btnActualizar').on('click',actualizarUsuario);
}

var actualizarUsuario = function(){ //Funcion para mandar a actualizar el password del usuario
	password1 = $('#txtPassword1').val();
	password2 = $('#txtPassword2').val();
	if (password1!='' && password2!=''){ //comprueba que no se encuentren vacias las cajas de texto
		if (password1 == password2){ //Comparar las dos contraseñas
			var datauser = {
					username:$("#txtNombreUsuario").val(),
					pw:password1
					};
			$.post('/SettingsUser/',{data:JSON.stringify(datauser)}, cbActualizacion);
		}else{
			alertify.alert('La verificación de la contraseña no coincide');
		}
	}else{
		alertify.alert('La contraseña no puede estar vacia');
	}
	return false;
}

var cbActualizacion = function(data){ //Call back de la funcion actualizar usuario
	alertify.alert(data.mensaje);
	$('#txtPassword1').val('');
	$('#txtPassword2').val('');
}