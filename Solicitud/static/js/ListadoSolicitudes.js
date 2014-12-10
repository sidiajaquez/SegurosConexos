$(document).on('ready',inicio);
var datosBusqueda = {};

function inicio(){	// Función que inicia las variables y los eventos de los controles del listado de solicitudes.
	activarMenu();
	buscarSolicitudes();
	$("#txtBuscarSolicitud").focus();
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function buscarSolicitudes(){ // Función que busca las solicitudes de aseguramiento pasando el id de la solicitud y las carga en la plantilla listasSolicitudes.html
	Dajaxice.Solicitud.buscar_solicitudes(cargarSolicitudes);
}

function editarSolicitud(IdSolicitud){ // Función que permite editar la solicitud seleccionada del listado pasando el id de la solicitud a la plantilla solicitud.html
	solicitudSeleccionado = IdSolicitud.closest("li");
	location.href = '/Solicitud/?'+ solicitudSeleccionado.children()[0].innerText;
}

function eliminarSolicitud(IdSolicitud){ // Función que elimina la solicitud seleccionada del listado pasando el id de la solicitud
	alertify.set({ labels: {
	    ok     : "Si",
	    cancel : "No"
	}});
	alertify.confirm("¿Eliminar solicitud?", function (e) {
	    if (e) {
	    	solicitudSeleccionado = IdSolicitud.closest("li");
	    	id_Solicitud = solicitudSeleccionado.children()[0].innerText;
	    	solicitudSeleccionado.remove();
	    	Dajaxice.Solicitud.eliminar_solicitud(Dajax.process, {'idSolicitud':id_Solicitud});
	    	eliminarDatoBusqueda(id_Solicitud);
			alertify.success("Solicitud eliminada correctamente");
	    }
	});	
	return false;
}

function eliminarDatoBusqueda(idSolicitud){ //Elimina de la lista la solicitud
	if (datosBusqueda.solicitudes.length>0){
		$.each(datosBusqueda.solicitudes, function(i,solicitud){
			if (solicitud.IdSolicitud == idSolicitud){
				datosBusqueda.solicitudes.splice(i,1);
				return false;
			}
		});
		cargarSolicitudes(datosBusqueda);
	}
}

function relacionAnexa(Solicitud){ //Funcion que direcciona la solicitud para agregarle su relacion anexa
	solicitudSeleccionado = Solicitud.closest("li");
	id_Solicitud = solicitudSeleccionado.children()[0].innerText;
	location.href = '/RelacionAnexaSolicitudAseguramiento/' + id_Solicitud; 
}

function cargarSolicitudes(data){ // Obtiene la información de la busqueda de las solicitudes que recibe del método buscar_solicitudes de ajax.py
	$(".list").html('');
	datosBusqueda = data;
	var items = [];
	$.each(data.solicitudes, function(i,solicitud)
	{	
		items.push({PersonaSolicitud:solicitud.PersonaAsegurada, FolioSolicitud:"Folio Solicitud: "+solicitud.FolioSolicitud, FechaSolicitud:"Fecha: "+solicitud.FechaSolicitud, TipoSeguro:"Seguro: "+solicitud.TipoSeguro, SubTipoSeguro:"SubTipo: "+solicitud.SubTipoSeguro, Moneda:solicitud.Moneda, IdSolicitud:solicitud.IdSolicitud});
	});
	
	options = {
	        item: "<li><div style='display: none;'><span class='IdSolicitud'></span></div>" +
	        		"<div class='row'>" +
	        		"<span class='PersonaSolicitud tituloPrincipal span5'></span>" +
	        		"<span class='TipoSeguro span3'></span><span class='SubTipoSeguro'></span>" +
	        		"</div>" +
	        		"<div class='row'><span class='FolioSolicitud Subtitulo span5'></span>" +
	        		"<span class='Moneda span3'></span><span class='FechaSolicitud'></span>" +
	        		"<span class='offset1'><a href='#' title='Editar Solicitud' onclick='editarSolicitud($(this));'><i class='icon-pencil'></i></a></span>" +
	        		"<span class='accionesSolicitud'><a href='#' title='Relación Anexa' onclick='relacionAnexa($(this));'><i class='icon-th-list'></i></a></span>" +
	        		"</div>" +
	        		"</li>",
	        valueNames: [ 'PersonaSolicitud', 'FolioSolicitud', 'FechaSolicitud', 'TipoSeguro', 'SubTipoSeguro', 'Moneda', 'IdSolicitud' ],
	        plugins: [
	            [ 'fuzzySearch' ]
	        ]
	};		
	
	if(data.solicitudes.length==0){ //si no existe ningun elemento para mostrarlo en la lista se pone el item oculta del html
		alertify.alert('No se encontraron solicitudes para este ejercicio');
		options = {
		        item: "<li style='display: none;><div style='display: none;'><span class='IdSolicitud'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='PersonaSolicitud tituloPrincipal span5'></span>" +
		        		"<span class='TipoSeguro span3'></span><span class='SubTipoSeguro'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='FolioSolicitud Subtitulo span5'></span>" +
		        		"<span class='Moneda span3'></span><span class='FechaSolicitud'></span>" +
		        		"<span class='offset1'><a href='#' title='Editar Solicitud' onclick='editarSolicitud($(this));'><i class='icon-pencil'></i></a></span>" +
		        		"<span class='accionesSolicitud'><a href='#' title='Relación Anexa' onclick='relacionAnexa($(this));'><i class='icon-th-list'></i></a></span>" +
		        		"<span class='accionesSolicitud'><a href='#' title='Eliminar Solicitud' onclick='eliminarSolicitud($(this));'><i class='icon-remove'></i></a></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'PersonaSolicitud', 'FolioSolicitud', 'FechaSolicitud', 'TipoSeguro', 'SubTipoSeguro', 'Moneda', 'IdSolicitud' ],
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		};
	}
	
	var featureList = new List('lovely-things-list', options, items);

    $('.search-fuzzy').keyup(function() {
        featureList.fuzzySearch($(this).val());
    });
}

function cargarPaginaSolicitud(solicitud){ // Función que carga la pagina solicitud pasandole el id de la solicitud que se cargara en los controles del formulario.
	solicitudSeleccionada = solicitud.closest("tr");
	location.href = '/Solicitud/?'+ solicitudSeleccionada.children('td')[0].innerText;
}