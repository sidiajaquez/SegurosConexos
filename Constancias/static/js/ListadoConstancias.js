$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del listado de solicitudes.
	activarMenu();
	buscarSolicitudes();
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function buscarSolicitudes(){ // Funcion que busca las solicitudes con acta de verificacion y relacion anexa para mostrarlas en la lista de las constancias
	Dajaxice.Constancias.buscar_solicitudes(cargarSolicitudes);
}

function cargarSolicitudes(data){ // Obtiene la información de la busqueda de las solicitudes que recibe del método buscar_solicitudes de ajax.py
	if(data.solicitudes.length>0)
	{
		var items = [];
		$.each(data.solicitudes, function(i,solicitud)
		{
			linkImprimirConstancia = "";
			if (solicitud.ImprimirConstancia == 1){
				linkImprimirConstancia = "<a href='#' title='Imprimir Constancia' onclick='imprimirConstancia($(this));'><i class='icon-print'></i></a>";
			}
			
			items.push({PersonaSolicitud:solicitud.PersonaAsegurada, FolioSolicitud:"Folio Solicitud: "+solicitud.FolioSolicitud, FechaSolicitud:"Fecha Sol.: "+solicitud.FechaSolicitud, TipoSeguro:"Seguro: "+solicitud.TipoSeguro, SubTipoSeguro:"SubTipo: "+solicitud.SubTipoSeguro, Moneda:solicitud.Moneda, IdSolicitud:solicitud.IdSolicitud, accionesSolicitud:linkImprimirConstancia, IdConstancia:solicitud.IdConstancia});
		});
		
		options = {
		        item: "<li><div style='display: none;'><span class='IdSolicitud'></span></div><div style='display: none;'><span class='IdConstancia'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='PersonaSolicitud tituloPrincipal span5'></span>" +
		        		"<span class='TipoSeguro span3'></span><span class='SubTipoSeguro'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='FolioSolicitud Subtitulo span5'></span>" +
		        		"<span class='Moneda span3'></span><span class='FechaSolicitud'></span>" +
		        		"<span class='offset1'><a href='#' title='Generar Constancia' onclick='generarConstancia($(this));'><i class='icon-list-alt'></i></a></span>" +
		        		"<span class='accionesSolicitud'></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'PersonaSolicitud', 'FolioSolicitud', 'FechaSolicitud', 'TipoSeguro', 'SubTipoSeguro', 'Moneda', 'IdSolicitud', 'accionesSolicitud','IdConstancia' ],
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
		alertify.alert('No se encontraron solicitudes para la generación de su constancia');
	}	
}

var generarConstancia = function(idSolicitud){ //Funcion que toma el id de la solicitud para direccionar a la generacion de la Constancia
	solicitudSeleccionado = idSolicitud.closest("li");
	id_Solicitud = solicitudSeleccionado.children()[0].innerText;
	location.href = '/Constancia/' + id_Solicitud; 	
}

var imprimirConstancia = function(idSolicitud){ //Funcion que toma el id de la constancia para direccionar a la impresion de la constancia
	solicitudSeleccionado = idSolicitud.closest("li");
	id_Solicitud = solicitudSeleccionado.children()[1].innerText;
	location.href = '/ReporteConstancia/' + id_Solicitud; 		
}