$(document).on('ready',inicio); // Js que nos permite gestionar el pago de la prima en deposito.

function inicio(){ // Función que inicia las variables y los eventos de los controles
	activarMenu();
	buscarConstanciasAPagar();
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(27)').addClass('active');
}

var buscarConstanciasAPagar = function(){ // Función que nos permite obtener la informacion de las constancias que se encuentran disponibles para pagar mediante la función obtener_constancias_pago_depsito.
	Dajaxice.Cobranza.obtener_constancias_pago_depsito(cargarConstanciasAPagar);
}

var abrirReportePagoEndoso = function(idDeclaracion, tipoEndoso){ // Función que permite abrir el reporte del pago del recibo del pago del recibo.
	window.open('/ReportePagoEndoso/' + idDeclaracion + '/' + tipoEndoso);
}

var cargarConstanciasAPagar = function(datosConstancias){ // Callback de la función buscarConstanciasAPagar para mostrar en la lista la información de las constancias que proceden para el pago de la prima en deposito.
	var items = [];
		
	if(datosConstancias.constancias)
	{
		constancias = datosConstancias.constancias;
		
		for(rowArreglo=0;rowArreglo<constancias.length;rowArreglo++)
		{	
			linkGenerarPagoPrima = "<a href='#' title='Generar pago de prima en deposito' onclick='abrirPagoPrima($(this));'><img src='/static/img/usd.png' /></a>";
			items.push({IdConstancia:constancias[rowArreglo][6], Constancia: "Constancia: " + constancias[rowArreglo][0], Solicitud: "Solicitud: " + constancias[rowArreglo][1], 
				Vigencia:"Vigencia: "+ (constancias[rowArreglo][3] + " al " + constancias[rowArreglo][4]), Moneda:"Moneda: "+constancias[rowArreglo][13],Nombre:"Nombre: "+constancias[rowArreglo][10],
				Rfc:"RFC: " + constancias[rowArreglo][11], Direccion: "Direccion: " + constancias[rowArreglo][12], Monto:"Monto: " + (constancias[rowArreglo][5]).toCurrencyString(),
				pagoPrima:linkGenerarPagoPrima});
		}	
	}
	
	options = {
	        item: 	"<li><div style='display: none;'><span class='IdConstancia'></span></div>" +
	        		"<div class='row'>" +
	        		"<span class='Constancia span3'></span>" +
	        		"<span class='Solicitud span3'></span>" +
	        		"<span class='Vigencia span4'></span>"+
	        		"<span class='pagoPrima'></span>" +
	        		"</div>" +	        		
	        		"<div class='row'><span class='Direccion span3'></span>" +
	        		"<span class='Moneda span3'></span>"+
	        		"<span class='Monto span3'></span>" +
	        		"</div>" +
	        		"<div class='row'><span class='Nombre span6'></span>" +
	        		"<span class='Rfc span3'></span>" +
	        		"</div>" +
	        		"</li>",
	        valueNames: [ 'IdConstancia', 'Constancia', 'Solicitud', 'Vigencia', 'Moneda', 'Nombre', 'Rfc', 'Direccion', 'Monto', 'pagoPrima'],
	        plugins: [
	            [ 'fuzzySearch' ]
	        ]
	};
	
    var featureList = new List('lovely-things-list', options, items);

    $('.search-fuzzy').keyup(function() {
        featureList.fuzzySearch($(this).val());
    });		
}

var abrirPagoPrima = function(pagoPrima){ // Función que nos permite abrir la plantilla pagoprimadeposito.html
	pagoSeleccionado = pagoPrima.closest("li");
	location.href = '/PagoPrimaDeposito/' + pagoSeleccionado.children()[0].innerText;
}

Number.prototype.toCurrencyString = function(){ // Función que nos permite aplicarle formato current a las cantidades.
	return "$ " + Math.floor(this).toLocaleString() + (this % 1).toFixed(4).toLocaleString().replace(/^0/,''); 
}