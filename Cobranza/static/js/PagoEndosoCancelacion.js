$(document).on('ready',inicio);

function inicio(){ // Función que inicia las variables y los eventos de los controles
	activarMenu();
	$("#btnGuardarPagoEndoso").on("click", guardarPagoEndosoCancelacion);		
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

var guardarPagoEndosoCancelacion = function(){ // Función que nos permite mandar a guardar el pago del endoso de cancelación de las constancias anuales mediante la función guardar_prima_deposito.
	alertify.confirm("¿Desea generar el pago del endoso de cancelación?", function (e){
	    if (e){
	    	Dajaxice.Cobranza.guardar_pago_endoso_cancelacion(Dajax.process,{'idConstancia':$("#varIdConstancia").val(), 'montoAPagar':$("#varMontoAPagar").val()});	
	    	return false;
	    }
	});
}

var actualizarPagoEndoso = function(IdPago){ // Función que obtiene el id del pago para cargarlo en la variable cuando el pago es guardado en la base de datos.
	$("#varIdPagoEndosoCancelacion").val(IdPago);
	accionesBotonesAlGuardar();
	alertify.success('Pago del Endoso de Cancelación Guardado con el Folio: ' + IdPago);
}

var accionesBotonesAlGuardar = function(){ // Función que nos permite habilitar el boton de vista previa.
	$("#btnVistaPrevia").on("click", abrirReciboPagoEndoso);
	$("#btnVistaPrevia").removeAttr("disabled");
	$('#btnGuardarPagoEndoso').addClass('disabled');
	$("#btnGuardarPagoEndoso").unbind("click");
}

var abrirReciboPagoEndoso = function(){ // Función que nos permite abrir el recibo para el pago del endoso de cancelación de las constancias anuales.
	window.open('/ReportePagoEndosoCancelacion/' + $("#varIdPagoEndosoCancelacion").val());
}