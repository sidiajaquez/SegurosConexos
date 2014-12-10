$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario historico declaracion de transporte.​
	activarMenu();
	$("#btnBuscarConstancia").on("click", buscarConstancia);
	$("#btnBuscarConstanciaModal").on("click", limpiarBuscadorConstancia);
	tabla_buscar_constancia();
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

function pasarComprobacionesBuscarConstancia() // Función que permite pasar las comprobaciones para buscar la constancia.
{
	if ($("#txtBuscarConstancia").val() == "")
	{
		alertify.alert("Se requiere ingresar el número de constancia para continuar.");
		return false;
	}			
	
	return true;
}

function buscarConstancia(){ // Función que busca la lista de constancias en base en base al id de la constancia.
	if (pasarComprobacionesBuscarConstancia())
	{
		Dajaxice.Endoso.obtener_constancia_idconstancia_transporte(cargarModalConstancias,{'idConstancia':$("#txtBuscarConstancia").val()});	
		return false;
	}
};

function cargarModalConstancias(data){ // Obtiene la información de la busqueda de la persona que recibe del método buscar_persona de ajax.py, los datos de la busqueda se agregan a la tabla busquedaPersona de la ventana modal.
	var contenido = $('.tbl_buscar_constancia tbody');
	contenido.html('');	

	var moneda = "";
	
	if(data.constancias)
	{
		constancias = data.constancias;
		
		for(var i=0; i<constancias.length; i++)
		{
			if (constancias[i][3] == 1)
			{
				moneda = "PESO MEXICANO";
			}
			else if (constancias[i][3] == 2)
			{
				moneda = "DÓLAR"
			}
			
			$('<tr><td style="display: none;">'+constancias[i][0]+'</td><td>'+constancias[i][1]+"</td><td>"+constancias[i][2]+"</td><td>"+moneda+'</td><td>'+constancias[i][4]+'</td><td>'+constancias[i][5]+'</td><td>'+constancias[i][6]+'</td></tr>').appendTo(contenido);
		}	
		
	}
	else
	{
		alertify.alert("No se encontro constancia.");
	}
}

function limpiarBuscadorConstancia(){ // Función que cierra el formulario modal buscadorConstancia.
	$("#txtBuscarConstancia").val('');
	var contenido = $('.tbl_buscar_constancia tbody');
	contenido.html('');	
}

function tabla_buscar_constancia(){ // Función que permite interactuar con la ventana modal de buscar constancias.
	$(".modal").on('shown', function() {
	    $("#txtBuscarConstancia").focus();
	});	
	
	$('.tbl_buscar_constancia tbody').on('mouseover', 'tr', function(event) { //toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tbl_buscar_constancia tbody').on('mouseout', 'tr', function(event) { //evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	

	$('.tbl_buscar_constancia tbody').on('click', 'tr', function(event) { //evento click que selecciona el row y marca el check de la tabla		
		$("#varIdConstancia").val($(this).children('td')[0].innerText);	
		$(".close").click();
		buscarDeclaracionesTransporteConstancia();
	});
}

function buscarDeclaracionesTransporteConstancia() // Función que busca la lista de constancias en base en base al id de la constancia.
{
	Dajaxice.Endoso.obtener_declaraciones_transporte_idconstancia(cargarDeclaracionesTransporte,{'idConstancia':$("#varIdConstancia").val()});	
	return false;
}

function cargarDeclaracionesTransporte(data) // Función que nos permite cargar el listado de declaraciones de transporte.
{	
	if(data.declaraciontransporte.length > 0)
	{	
		var items = [];
		declaraciontransporte = data.declaraciontransporte;
		for(rowArreglo=0;rowArreglo<declaraciontransporte.length;rowArreglo++)
		{	
			linkVerDeclaracion = "";
			linkVerEndoso = "";
					
			fechaDeclaracion = declaraciontransporte[rowArreglo][6].split('/');
			
			var meses = new Array ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");
						
			var mes = fechaDeclaracion[1];
			var ano = fechaDeclaracion[2];
			var fechaActual = new Date();
			var mesActual = fechaActual.getMonth() + 1;
			var anoActual = fechaActual.getFullYear();
			
			linkVerDeclaracion = "<a href='#' title='Imprimir Declaracion' onclick='imprimirDeclaracionTransporte($(this));'><i class='icon-th-list'></i></a>";
			linkVerEndoso = "<a href='#' title='Imprimir Endoso' onclick='imprimirEndoso($(this));'><i class='icon-list-alt'></i></a>";
			
			items.push({Rfc:"Rfc: " + declaraciontransporte[rowArreglo][5], Nombre:"Nombre: " + declaraciontransporte[rowArreglo][4], IdEndoso:declaraciontransporte[rowArreglo][0], FolioConstancia:"Constancia: " + declaraciontransporte[rowArreglo][2], NumeroSolicitud:"Solicitud: " + declaraciontransporte[rowArreglo][3], Mes:meses[mes-1].toUpperCase() + ' DEL ' + anoActual, IdConstancia:declaraciontransporte[rowArreglo][1], accionesVerDeclaracion:linkVerDeclaracion, accionesVerEndoso:linkVerEndoso});
		}
		
		var options = {
		        item: "<li><div style='display: none;'><span class='IdEndoso'></span></div>" +
		        		"<div style='display: none;'><span class='IdConstancia'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='Rfc span2'></span><span class='Nombre span2'></span>" +
		        		"<span class='FolioConstancia span2'></span><span class='NumeroSolicitud span'></span>" +
		        		"<span class='Mes span2'></span>" +
		        		"<span class='accionesVerDeclaracion'></span>" +
		        		"<span class='accionesVerEndoso'></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'Rfc', 'Nombre', 'IdEndoso', 'FolioConstancia', 'NumeroSolicitud', 'Mes', 'IdConstancia' ], 
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		};
	
	    var featureList = new List('list_declaraciones', options, items);
	    
	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });
	}
	else
	{
		alertify.success('No se encontraron declaraciones de transportes');
	}
}

function imprimirDeclaracionTransporte(id_declaracion) // Función que nos permite imprimir la declaración de transporte.
{
	declaracionSeleccionada = id_declaracion.closest("li");
	window.open('/DeclaracionTransporteImpresion/' + declaracionSeleccionada.children()[0].innerText);
}

function imprimirEndoso(id_declaracion) // Función que nos permite imprimir la información del endoso de transporte.
{
	declaracionSeleccionada = id_declaracion.closest("li");
	window.open('/EndosoTransporteImpresion/' + declaracionSeleccionada.children()[0].innerText);
}