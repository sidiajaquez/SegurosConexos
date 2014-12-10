$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del listado de actas de verificacion
	activarMenu();
	buscarSolicitudes();
	$("#txtBuscarSolicitud").focus();
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

var buscarSolicitudes = function(){ //Función que busca las solicitudes de aseguramiento que tengan relacion anexa para poder elaborar su acta de verificacion
	Dajaxice.Solicitud.buscar_solicitudes_relacion_anexa(cargarSolicitudes,{"opcion":1});
}

var cargarSolicitudes = function(data){ // Obtiene la información de la busqueda de las solicitudes que recibe del método buscar_solicitudes de ajax.py
	if(data.solicitudes.length>0)
	{
		var items = [];
		$.each(data.solicitudes, function(i,solicitud)
		{	
			linkRelacionAnexaActaVerificacion = "";
			if (solicitud.Estatus == 1){
				linkRelacionAnexaActaVerificacion = "<a href='#' title='Relación Anexa Acta de Verificación' onclick='relacionAnexaActaVerificacion($(this));'><i class='icon-th-list'></i></a>";
			}
			items.push({PersonaSolicitud:solicitud.PersonaAsegurada, FolioSolicitud:"Folio Solicitud: "+solicitud.FolioSolicitud, FechaSolicitud:"Fecha: "+solicitud.FechaSolicitud, TipoSeguro:"Seguro: "+solicitud.TipoSeguro, SubTipoSeguro:"SubTipo: "+solicitud.SubTipoSeguro, Moneda:solicitud.Moneda, IdSolicitud:solicitud.IdSolicitud, accionesSolicitud:linkRelacionAnexaActaVerificacion });
		});
		
		
		options = {
		        item: "<li><div style='display: none;'><span class='IdSolicitud'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='PersonaSolicitud tituloPrincipal span5'></span>" +
		        		"<span class='TipoSeguro span3'></span><span class='SubTipoSeguro'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='FolioSolicitud Subtitulo span5'></span>" +
		        		"<span class='Moneda span3'></span><span class='FechaSolicitud'></span>" +
		        		"<span class='offset1'><a href='#' title='Acta de Verificación (Prellenada y de Campo)' onclick='actaVerificacion($(this));'><i class='icon-file'></i></a></span>" +
		        		"<span class='accionesSolicitud'></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'PersonaSolicitud', 'FolioSolicitud', 'FechaSolicitud', 'TipoSeguro', 'SubTipoSeguro', 'Moneda', 'IdSolicitud', 'accionesSolicitud' ],
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
		alertify.alert('No se encontraron solicitudes con relación anexa para este ejercicio');
	}	
}

function actaVerificacion(IdSolicitud){ // Función que permite crear el acta de verificacion para la solicitud
	solicitudSeleccionada = IdSolicitud.closest("li");
	location.href = '/ActaVerificacion/'+ solicitudSeleccionada.children()[0].innerText;
}

function relacionAnexaActaVerificacion(IdSolicitud){ //Funcion que linkea la solicitud aprobada a su acta de verificacion
	solicitudSeleccionada = IdSolicitud.closest("li");
	location.href = '/RelacionAnexaActaVerificacion/'+ solicitudSeleccionada.children()[0].innerText;
	
}