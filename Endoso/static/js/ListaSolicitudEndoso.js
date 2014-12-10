$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario listado de cotizaciones.
	activarMenu();
	buscarConstancias();
}

var activarMenu = function() { // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

var buscarConstancias = function(){ //Funcion que carga las constancias para su cobro
	Dajaxice.Endoso.buscar_constancias_endoso(cargarConstancias,{'tipoEndoso':''});
}

var generarSolicitudEndoso = function(idConstancia){ //Funcion que manda a la generacion de una solicitud de endoso
	constanciaSeleccionada = idConstancia.closest("li");
	id_Constancia = constanciaSeleccionada.children()[1].innerText;
	location.href = '/SolicitudEndoso/' + id_Constancia;
}

var reimprimirSolicitudEndoso = function(idSolicitudEndoso){ //Reimpresion del formado de la ultima solicitud de endoso de la constancia
	window.open('/SolicitudEndosoImpresion/'+idSolicitudEndoso);
}

var cargarConstancias = function(datosConstancias) { //Callback de la funcion buscar_constancias para mostrar en la lista la informacion de las constancias no cobradas
	if(datosConstancias.constancias.length>0)
	{
		var items = [];
		$.each(datosConstancias.constancias, function(i,constancia)
		{
			linkReimpresionUltimaSolicitud = "";
			if (constancia.SolicitudEndoso[2]){ //Si tiene en true la opcion de reimprimir
				linkReimpresionUltimaSolicitud = "<a href='#' title='Reimpresion Solicitud de "+constancia.SolicitudEndoso[1]+"' onclick='reimprimirSolicitudEndoso("+constancia.SolicitudEndoso[0]+");'><i class='icon-print'></i></a>";
			}			
			items.push({PersonaConstancia:constancia.PersonaAsegurada, FolioConstancia:"Folio Constancia: " + constancia.FolioConstancia, VigenciaConstancia:"Vigencia: "+constancia.VigenciaConstancia, 
				CuotaNeta:constancia.CuotaNeta, SumaAsegurada:"Suma Asegurada: $"+constancia.SumaAsegurada,Moneda:constancia.Moneda, IdSolicitud:constancia.IdSolicitud, IdConstancia:constancia.IdConstancia,
				accionesSolicitud:linkReimpresionUltimaSolicitud});
		});
		
		options = {
		        item: "<li><div style='display: none;'><span class='IdSolicitud'></span></div><div style='display: none;'><span class='IdConstancia'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='PersonaConstancia tituloPrincipal span5'></span>" +
		        		"<span class='CuotaNeta span3'></span><span class='SumaAsegurada span3'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='FolioConstancia Subtitulo span5'></span>" +
		        		"<span class='VigenciaConstancia span3'></span><span class='Moneda span1'></span>" +
		        		"<span class='offset1'><a href='#' title='Solicitud de Endoso' onclick='generarSolicitudEndoso($(this));'><i class='icon-file'></i></a></span>" +
		        		"<span class='accionesSolicitud'></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'PersonaConstancia', 'FolioConstancia', 'VigenciaConstancia', 'Moneda', 'IdConstancia', 'IdSolicitud', 'CuotaNeta', 'SumaAsegurada','accionesSolicitud'],
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
		alertify.alert('No se encontraron solicitudes para la generación de la solicitud de endoso');
	}	
}