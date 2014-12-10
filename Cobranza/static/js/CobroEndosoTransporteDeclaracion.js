$(document).on('ready',inicio); // Cobro de los endoso a declaración.

function inicio(){ // Función que inicia las variables y los eventos de los controles
	//activarMenu();
	$("#btnPagoEndoso").on("click", guardarPagoEndoso);	
	$("#btnImprimir").attr("disabled","disabled");
}

var pasarComprobacionesGuardar = function(){ // Función que nos permite verificar si la información ingresada en la platilla es valida para guardar el cobro de endoso de transporte o declaración.
	var formaPago = document.getElementById("FormaPago");
	var checarFormaPago = formaPago.options[formaPago.selectedIndex].text;
	
	if(checarFormaPago == '---------')
	{
		alertify.alert('Se requiere seleccionar forma de pago para continuar para continuar.');
		return false;
	}
	
	return true;
}

var guardarPagoEndoso = function(){ // Función que nos permite generar el pago de los endosos de delcaración y transporte, guardando en la base de datos mediante la función guardar_pago_declaracion.

	if (pasarComprobacionesGuardar())
	{
		alertify.confirm("¿Desea pagar el cobro del endoso?", function (e)
		{
		    if (e)
		    {
				Dajaxice.Cobranza.guardar_pago_declaracion(Dajax.process,{'idDeclaracion':$("#varIdDeclaracion").val(), 'tipoEndoso':$("#varTipoDeclaracion").val(),'importeAPagar':$("#varTotalAPagar").val(), 'formaPago':$("#FormaPago option:selected").text()});
				return false;
		    }
		});	
	}
}

var actualizarPagoEndoso = function(idPago) { // Función que nos permite actualizar el id del pago del endoso y mandar un mensaje indicado que el pago se realizo de manera adecuada.
	$("#varIdPagoEndoso").val(idPago);
	accionesBotonesAlGuardar();
	alertify.success('Pago de endoso con el Folio: ' + idPago.toString());
}



var accionesBotonesAlGuardar = function() { // Función que permite gestionar las acciones de los botones pagar e imprimir al momento de guardar el pago.
	$("#btnImprimir").on("click", abrirReportePagoEndoso);
	$("#btnImprimir").removeAttr("disabled");
	$("#btnPagoEndoso").unbind("click");
	$("#btnPagoEndoso").attr("disabled","disabled");
}

var abrirReportePagoEndoso = function() { // Función que permite abrir el reporte de pago de endoso de declaración y transporte.	
	window.open('/ReportePagoEndoso/' + $("#varIdDeclaracion").val() + '/' + $("#varTipoDeclaracion").val());
}
		