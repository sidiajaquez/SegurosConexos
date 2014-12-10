$(document).on('ready',inicio); // Listado que muestra las constancias que no han sido pagadas.

function inicio () { // Función que inicia las variables y los eventos de los controles.
	activarMenu();
	buscarConstancias();
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(27)').addClass('active');
}

var buscarConstancias = function(){ // Funcion que carga las constancias para su cobro mediante la clase ajax.py llamando a la función buscar_constancias.
	Dajaxice.Cobranza.buscar_constancias(cargarConstancias);
}

var generarPagoConstancia = function(idConstancia){ // Funcion que obtiene el IdConstancia para generar el recibo de pago
	constanciaSeleccionada = idConstancia.closest("li");
	id_Constancia = constanciaSeleccionada.children()[1].innerText;
	location.href = '/PagoConstancia/' + id_Constancia;
}

var cargarConstancias = function(datosConstancias) { // Callback de la funcion buscar_constancias para mostrar en la lista la informacion de las constancias no cobradas
	if(datosConstancias != null && datosConstancias.constancias.length > 0)
	{
		var items = [];
		$.each(datosConstancias.constancias, function(i,constancia)
		{
			linkImprimirReciboPago = "";
			linkGenerarPagoConstancia = "";
			if (constancia.Estatus == 1){
				linkImprimirReciboPago = "<a href='#' title='Imprimir Recibo de Pago' onclick='generarPagoConstancia($(this));'><i class='icon-print'></i></a>";
			}else{
				linkGenerarPagoConstancia = "<a href='#' title='Generar Recibo de Pago' onclick='generarPagoConstancia($(this));'><img src='/static/img/usd.png' /></a>";
			}
			items.push({PersonaConstancia:constancia.PersonaAsegurada, FolioConstancia:"Folio Constancia: " + constancia.FolioConstancia, VigenciaConstancia:"Vigencia: "+constancia.VigenciaConstancia, 
				CuotaNeta:constancia.CuotaNeta, SumaAsegurada:"Suma Asegurada: $"+constancia.SumaAsegurada,Moneda:constancia.Moneda, IdSolicitud:constancia.IdSolicitud, IdConstancia:constancia.IdConstancia,
				accionesConstancia:linkImprimirReciboPago,pagoConstancia:linkGenerarPagoConstancia});
		});
		
		options = {
		        item: "<li><div style='display: none;'><span class='IdSolicitud'></span></div><div style='display: none;'><span class='IdConstancia'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='PersonaConstancia tituloPrincipal span5'></span>" +
		        		"<span class='CuotaNeta span3'></span><span class='SumaAsegurada span3'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='FolioConstancia Subtitulo span5'></span>" +
		        		"<span class='VigenciaConstancia span3'></span><span class='Moneda span1'></span>" +
		        		"<span class='offset2 pagoConstancia'></span>" +
		        		"<span class='accionesConstancia'></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'PersonaConstancia', 'FolioConstancia', 'VigenciaConstancia', 'Moneda', 'IdConstancia', 'IdSolicitud', 'CuotaNeta', 'SumaAsegurada', 'accionesConstancia', 'pagoConstancia' ],
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		};		
		
	    var featureList = new List('lovely-things-list', options, items);

	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });		
	}
	else
	{
		alertify.error('No se encontraron solicitudes para la generación de su constancia');
	}	
}