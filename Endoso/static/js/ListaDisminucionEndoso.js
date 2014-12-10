$(document).on('ready',inicio);
var datosBusqueda = {};

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario listado de endosos de disminucion  
	buscarConstancias();
	activarMenu();
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

var buscarConstancias = function(){ //Funcion que carga las constancias con solicitud de endoso de disminucion
	Dajaxice.Endoso.buscar_constancias_endoso(cargarConstancias, {'tipoEndoso':'DISMINUCIÓN'});
}

var cancelarEndosoDisminucion = function(idConstancia){ //Funcion para cancelar la solicitud o el endoso de disminucion
	alertify.set({ labels: {
	    ok     : "Si",
	    cancel : "No"
	}});	
	alertify.confirm("¿Cancelar Endoso?", function (e) {
	    if (e) {
	    	constanciaSeleccionada = idConstancia.closest("li");
	    	id_Constancia = constanciaSeleccionada.children()[1].innerText;
	    	tiene_Endoso = constanciaSeleccionada.children()[2].innerText;
	    	id_SolicitudEndoso = constanciaSeleccionada.children()[3].innerText;
	    	constanciaSeleccionada.remove();
	    	Dajaxice.Endoso.cancelar_endoso(Dajax.process, {'idConstancia':id_Constancia,'tieneEndoso':tiene_Endoso,'idSolicitudEndoso':id_SolicitudEndoso});
	    	eliminarDatoBusqueda(id_Constancia);
			alertify.success("Endoso eliminado correctamente");
	    }
	});	
	return false;	
}

var eliminarDatoBusqueda = function(idConstancia){ //Elimina de la lista la constancia
	if (datosBusqueda.constancias.length>0){
		$.each(datosBusqueda.constancias, function(i,constancia){
			if (constancia.IdConstancia == idConstancia){
				datosBusqueda.constancias.splice(i,1);
				return false;
			}
		});
		cargarConstancias(datosBusqueda);
	}
}

var generarEndosoDisminucion = function(idConstancia){ //Funcion para direccionar a la pagina de generacion de endoso de disminucion
	constanciaSeleccionada = idConstancia.closest("li");
	id_Constancia = constanciaSeleccionada.children()[1].innerText;
	location.href = '/EndosoDisminucion/' + id_Constancia;	
}

var imprimirEndosoDisminucion = function(idControlEndoso){ //Funcion que manda a imprimir el endoso de disminucion con la nueva descripcion de los bienes
	constanciaSeleccionada = idControlEndoso.closest("li");
	id_ControlEndoso = constanciaSeleccionada.children()[4].innerText;
	window.open('/EndosoADImpresion/'+id_ControlEndoso);
}

var cargarConstancias = function(datosConstancias) { //Callback de la funcion buscar_constancias para mostrar en la lista la informacion de las constancias con solicitud de endoso de disminucion
	$(".list").html('');
	datosBusqueda = datosConstancias;
	var items = [];
	
	$.each(datosConstancias.constancias, function(i,constancia)
	{
		linkImprimirAumentoEndoso = "<a href='#' title='Crear Endoso de Aumento' onclick='generarEndosoDisminucion($(this));'><i class='icon-file'></i></a>";
		if (constancia.TieneEndoso == true){
			linkImprimirAumentoEndoso = "<a href='#' title='Imprimir Endoso de Aumento' onclick='imprimirEndosoDisminucion($(this));'><i class='icon-print'></i></a>"; 
		}
		items.push({PersonaConstancia:constancia.PersonaAsegurada, FolioConstancia:"Folio Constancia: " + constancia.FolioConstancia, VigenciaConstancia:"Vigencia: "+constancia.VigenciaConstancia, 
			CuotaNeta:constancia.CuotaNeta, SumaAsegurada:"Suma Asegurada: $"+constancia.SumaAsegurada,Moneda:constancia.Moneda, IdSolicitud:constancia.IdSolicitud, IdConstancia:constancia.IdConstancia,
			AccionesEndoso:linkImprimirAumentoEndoso,TieneEndoso:constancia.TieneEndoso,IdSolicitudEndoso:constancia.SolicitudEndoso[0],IdControlEndoso:constancia.IdControlEndoso});
	});
	
	options = {
	        item: "<li><div style='display: none;'><span class='IdSolicitud'></span></div>" +
	        		"<div style='display: none;'><span class='IdConstancia'></span></div>" +
	        		"<div style='display: none;'><span class='TieneEndoso'></span></div>" +
	        		"<div style='display: none;'><span class='IdSolicitudEndoso'></span></div>" +
	        		"<div style='display: none;'><span class='IdControlEndoso'></span></div>" +
	        		"<div class='row'>" +
	        		"<span class='PersonaConstancia tituloPrincipal span5'></span>" +
	        		"<span class='CuotaNeta span3'></span><span class='SumaAsegurada span3'></span>" +
	        		"</div>" +
	        		"<div class='row'><span class='FolioConstancia Subtitulo span5'></span>" +
	        		"<span class='VigenciaConstancia span3'></span><span class='Moneda span1'></span>" +
	        		"<span class='offset1 AccionesEndoso'></span>" +
	        		"<span><a href='#' title='Cancelar Endoso de Aumento' onclick='cancelarEndosoDisminucion($(this));'><i class='icon-trash'></i></a></span>" +
	        		"</div>" +
	        		"</li>",
	        valueNames: [ 'PersonaConstancia', 'FolioConstancia', 'VigenciaConstancia', 'Moneda', 'IdConstancia', 'IdSolicitud', 'TieneEndoso', 
	                      'IdSolicitudEndoso', 'CuotaNeta', 'SumaAsegurada','AccionesEndoso','IdControlEndoso'],
	        plugins: [
	            [ 'fuzzySearch' ]
	        ]
	};

	if(datosConstancias.constancias.length==0){ //si no existe ningun elemento para mostrarlo en la lista se pone el item oculto del html
		alertify.error('No se encontraron solicitudes de endoso de disminución');
		options = {
		        item: "<li style='display: none;><div style='display: none;'><span class='IdSolicitud'></span></div>" +
		        		"<div style='display: none;'><span class='IdConstancia'></span></div>" +
		        		"<div style='display: none;'><span class='TieneEndoso'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='PersonaConstancia tituloPrincipal span5'></span>" +
		        		"<span class='CuotaNeta span3'></span><span class='SumaAsegurada span3'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='FolioConstancia Subtitulo span5'></span>" +
		        		"<span class='VigenciaConstancia span3'></span><span class='Moneda span1'></span>" +
		        		"<span class='offset1 AccionesEndoso'></span>" +
		        		"<span><a href='#' title='Cancelar Endoso de Aumento' onclick='cancelarEndosoDisminución($(this));'><i class='icon-trash'></i></a></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'PersonaConstancia', 'FolioConstancia', 'VigenciaConstancia', 'Moneda', 'IdConstancia', 'IdSolicitud', 'TieneEndoso','CuotaNeta', 'SumaAsegurada','AccionesEndoso'],
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