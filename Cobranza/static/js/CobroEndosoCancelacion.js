$(document).on('ready',inicio); // Cobro de los endosos de cancelación de las constancias a declaración.

function inicio () { // Función que inicia las variables y los eventos de los controles
	activarMenu();
	$("#btnGuardarCobroEndoso").on("click", guardarCobroEndosoCancelacion);		
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq()').addClass('active');
}

var guardarCobroEndosoCancelacion = function(){ /* Función que nos permite mandar a guardar el cobro del endoso de cancelación de las constancias a declaración mediante la 
												   función guardar_cobro_endoso_cancelacion que se encuentra en la clase ajax.py pasandole el id de la constancia y el monto a guardar. */ 
	
	alertify.confirm("¿Desea generar el cobro del endoso de cancelación?", function (e)
	{
	    if (e)
	    {
	    	Dajaxice.Cobranza.guardar_cobro_endoso_cancelacion(Dajax.process,{'idConstancia':$("#varIdConstancia").val(), 'montoAPagar':$("#varMontoAPagar").val()});	
	    	return false;
	    }
	});
}

var actualizarCobroEndoso = function(idCobro){ // Función que obtiene el id del cobro para cargarlo en la variable varIdCobroEndosoCancelacion cuando el pago es guardado en la base de datos.

	$("#varIdCobroEndosoCancelacion").val(idCobro);
	accionesBotonesAlGuardar();
	alertify.success('Cobro del Endoso de Cancelación Guardado con el Folio: ' + idCobro);
}

var accionesBotonesAlGuardar = function() { // Función que nos permite habilitar el boton de vista previa y deshabilita el boton de guardar el cobro.
	$("#btnVistaPrevia").on("click", abrirReciboCobroEndoso);
	$("#btnVistaPrevia").removeAttr("disabled");
	$('#btnGuardarCobroEndoso').addClass('disabled');
	$("#btnGuardarCobroEndoso").unbind("click");
}

var abrirReciboCobroEndoso = function() // Función que nos permite abrir el recibo para el pago del endoso de cancelación de las constancias a declaración..
{	
	window.open('/ReporteCobroEndosoCancelacion/' + $("#varIdCobroEndosoCancelacion").val());
}