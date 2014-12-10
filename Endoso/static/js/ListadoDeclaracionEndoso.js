$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario listado de cotizaciones.  
	activarMenu();
	obtenerDeclaracionesTransporte();
	$("#btnEndosoNuevo").on("click", abrirEndosoNuevo);	
}

function abrirEndosoNuevo(){ // Función que nos permite abrir un endoso nuevo.
	location.href = '/DeclaracionEndoso/';
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

function obtenerDeclaracionesTransporte(){ // Función que permite obtener todas las declaraciones de transporte de la base de datos.
	Dajaxice.Endoso.obtener_declaraciones_endoso(cargarListadoDeclaracionEndoso);
	return false;	
}

function cargarListadoDeclaracionEndoso(data){ // Obtiene la información de la busqueda de las declaraciones que recibe del método obtener_declaraciones_transporte de ajax.py.
	
	if(data.declaracionendoso != null && data.declaracionendoso.length > 0)
	{	
		var items = [];
		declaracionendoso = data.declaracionendoso;
		
		for(rowArreglo=0;rowArreglo<declaracionendoso.length;rowArreglo++)
		{	
			linkEditarDeclaracion = "";
			linkNuevaDeclaracion = "";
			linkNuevoEndoso = "";
		
			fechaDeclaracion = declaracionendoso[rowArreglo][6].split('/');
			
			var meses = new Array ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");
						
			var mes = fechaDeclaracion[1];
			var ano = fechaDeclaracion[2];
			var fechaActual = new Date();			
			var mesActual = fechaActual.getMonth() + 1;
			var anoActual = fechaActual.getFullYear();
			
			if (declaracionendoso[rowArreglo][7] == 1)
			{					
				if (declaracionendoso[rowArreglo][8] == 0 && declaracionendoso[rowArreglo][9] > 0)
				{
					linkNuevaDeclaracion = "<a href='#' title='Nueva Declaración' onclick='crearNuevaDeclaracion($(this));'><i class='icon-th-list'></i></a>";
				}
				
				if (declaracionendoso[rowArreglo][9] == 0)
				{
					linkNuevoEndoso = "<a href='#' title='Nuevo Endoso' onclick='crearNuevoEndoso($(this));'><i class='icon-list-alt'></i></a>";
				}				
			}
			else
			{
				linkEditarDeclaracion = "<a href='#' title='Editar Declaración' onclick='editarEndoso($(this));'><i class='icon-pencil'></i></a>";
			}
			
			items.push({Rfc:"Rfc: " + declaracionendoso[rowArreglo][5], Nombre:"Nombre: " + declaracionendoso[rowArreglo][4], IdEndoso:declaracionendoso[rowArreglo][0], FolioConstancia:"Constancia: " + declaracionendoso[rowArreglo][2], NumeroSolicitud:"Solicitud: " + declaracionendoso[rowArreglo][3], Mes:meses[mes-1].toUpperCase() + ' DEL ' + anoActual, IdConstancia:declaracionendoso[rowArreglo][1], accionesEditar:linkEditarDeclaracion, accionesCrearNuevaDeclaracion:linkNuevaDeclaracion, accionesCrearNuevoEndoso:linkNuevoEndoso });
		}
		
		var options = {
		        item: "<li><div style='display: none;'><span class='IdEndoso'></span></div>" +
		        		"<div style='display: none;'><span class='IdConstancia'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='Rfc span2'></span><span class='Nombre span2'></span>" +
		        		"<span class='FolioConstancia span2'></span><span class='NumeroSolicitud span'></span>" +
		        		"<span class='Mes span2'></span>" +
		        		"<span class='accionesEditar'></span>" +
		        		"<span class='accionesCrearNuevaDeclaracion'></span>" +
		        		"<span class='accionesCrearNuevoEndoso'></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'Rfc', 'Nombre', 'IdEndoso', 'FolioConstancia', 'NumeroSolicitud', 'Mes', 'IdConstancia' ], 
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		};
		
		if(declaracionendoso.length==0){ // Si no existe ningun elemento para mostrarlo en la lista se pone el item oculto del html
			alertify.error('No se encontraron declaraciones de endoso');
			options = {
			        item: "<li><div style='display: none;'><span class='IdEndoso'></span></div>" +
			        		"<div style='display: none;'><span class='IdConstancia'></span></div>" +
			        		"<div class='row'>" +
			        		"<span class='Rfc span2'></span><span class='Nombre span2'></span>" +
			        		"<span class='FolioConstancia span2'></span><span class='NumeroSolicitud span'></span>" +
			        		"<span class='Mes span2'></span>" +
			        		"<span class='accionesEditar'></span>" +
			        		"<span class='accionesCrearNuevaDeclaracion'></span>" +
			        		"<span class='accionesCrearNuevoEndoso'></span>" +
			        		"</div>" +
			        		"</li>",
			        valueNames: [ 'Rfc', 'Nombre', 'IdEndoso', 'FolioConstancia', 'NumeroSolicitud', 'Mes', 'IdConstancia' ], 
			        plugins: [
			            [ 'fuzzySearch' ]
			        ]
			};
		}
	
	    var featureList = new List('list_endoso', options, items);
	    
	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });
	}
	else
	{
		alertify.error('No se encontraron declaraciones de endoso');
	}
}

function crearNuevoEndoso(id_declaracion){ // Función que obtiene el row de la tabla listado_declaracion para pasarlo por la url al cargar la plantilla declaraciones.html
	declaracionSeleccionada = id_declaracion.closest("li");
	location.href = '/EndosoDeclaracion/' + declaracionSeleccionada.children()[0].innerText;
}

function editarEndoso(id_Endoso){ // Función que obtiene el row de la tabla listado_declaracion para pasarlo por la url al cargar la plantilla declaraciones.html
	declaracionSeleccionada = id_Endoso.closest("li");
	location.href = '/DeclaracionEndoso/' + declaracionSeleccionada.children()[0].innerText;
}

function crearNuevaDeclaracion(id_constancia){ // Función que obtiene el row de la tabla listado_declaracion para pasarlo por la url al cargar la plantilla declaraciones.html
	declaracionSeleccionada = id_constancia.closest("li");
	location.href = '/DeclaracionEndosoConstancia/' + declaracionSeleccionada.children()[1].innerText;
}

function eliminarEndoso(idDeclaracionEndoso)  // Función que permite eliminar el cotizador seleccionado de la tabla listado_declaracion. 
{
	alertify.confirm("Esto eliminará la declaración, ¿Desea continuar?", function (e) {
	    if (e) {
			declaracionEndoso = idDeclaracionEndoso.closest("li");
			id_declaracion = declaracionEndoso.children()[0].innerText;
			declaracionEndoso.remove();
			Dajaxice.Endoso.eliminar_declaracion_endoso(Dajax.process, {'idDeclaracion':id_declaracion});
			alertify.success("Declaración eliminada correctamente");
	    }
	});
	
	return false;	
}