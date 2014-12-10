$(document).on('ready',inicio); // Archivo js que nos permite gestionar el listado de avisios de siniestro.

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario listado de avisos de siniestro.  
	activarMenu();
	obtenerAvisosSiniestro();
	$("#btnAvisoNuevo").on("click", creaNuevoAviso);	
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(40)').addClass('active');
}

var obtenerAvisosSiniestro = function(){ // Función que permite obtener los avisos de siniestro de la clase ajax.py mediante la función obtener_avisos_siniestro.
	Dajaxice.Siniestro.obtener_avisos_siniestro(cargarListadoAvisosSiniestro);
	return false;
}

var cargarListadoAvisosSiniestro = function(data){ // Función que carga en el listado la información recibida de la función obtenerAvisosSiniestro.
	
	if(data.avisos != null && data.avisos.length > 0)
	{	
		var items = [];
		avisos = data.avisos;
		
		for(rowArreglo=0;rowArreglo<avisos.length;rowArreglo++)
		{				
			linkEditarAviso = "<a href='#' title='Editar Aviso' onclick='editarAviso($(this));'><i class='icon-edit'></i></a>";
			
			items.push({ IdAviso:avisos[rowArreglo][0], Aviso:"Aviso: " + avisos[rowArreglo][6], FechaAviso:"Fecha de Aviso: " + avisos[rowArreglo][1], FechaSiniestro:"Fecha de Siniestro: " + avisos[rowArreglo][2], 
				Constancia:"Constancia: " + avisos[rowArreglo][3], PersonaAsegurada:"Asegurado: " + avisos[rowArreglo][5],
				accionesEditar:linkEditarAviso});
		}
		
		var options = {
		        item: "<li><div style='display: none;'><span class='IdAviso'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='Aviso tituloPrincipal span3'></span><span class='FechaAviso span3'></span>" +
		        		"<span class='FechaSiniestro span4'></span>" +
		        		"</div>" +
		        		"<div class='row'>" +
		        		"<span class='Constancia Subtitulo span3'></span>" +
		        		"<span class='PersonaAsegurada span7'></span>" +
		        		"<span class='accionesEditar'></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'IdAviso', 'Aviso', 'FechaAviso', 'FechaSiniestro', 'Constancia', 'PersonaAsegurada' ], 
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		};
	
	    var featureList = new List('list_aviso', options, items);
	    
	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });
	}
	else
	{
		alertify.error('No se encontraron avisos de siniestros');
	}
}

function editarAviso(id_aviso){ // Función que recibe el row seleccionado de la lista para obtener el id del aviso de siniestro para pasarlo a la plantilla avisosiniestro.html que nos permite modificar los datos.
	avisoSeleccionado = id_aviso.closest("li");
	location.href = '/AvisoSiniestroEditar/' + avisoSeleccionado.children()[0].innerText;
}

function creaNuevoAviso(){ // Función que nos permite crear un aviso de siniestro nuevo llamando a la plantilla avisosiniestro.html
	location.href = '/AvisoSiniestroNuevo/';
}

function eliminarEndoso(idDeclaracionEndoso){  // Función que permite eliminar el cotizador seleccionado de la tabla listado_declaracion. 
	alertify.confirm("Esto eliminará la declaración, ¿Desea continuar?", function (e)
	{
	    if (e) 
	    {
			declaracionEndoso = idDeclaracionEndoso.closest("li");
			id_declaracion = declaracionEndoso.children()[0].innerText;
			declaracionEndoso.remove();
			Dajaxice.Endoso.eliminar_declaracion_endoso(Dajax.process, {'idDeclaracion':id_declaracion});
			alertify.success("Declaración eliminada correctamente");
	    }
	});
	
	return false;
}