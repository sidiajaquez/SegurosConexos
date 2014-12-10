$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario listado de cotizaciones.  
	activarMenu();
	obtenerCotizaciones();
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function obtenerCotizaciones(){ // Función que permite obtener todas las cotizaciones de la base de datos.
	Dajaxice.Cotizador.obtener_cotizaciones(cagarListadoCotizaciones);
	return false;	
}

function cagarListadoCotizaciones(data){ // Obtiene la información de la busqueda de las solicitudes que recibe del método buscar_solicitudes de ajax.py, los datos de la busqueda se agregan a la tabla listado_solicitudes_tabla.
	
	if(data.cotizaciones.length > 0)
	{	
		var items = [];
		var options = {
		        item: "<li><div style='display: none;'><span class='IdCotizador'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='FolioCotizador tituloPrincipal span5'></span>" +
		        		"<span class='PorcentajeFondo span3'></span><span class='PorcentajeReaseguro'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='FolioPrograma Subtitulo span5'></span>" +
		        		"<span class='Prima span3'></span>" +
		        		"<span class='offset2'><a href='#' title='Editar Cotizador' onclick='editarCotizador($(this));'><i class='icon-pencil'></i></a></span><span class='accionesCotizador'></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'FolioCotizador', 'PorcentajeFondo', 'PorcentajeReaseguro', 'FolioPrograma', 'Prima', 'IdCotizador' ],
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		    };	
		
		
		if(data.cotizaciones)
		{
			$.each(data.cotizaciones, function(i,cotizador)
			{		
				prima = "PORCENTAJE";
				
				if (cotizador.Prima == 1)
				{
					prima = "MILLAR";
				}
				
				items.push({FolioCotizador:"Folio Cotizador: " + cotizador.FolioCotizador, PorcentajeFondo:"Porcentaje Fondo: " + cotizador.PorcentajeFondo + "%", PorcentajeReaseguro:"Porcentaje Reaseguro: " + cotizador.PorcentajeReaseguro + "%", FolioPrograma:"Folio Programa: " + cotizador.FolioPrograma, Prima: "Prima: " + prima, IdCotizador:cotizador.IdCotizador});
				
			});																																																																																																																										
		}	
	
	    var featureList = new List('list_cotizadores', options, items);
	
	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });
	}
	else
	{
		alertify.alert('No se encontraron cotizadores');
	}
}

function editarCotizador(idCotizador){ // Función que obtiene el row de la tabla listado_cotizador_tabla para pasarlo por la url al cargar la plantilla cotizador.html
	cotizadorSeleccionado = idCotizador.closest("li");
	location.href = '/CotizadorEditar/'+ cotizadorSeleccionado.children()[0].innerText;
}

function eliminarCotizador(idCotizador)  // Función que permite eliminar el cotizador seleccionado de la tabla listado_cotizador_tabla. 
{
	alertify.confirm("Esto eliminará el cotizador, ¿Desea continuar?", function (e) {
	    if (e) {	    	
			cotizadorSeleccionado = idCotizador.closest("li");
			id_Cotizador = cotizadorSeleccionado.children()[0].innerText;
			cotizadorSeleccionado.remove();
			Dajaxice.Cotizador.eliminar_cotizador(Dajax.process, {'idCotizador':id_Cotizador});
			alertify.success("Cotizador eliminado correctamente");
	    }
	});	
	return false;	
}