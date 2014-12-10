$(document).on('ready',inicio);

function inicio(){ // Función que inicia las variables y los eventos de los controles del formulario listado de cotizaciones.
	activarMenu();
	$("#btnCancelarSolicitudEndoso").on('click',cancelarSolicitudEndoso);
	$("#btnGuardarSolicitudEndoso").on('click',guardarSolicitudEndoso);
	$("#btnImprimirSolicitudEndoso").on('click',imprimirSolicitudEndoso);
}

var activarMenu = function() { // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

var imprimirSolicitudEndoso = function(){ //Crea la impresion en pdf para la solicitud de endoso
	window.open('/SolicitudEndosoImpresion/'+$("#varIdSolicitudEndoso").val());
	return false;
}

var cancelarSolicitudEndoso = function(){ //Funcion que redirecciona la solicitud de endoso al listado por motivo de cancelacion
	location.href = '/ListadoSolicitudEndoso/';
	return false;
}

var guardarSolicitudEndoso = function() { //Funcion que guarda la Solicitud de endoso
	if(pasarComprobaciones()){
		Dajaxice.Endoso.guardar_solicitud_endoso(Dajax.process,{'frmSolicitudEndoso':$('#formulario_solicitud_endoso').serialize(true)});
	}else{
		alertify.alert("Se requieren datos para guardar");
	}
	return false;
}

var pasarComprobaciones = function() { //Validacion de los datos a capturar
	if ($("#TipoEndoso").val() && $("#Observaciones").val()){
		return true;
	}
	return false;
}

var mensajeSolicitud = function(numeroSolicitud){ //Funcion que recibe el folio de la solicitud de endoso de la funcion Dajaxice.Endoso.guardar_solicitud_endoso para mostrarla en un alert
	if (numeroSolicitud){
		alertify.set({ labels: {
		    ok     : "Si",
		    cancel : "No"
		}});
		$("#varIdSolicitudEndoso").val(numeroSolicitud[1]);
		$("#btnImprimirSolicitudEndoso").attr('disabled',false);
		$("#btnCancelarSolicitudEndoso").text('Salir');	
		$("#btnGuardarSolicitudEndoso").attr('disabled',true);
		alertify.confirm('Solicitud Guardada con el Folio: '+ numeroSolicitud[0] + ' ¿Desea imprimir la Solicitud?', function (e) {
		    if (e) {
		    	imprimirSolicitudEndoso();
		    }
		});
	}else{
		alertify.alert('Error al guardar contacte al administrador del sistema');
	}
	return false;
}