$(document).on('ready',inicio);

function inicio () { // Función que inicia las variables y los eventos de los controles
	activarMenu();
	$("#btnGuardarPagoPrimaDeposito").on("click", guardarPagoEndosoAumento);		
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

var guardarPagoEndosoAumento = function() // Función de la cobranza que nos permite guardar el pago de endoso de aumento en la base de datos.
{	
	alertify.confirm("¿Desea generar el pago de la prima en deposito?", function (e)
	{
	    if (e)
	    {
	    	Dajaxice.Cobranza.guardar_prima_deposito(Dajax.process,{'idConstancia':$("#varIdConstancia").val(), 'montoAPagar':$("#varMontoAPagar").val()});	
	    	return false;
	    }
	});
}

var actualizarPagoPrima = function(IdPago) // Función que obtiene el id del pago para cargarlo en la variable cuando el pago es guardado en la base de datos.
{
	$("#varIdPagoPrimaDeposito").val(IdPago);
	accionesBotonesAlGuardar();
	alertify.success('Pago de prima en deposito Guardado con el Folio: ' + IdPago);
}

var accionesBotonesAlGuardar = function() { // Función que nos permite habilitar el boton de vista previa.
	$("#btnVistaPrevia").on("click", abrirReciboPagoPrima);
	$("#btnVistaPrevia").removeAttr("disabled");
	$('#btnGuardarPagoPrimaDeposito').addClass('disabled');
	$("#btnGuardarPagoPrimaDeposito").unbind("click");
}

var abrirReciboPagoPrima = function() // Función que nos permite abrir el recibo para el pago de la prima en deposito.
{	
	window.open('/ReciboPagoPrimaDeposito/' + $("#varIdPagoPrimaDeposito").val());
}