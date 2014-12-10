$(document).on('ready',inicio); // Js que nos permite gestionar el cobro de endosos de aumento.

function inicio(){ // Función que inicia las variables y los eventos de los controles
	activarMenu();
	buscarEndososAPagar();
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(27)').addClass('active');
}

var buscarEndososAPagar = function(){ // Función que carga en la lista los endosos que se pagarán.
	Dajaxice.Cobranza.obtener_control_endoso(cargarEndosos);
}

var guardarEnBaseDatos = function(importe, idDeclaracion, tipoEndoso){ // Función que guarda en la base de datos el registro de pago de recibo de los endosos.
	Dajaxice.Cobranza.guardar_pago_declaracion(Dajax.process,{'idDeclaracion':idDeclaracion, 'tipoEndoso':tipoEndoso,'importeAPagar':importe});	
	return false;
}

var abrirReportePagoEndoso = function(idDeclaracion, tipoEndoso){ // Función que permite abrir el reporte de pago de endoso.	
	window.open('/ReportePagoEndoso/' + idDeclaracion + '/' + tipoEndoso);
}

var cargarEndosos = function(datosEndosos){ //Callback de la función buscarEndososAPagar para mostrar en la lista la información de los endosos no cobradas
	var items = [];
		
	if(datosEndosos.endosos)
	{
		declaracionesEndoso = datosEndosos.endosos;
		
		$.each(declaracionesEndoso, function(i,endoso)
		{		
			linkGenerarPagoEndoso = "<a href='#' title='Pago de endoso' onclick='abrirPagoEndoso($(this));'><img src='/static/img/usd.png' /></a>";
			items.push({IdControlEndoso:endoso.IdControlEndoso, FolioEndoso:'Folio Endoso: ' + endoso.FolioEndoso, FolioSolicitudEndoso:'Solicitud: ' + endoso.FolioSolicitudEndoso,
						NombreCompleto:'Asegurado: ' + endoso.Nombre, Monto: 'Monto: ' + endoso.MontoAPagar, Rfc: 'Rfc: ' + endoso.Rfc, FechaEndoso: 'Fecha: ' + endoso.FechaEndoso,
						Constancia:'Constancia: ' + endoso.Constancia, pagoEndoso:linkGenerarPagoEndoso});			
		});		
	}
	
	options = {
	        item: 	"<li><div style='display: none;'><span class='IdControlEndoso'></span></div>" +
	        		"<div class='row'>" +
	        		"<span class='FolioEndoso tituloPrincipal span3'></span>" +
	        		"<span class='Rfc span3'></span><span class='NombreCompleto span4'></span>" +
	        		"<span class='pagoEndoso'></a></span>"+
	        		"</div>" +
	        		"<div class='row'><span class='Constancia Subtitulo span3'></span>" +
	        		"<span class='FolioSolicitudEndoso span3'></span><span class='FechaEndoso span3'></span>" +
	        		"<span class='Monto'></span>" +
	        		"</div>" +
	        		"</li>",
	        valueNames: [ 'IdControlEndoso', 'FolioEndoso', 'FolioSolicitudEndoso', 'NombreCompleto', 'Monto', 'Rfc', 'FechaEndoso', 'Constancia', 'pagoEndoso'],
	        plugins: [
	            [ 'fuzzySearch' ]
	        ]
	};
	
    var featureList = new List('lovely-things-list', options, items);

    $('.search-fuzzy').keyup(function() {
        featureList.fuzzySearch($(this).val());
    });		
}

var abrirPagoEndoso = function(controlEndoso){ // Función que nos permite abrir la plantilla pagoendoso.html
	controlSeleccionado = controlEndoso.closest("li");
	location.href = '/PagoEndoso/' + controlSeleccionado.children()[0].innerText;
}

Number.prototype.toCurrencyString = function(){ // Función que nos permite aplicarle formato current a las cantidades. 
	return "$ " + Math.floor(this).toLocaleString() + (this % 1).toFixed(4).toLocaleString().replace(/^0/,''); 
}