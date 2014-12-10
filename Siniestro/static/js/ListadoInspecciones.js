$(document).on('ready',inicio); // Archivo js que nos permite gestionar el listado de avisios de siniestro.

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario listado de avisos de siniestro.  
	activarMenu();
	obtenerInspecciones();
	$("#btnNuevaInspeccion").on("click", CrearNuevaInpeccion);	
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(40)').addClass('active');
}

var obtenerInspecciones = function(){ // Función que permite obtener las inspecciones de la clase ajax.py mediante la función obtener_listado_inspecciones.
	Dajaxice.Siniestro.obtener_listado_inspecciones(cargarListadoInspecciones);
	return false;	
}

var cargarListadoInspecciones = function(data){ // Función que carga en el listado la información recibida de la función obtenerAvisosSiniestro.
	
	if(data.inspecciones != null && data.inspecciones.length > 0)
	{	
		var items = [];
		inspecciones = data.inspecciones;
		
		for(rowArreglo=0;rowArreglo<inspecciones.length;rowArreglo++)
		{				
			linkEditarAviso = "<a href='#' title='Editar Inspeccion' onclick='editarInspeccion($(this));'><i class='icon-edit'></i></a>";
			linkImprimirActaSiniestro = "<a href='#' title='Acta Siniestro' onclick='imprimirActaSiniestro($(this));'><i class='icon-file'></i></a>";
			linkCompletarActaSiniestro = "<a href='#' title='Completar Acta Siniestro' onclick='completarActaSiniestro($(this));'><i class='icon-book'></i></a>";
			
			vigencia = inspecciones[rowArreglo][18] + " al " + inspecciones[rowArreglo][19]
			items.push({ IdInspeccion:inspecciones[rowArreglo][0], FolioInspeccion:"Inspección: " + inspecciones[rowArreglo][2], FolioAviso:"Aviso: " + inspecciones[rowArreglo][3], 
				TipoAviso:"Tipo de Aviso: " + inspecciones[rowArreglo][4], FechaSiniestro:"Siniestro: " + inspecciones[rowArreglo][7], Asegurado:"Asegurado: " + inspecciones[rowArreglo][17],
				Vigencia:"Vigencia: " + vigencia, Tecnico:"Técnico: " + inspecciones[rowArreglo][21], accionesEditar:linkEditarAviso, accionesImprimirActa:linkImprimirActaSiniestro,
				accionesCompletarActaSiniestro:linkCompletarActaSiniestro});
		}
		
		var options = {
		        item: "<li><div style='display: none;'><span class='IdInspeccion'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='FolioInspeccion tituloPrincipal span2'></span><span class='TipoAviso span3'></span>" +
		        		"<span class='FechaSiniestro span2'></span>" +
		        		"<span class='Vigencia span3'></span>" +
		        		"</div>" +
		        		"<div class='row'>" +
		        		"<span class='FolioAviso Subtitulo span2'></span>" +
		        		"<span class='Asegurado span8'></span>" +
		        		"</div>" +
		        		"<div class='row'>" +
		        		"<span class='Tecnico span10'></span>" +
		        		"<span class='accionesEditar'></span>" +
		        		"<span class='accionesImprimirActa'></span>" +
		        		"<span class='accionesCompletarActaSiniestro'></span>" +		        		
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'IdInspeccion', 'FolioInspeccion', 'FolioAviso', 'TipoAviso', 'FechaSiniestro', 'FechaSiniestro', 'Asegurado', 'vigencia', 'Tecnico' ], 
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		};
	
	    var featureList = new List('list_inspecciones', options, items);
	    
	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });
	}
	else
	{
		alertify.error('No se encontraron avisos de siniestros');
	}
}

function editarInspeccion(id_inspeccion){ // Función que recibe el row seleccionado de la lista para obtener el id de la inspección de siniestro para pasarlo a la plantilla inspeccion.html que nos permite modificar los datos.
	inspeccionSeleccionado = id_inspeccion.closest("li");
	location.href = '/InspeccionEditar/' + inspeccionSeleccionado.children()[0].innerText;
}

function CrearNuevaInpeccion(){ // Función que nos permite llamar a la platilla inpecciones.html para crear una nueva inspección en base a un aviso de siniestro.
	location.href = '/InspeccionNueva/';
}

function completarActaSiniestro(id_inspeccion){ // Función que recibe el row seleccionado de la lista para obtener el id de la inspección de siniestro para pasarlo a la plantilla inspeccion.html que nos permite modificar los datos.
	inspeccionSeleccionado = id_inspeccion.closest("li");
	location.href = '/ActaSiniestro/' + inspeccionSeleccionado.children()[0].innerText;
}

function imprimirActaSiniestro(id_inspeccion){ // Función que nos permite imprimir el acta de siniestro.
	inspeccionSeleccionado = id_inspeccion.closest("li");
	location.href = '/ReporteActaSiniestro/' + inspeccionSeleccionado.children()[0].innerText;
}