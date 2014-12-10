$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario telefonos.
	activarMenu();
	buscarProgramas();
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function buscarProgramas(){ // Función que busca los programas de aseguramiento pasando el id del programa y las carga en la plantilla listadoprogramas.html
	Dajaxice.Programas.obtener_programas(cargarProgramas);
	return false;
}

function cargarProgramas(data){ // Obtiene la información de la busqueda de los programas que recibe del método buscarProgramas de ajax.py, los datos de la busqueda se agregan a la tabla listado_Programa_tabla.
	
	if(data.programas.length > 0)
	{	
		linkEliminarPrograma = ""
		
		var items = [];
		var options = {
		        item: "<li><div style='display: none;'><span class='IdPrograma'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='Folio tituloPrincipal span4'></span>" +
		        		"<span class='NumeroContrato span3'></span><span class='Ejercicio span4'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='TipoSeguro Subtitulo span4'></span><span class='SubTipoSeguro span3'></span><span class='Moneda span4'></span>" +
		        		"<span><a href='#' title='Editar Cotizador' onclick='editarPrograma($(this));'><i class='icon-pencil'></i></a></span><span class='accionesPrograma'></span></div>" +
		        		"<div class='row'><span class='Observaciones span11'></span>" + 	        		        		
		        		"</div>" +
		        		"<div style='display: none;'><span class='Utilizado'></span></div>" +
		        		"</li>",
		        valueNames: [ 'Folio', 'TipoSeguro', 'SubTipoSeguro','Ejercicio', 'Moneda', 'Observaciones', 'NumeroContrato', 'IdPrograma', 'Utilizado' ],
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		    };
		
		
		if(data.programas)
		{
			$.each(data.programas, function(i,programa)
			{		
				var moneda;
				
				if (programa.IdTipoMoneda == 1)
				{
					moneda = "PESO MEXICANO";
				}
				else
				{
					moneda = "DÓLAR ESTADOUNIDENSE";
				}
				
				if (programa.TieneCotizador == 0)
				{
					linkEliminarPrograma = "<a href='#' title='Eliminar Programa' onclick='eliminarPrograma($(this));'><i class='icon-remove'></i></a>";
				}
				else
				{
					linkEliminarPrograma = ""
				}
				
				items.push({Folio:'Folio:' + programa.FolioPrograma, TipoSeguro:"Tipo de Seguro: " + programa.TipoSeguro, SubTipoSeguro:"Sub Tipo Seguro: " + programa.SubTipoSeguro, Ejercicio:"Ejercicio: " + programa.Ejercicio, Moneda:"Moneda: " + moneda, Observaciones:"Observaciones: " + programa.Observaciones, NumeroContrato:"Numero de Contrato: " + programa.NumeroContrato, IdPrograma:programa.IdPrograma, Utilizado:programa.TieneCotizador, accionesPrograma:linkEliminarPrograma});			
			});																																																																																																																										
		}
	
	    var featureList = new List('list_programas', options, items);
	
	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });
	}
	else
	{
		alertify.alert('No se encontraron programas');
	}
}

function editarPrograma(programa){ // Función que permite editar el programa seleccionado de la table listado_programa_tabla pasando el id del programa a la plantilla programa.html
	var programaSeleccionado = programa.closest("li");
	var idPrograma = programaSeleccionado.children()[0].innerText;

	location.href = '/Programa/'+ idPrograma;
}

function eliminarPrograma(programa){ // Función que recibe un programa para eliminarlo de la tabla y de la base de datos.
	var programaSeleccionado = programa.closest("li");
	var id_Programa = programaSeleccionado.children()[0].innerText;
	var utilizado =  programaSeleccionado.children()[2].children[3].innerText;	

	alertify.confirm("Esto eliminará el programa, ¿Desea continuar?", function (e) {
		if (e)
		{
			programaSeleccionado.remove();
			Dajaxice.Programas.eliminar_programa(Dajax.process, {'idPrograma':id_Programa});
			alertify.success("Programa eliminado correctamente");
		}
	});
}