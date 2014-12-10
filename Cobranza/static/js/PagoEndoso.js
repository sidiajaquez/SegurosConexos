$(document).on('ready',inicio);

function inicio(){ // Función que inicia las variables y los eventos de los controles
	//activarMenu();
	$("#btnGuardarPago").on("click", guardarPagoEndosoAumento);		
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

var buscarEndososAPagar = function(){ // Función que carga en la lista los endosos que se pagarán.
	Dajaxice.Cobranza.obtener_control_endoso(cargarEndosos);
}

var guardarPagoEndosoAumento = function(){ // Función de la cobranza que nos permite guardar el pago de endoso de aumento en la base de datos.
	if (pasarComprobaciones())
	{
		Dajaxice.Cobranza.guardar_pago_endoso_aumento(Dajax.process,{'idConstancia':$("#varIdConstancia").val(), 'idSolicitud':$("#varIdSolicitudEndoso").val(),'montoAPagar':$("#Cuota").val(),'sumaAseguradaAumento':$("#SumaAseguradaBienesAumento").val(), 'formaPago':$("#FormaPago option:selected").text()});	
		return false;
	}
}

var pasarComprobaciones = function(){ // Función que valida la información ingresada en el formulario sea la correcta para poder guardar en la base de datos.
	var formaPago = document.getElementById("FormaPago");
	var checarFormaPago = formaPago.options[formaPago.selectedIndex].text;
		
	if (checarFormaPago == "---------")
	{
		alertify.alert('Se requiere seleccionar forma de pago para continuar para continuar.');
		return false;
	}
	
	return true;
}

var actualizarIdPago = function(IdPago){ // Función que al guardar el pago de endoso de aumento en la base de datos obtiene el id que se le asigno.
	$("#varIdPagoEndoso").val(IdPago);
	accionesBotonesAlGuardar();
	alertify.alert('Pago de endoso de Aumento Guardado con el Folio: ' + IdPago);
}

function accionesBotonesAlGuardar(){ // Función que nos permite habilitar el boton de vista previa.
	$("#btnVistaPrevia").on("click", abrirReciboPagoEndoso);
	$("#btnVistaPrevia").removeAttr("disabled");
	$('#btnGuardarPago').addClass('disabled');
	$("#btnGuardarPago").unbind("click");
}

var abrirReciboPagoEndoso = function(){ // Función que nos permite abrir la plantilla recibopagoendosoaumento.html para imprimir la informacion.
	window.open('/ReportePagoEndosoAumento/' + $("#varIdPagoEndoso").val());
}