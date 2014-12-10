$(document).on('ready',inicio);

function inicio(){ // Función que inicia las variables y los eventos de los controles.
	$("#btnGuardarEndoso").on('click', guardarEndosoCancelacion);
	$("#btnVolverListadoEndoso").on("click", regresarListadoEndosoCancelacion);
}

var guardarEndosoCancelacion = function() { // Función que nos permite guardar el endoso de cancelación llamando la función guardar_endoso_cancelacion de la clase ajax.
	
	alertify.confirm('Esto cancelará la constancia ¿Desea continuar?', function (e) {
	    if (e) {	    	
	    	Dajaxice.Endoso.guardar_endoso_cancelacion(Dajax.process,{'idConstancia':$('#varIdConstancia').val(), 'idSolicitudEndoso':$('#varIdSolicitudEndoso').val(), 'monto':$("#varMontoCancelacion").val(), 'tipoEndoso':$("#varTipoEndoso").val()});
	    	return false;
	    }
	});
}

var mensajeEndosoGuardar = function(idEndosoCancelacion) { // Función que nos permite mandar un mensaje al momento de guardar el endoso de cancelación.
	$("#varIdEndosoCancelacion").val(idEndosoCancelacion);
	controlBotones();
	alertify.success('Endoso de Cancelación Guardado con el Folio: ' + idEndosoCancelacion);
}

var controlBotones = function() { // Función que nos permite habilitar y deshabilitar botones al momento de guardar un endoso de cancelación.
	$("#btnImprimirEndoso").on("click",imprimirEndosoCancelacion);
	$("#btnImprimirEndoso").removeAttr("disabled");	
	$("#btnGuardarEndoso").unbind("click");
	$("#btnGuardarEndoso").attr("disabled","disabled");
}

var regresarListadoEndosoCancelacion = function() { // Función que nos permite regresar al listado de los endosos de cancelación.
	location.href = '/ListadoCancelacionEndoso/';
}

var imprimirEndosoCancelacion = function() { // Función que nos permite imprimir el endoso de cancelación pasando el id del endoso y el tipo de endoso.
	window.open('/ReporteEndosoCancelacion/' + $("#varIdEndosoCancelacion").val());
}
