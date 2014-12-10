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

var buscarConstancias = function(){ //Función que carga las constancias con solicitud de endoso de cancelación.
	Dajaxice.Endoso.obtener_constancias_endoso_cancelacion(cargarConstancias);
}

var imprimirEndosoDisminucion = function(idControlEndoso){ //Funcion que manda a imprimir el endoso de disminucion con la nueva descripcion de los bienes
	constanciaSeleccionada = idControlEndoso.closest("li");
	id_ControlEndoso = constanciaSeleccionada.children()[4].innerText;
	window.open('/EndosoADImpresion/'+id_ControlEndoso);
}

var generarEndosoCancelacion = function(rowConstancia) { // Función que nos permite llamar a la platilla endosocancelacion.html pasandole el id de la constancia.
	constanciaSeleccionada = rowConstancia.closest("li");
	id_constancia = constanciaSeleccionada.children()[0].innerText;
	location.href = '/EndosoCancelacion/' + id_constancia;
}

var cargarConstancias = function(datosConstancias) { // Callback de la funcion buscar_constancias para mostrar en la lista la informacion de las constancias con solicitud de endoso de disminucion

	if (datosConstancias.constancias != null && datosConstancias.constancias.length > 0)
	{		
		$(".list").html('');
		var items = [];
		var constancias = datosConstancias.constancias
		for(rowArreglo=0;rowArreglo<constancias.length;rowArreglo++)
		{
			linkGenerarEndosoCancelacion = "<a href='#' title='Crear Endoso de Cancelación' onclick='generarEndosoCancelacion($(this));'><i class='icon-file'></i></a>";
			
			var vigencia = (String(constancias[rowArreglo][5]) + " al " + String(constancias[rowArreglo][6]));
			
			items.push({IdConstancia:constancias[rowArreglo][0], NoConstancia:"Constancia: " + constancias[rowArreglo][0], NoSolicitud:"Solicitud: " + constancias[rowArreglo][1], Vigencia:"Vigencia: " + vigencia, 
				Moneda:"Moneda: " + constancias[rowArreglo][3], FolioSolicitud:"Folio Solicitud: " + constancias[rowArreglo][2],FechaSolicitud:"Fecha Solicitud: " + constancias[rowArreglo][4],
				Nombre:"Socio Asegurado: " + constancias[rowArreglo][7], Rfc:"RFC: " + constancias[rowArreglo][8], SumaAsegurada:"Suma Asegurada: $" + formatCurrency(constancias[rowArreglo][9]),
				generarEndoso:linkGenerarEndosoCancelacion
			});
		}
		
		options = {
		        item: "<li>" +
	    				"<div style='display: none;'><span class='IdConstancia'></span></div>" +
		        		"<div class='row'>" +
		        		"<div><span class='NoConstancia tituloPrincipal span2'></span></div>" +
		        		"</div>" +
		        		"<div class='row'>" +
		        		"<div><span class='NoSolicitud span3'></span><span class='FolioSolicitud span4'></span><span class='FechaSolicitud span3'></span><span class='generarEndoso'></span></div>" +
		        		"</div>" +
		        		"<div class='row'>" +
		        		"<div><span class='Moneda span3'></span><span class='SumaAsegurada span4'></span></span><span class='Vigencia span3'></span></div>" +
		        		"</div>" +
		        		"<div class='row'>" +
		        		"<div><span class='Rfc span3'></span><span class='Nombre span6'></span></div>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'IdConstancia', 'NoConstancia', 'NoSolicitud', 'Moneda', 'FechaSolicitud', 'Vigencia', 'Nombre', 
		                      'Rfc', 'SumaAsegurada','generarEndoso'],
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
		alertify.error('No se encontraron endosos de cancelación');
	}
}

Number.prototype.formatMoney = function(c, d, t){
	var n = this, 
	    c = isNaN(c = Math.abs(c)) ? 2 : c, 
	    d = d == undefined ? "." : d, 
	    t = t == undefined ? "," : t, 
	    s = n < 0 ? "-" : "", 
	    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
	    j = (j = i.length) > 3 ? j % 3 : 0;
	   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
	 };