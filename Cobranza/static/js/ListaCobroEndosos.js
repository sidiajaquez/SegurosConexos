$(document).on('ready',inicio); // Js que nos permite gestionar los datos para el cobro de endosos de transporte y declaracion.

function inicio () { // Función que inicia las variables y los eventos de los controles
	activarMenu();
	buscarEndosos();
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(27)').addClass('active');
}

var abrirPagoEndosos = function(idDeclaracion){ // Función que nos permite abrir una nueva platilla con la información necesaria para realizar el pago de endoso de (Declaración y Transporte).
	declaracionSeleccionada = idDeclaracion.closest("li");
	importe = declaracionSeleccionada.children()[3].innerText;
	idDeclaracion = declaracionSeleccionada.children()[0].innerText;
	tipoEndoso = declaracionSeleccionada.children()[2].innerText;
	location.href = '/PagoEndosoTransporteDeclaracion/' + idDeclaracion + '/' + tipoEndoso;
}

var buscarEndosos = function(){ //Función que obtiene los endoso a declaración o transporte.
	Dajaxice.Cobranza.obtener_declaraciones_endoso_traspaso(cargarEndosos);
}

var cargarEndosos = function(datosEndosos){ //Callback de la función buscarEndosos para mostrar en la lista la información de los endosos no cobradas
	var items = [];
	declaracionesEndoso = datosEndosos.declaraciones;
	
	for(rowArreglo=0;rowArreglo<declaracionesEndoso.length;rowArreglo++)
	{	
		linkGenerarPagoEndoso = "<a href='#' title='Generar pago de endoso' onclick='abrirPagoEndosos($(this));'><img src='/static/img/usd.png' /></a>";
		items.push({IdDeclaracion:declaracionesEndoso[rowArreglo][0], IdConstancia:declaracionesEndoso[rowArreglo][1], FolioConstancia:"Constancia: " + declaracionesEndoso[rowArreglo][2], 
			FolioSolicitud:"Solicitud: "+declaracionesEndoso[rowArreglo][3], NombreCompleto:"Nombre: "+declaracionesEndoso[rowArreglo][4],Rfc:"Rfc: "+declaracionesEndoso[rowArreglo][5],
			PeriodoInicio:"Periodo: " + declaracionesEndoso[rowArreglo][6], TipoEndoso:declaracionesEndoso[rowArreglo][7], Importe:"Importe: " + (declaracionesEndoso[rowArreglo][8]),ImporteAPagar:declaracionesEndoso[rowArreglo][8],
			pagoEndoso:linkGenerarPagoEndoso});
	}
	
	options = {
	        item: "<li><div style='display: none;'><span class='IdDeclaracion'></span></div><div style='display: none;'><span class='IdConstancia'></span></div><div style='display: none;'><span class='TipoEndoso'></span></div><div style='display: none;'><span class='ImporteAPagar'></span></div>" +
	        		"<div class='row'>" +
	        		"<span class='FolioConstancia tituloPrincipal span3'></span>" +
	        		"<span class='FolioSolicitud span3'></span><span class='NombreCompleto span4'></span>" +
	        		"<span class='pagoEndoso'></span>" +
	        		"</div>" +
	        		"<div class='row'><span class='Rfc Subtitulo span3'></span>" +
	        		"<span class='PeriodoInicio span3'></span><span class='Importe span4'></span>" +
	        		"</div>" +
	        		"</li>",
	        valueNames: [ 'IdDeclaracion', 'IdConstancia', 'FolioSolicitud', 'NombreCompleto', 'Rfc', 'PeriodoInicio', 'TipoEndoso', 'pagoEndoso', 'Importe', 'ImporteAPagar' ],
	        plugins: [
	            [ 'fuzzySearch' ]
	        ]
	};		
	
    var featureList = new List('lovely-things-list', options, items);

    $('.search-fuzzy').keyup(function() {
        featureList.fuzzySearch($(this).val());
    });		
}

Number.prototype.toCurrencyString = function(){
	return "$ " + Math.floor(this).toLocaleString() + (this % 1).toFixed(4).toLocaleString().replace(/^0/,''); 
}