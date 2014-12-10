$(document).on('ready',inicio);

function inicio(){ // Función que inicia las variables y los eventos de los controles
	activarMenu();
	buscarConstanciasCanceladas();
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(26)').addClass('active');
}

var buscarConstanciasCanceladas = function(){ //Funcion que busca las constancias que esten sobre los primeros 5 dias para pagar pasados sus 30 dias de gracia para su pago
	Dajaxice.Cobranza.buscar_constancias_canceladas(cargarConstanciasCanceladas);
}

var rehabilitarConstancia = function(idConstancia){
	constanciaSeleccionada = idConstancia.closest("li");
	id_Constancia = constanciaSeleccionada.children()[1].innerText;
	location.href = '/PagoConstancia/' + id_Constancia;
}

var cargarConstanciasCanceladas = function(datosConstanciasCanceladas){ //Callback de Cobranza.buscar_constancias_canceladas
	if(datosConstanciasCanceladas.ConstanciasCanceladas.length>0)
	{
		var items = [];
		$.each(datosConstanciasCanceladas.ConstanciasCanceladas, function(i,constancia)
		{
			linkImprimirReciboPago = "";
			linkRehabilitarConstancia = "";
			if (constancia.Estatus == 1){
				linkImprimirReciboPago = "<a href='#' title='Imprimir Recibo de Pago' onclick='generarPagoConstancia($(this));'><i class='icon-print'></i></a>";
			}else{
				linkRehabilitarConstancia = "<a href='#' title='Rehabilitar Constancia' onclick='rehabilitarConstancia($(this));'><i class='icon-refresh'></i></a>";
			}
			items.push({PersonaConstancia:constancia.PersonaAsegurada, FolioConstancia:"Folio Constancia: " + constancia.FolioConstancia, VigenciaConstancia:"Vigencia: "+constancia.VigenciaConstancia, 
				CuotaNeta:constancia.CuotaNeta, SumaAsegurada:"Suma Asegurada: $"+constancia.SumaAsegurada,Moneda:constancia.Moneda, IdSolicitud:constancia.IdSolicitud, IdConstancia:constancia.IdConstancia,
				accionesConstancia:linkImprimirReciboPago,pagoConstancia:linkRehabilitarConstancia});
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
		alertify.alert('No se encontraron constancias canceladas para su rehabilitación');
	}
}