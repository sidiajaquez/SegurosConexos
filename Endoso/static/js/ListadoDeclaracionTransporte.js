$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario listado de cotizaciones.  
	activarMenu();
	obtenerEndoso();
	$("#btnTransporteNuevo").on("click", abrirTransporteNuevo);	
}

function abrirTransporteNuevo(){ // Función que nos permite abrir la declaración de transporte.
	location.href = '/DeclaracionTransporte/';
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

function obtenerEndoso(){ // Función que permite obtener todas las declaraciones de transporte de la base de datos.
	Dajaxice.Endoso.obtener_declaraciones_transporte(cagarListadoEndoso);
	return false;	
}

function cagarListadoEndoso(data){ // Obtiene la información de la busqueda de las solicitudes que recibe del método buscar_solicitudes de ajax.py, los datos de la busqueda se agregan a la tabla listado_solicitudes_tabla.
	
	if(data.declaraciontransporte != null && data.declaraciontransporte.length > 0)
	{	
		var items = [];
		declaraciontransporte = data.declaraciontransporte;
		for(rowArreglo=0;rowArreglo<declaraciontransporte.length;rowArreglo++)
		{	
			linkEditarDeclaracion = "";
			linkNuevaDeclaracion = "";
			linkNuevoEndoso = "";
			
			fechaDeclaracion = declaraciontransporte[rowArreglo][6].split('/');
			
			var mes = fechaDeclaracion[1];
			var ano = fechaDeclaracion[2];
			
			var fechaActual = new Date();
			
			var mesActual = fechaActual.getMonth() + 1;
			var anoActual = fechaActual.getFullYear();
			
			var meses = new Array ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");
			
			if (declaraciontransporte[rowArreglo][7] == 1)
			{					
				if (declaraciontransporte[rowArreglo][8] == 0 && declaraciontransporte[rowArreglo][9] > 0)
				{
					linkNuevaDeclaracion = "<a href='#' title='Nuevo Declaración' onclick='crearNuevaDeclaracion($(this));'><i class='icon-th-list'></i></a>";
				}
				
				if (declaraciontransporte[rowArreglo][9] == 0)
				{
					linkNuevoEndoso = "<a href='#' title='Nuevo Endoso' onclick='crearNuevoEndosoTransporte($(this));'><i class='icon-list-alt'></i></a>";		
				}				
			}
			else
			{
				linkEditarDeclaracion = "<a href='#' title='Editar Declaración' onclick='editarDeclaracionTransporte($(this));'><i class='icon-pencil'></i></a>";
			}
			
			items.push({Rfc:"Rfc: " + declaraciontransporte[rowArreglo][5], Nombre:"Nombre: " + declaraciontransporte[rowArreglo][4], IdEndoso:declaraciontransporte[rowArreglo][0], FolioConstancia:"Constancia: " + declaraciontransporte[rowArreglo][2], NumeroSolicitud:"Solicitud: " + declaraciontransporte[rowArreglo][3], Mes:meses[mes-1].toUpperCase() + ' DEL ' + anoActual, IdConstancia:declaraciontransporte[rowArreglo][1], accionesEditar:linkEditarDeclaracion, accionesCrearNuevaDeclaracion:linkNuevaDeclaracion, accionesCrearNuevoEndoso:linkNuevoEndoso });
		};
		
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
	
	    var featureList = new List('list_transporte', options, items);
	    
	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });
	}
	else
	{
		alertify.error('No se encontraron declaraciones de endoso');
	}
}

function crearNuevoEndosoTransporte(id_declaracion){ // Función que obtiene el row de la tabla listado_declaracion para pasarlo por la url al cargar la plantilla declaraciones.html
	declaracionSeleccionada = id_declaracion.closest("li");
	location.href = '/EndosoTransporte/' + declaracionSeleccionada.children()[0].innerText;
}

function editarDeclaracionTransporte(id_Transporte){ // Función que obtiene el row de la tabla listado_declaracion para pasarlo por la url al cargar la plantilla declaraciones.html
	declaracionSeleccionada = id_Transporte.closest("li");
	location.href = '/DeclaracionTransporte/' + declaracionSeleccionada.children()[0].innerText;
}

function crearNuevaDeclaracion(id_constancia){ // Función que obtiene el row de la tabla listado_declaracion para pasarlo por la url al cargar la plantilla declaraciones.html
	declaracionSeleccionada = id_constancia.closest("li");
	location.href = '/DeclaracionTransporteConstancia/' + declaracionSeleccionada.children()[1].innerText;
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