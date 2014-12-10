$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario de endoso.  
	activarMenu();
	
	$("#btnVistaPrevia").on("click", endosoDeclaracionImpresion);
	
	if ($("#varIdEndoso").val() == "")
	{
		$("#btnGuardarEndoso").on("click", guardarEndoso);
	}
	else
	{
		$("#btnGuardarEndoso").attr("disabled", true);
	}
	
	document.getElementById("txtEndoso").readOnly = true;
	document.getElementById("txtConstancia").readOnly = true;
	document.getElementById("txtMoneda").readOnly = true;
	document.getElementById("txtVigenciaInicio").readOnly = true;
	document.getElementById("txtVigenciaFin").readOnly = true;
	document.getElementById("txtSeguro").readOnly = true;
	document.getElementById("txtSubSeguro").readOnly = true;
	document.getElementById("txtSocio").readOnly = true;
	document.getElementById("txtDomicilio").readOnly = true;
}

function endosoDeclaracionImpresion() { // Función que permite imprimir la declaracion de endoso.
	window.open('/EndosoDeclaracionImpresion/' + $("#varIdDeclaracionEndoso").val());
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

function guardarEndoso(){ // Función que envia el formulario para guardarlo en la base de datos.
	
	if (pasarComprobacionesEndoso())
	{	
		Dajaxice.Endoso.guardar_endoso(Dajax.process,{'formulario':$('#formulario_endoso_declaracion').serialize(true), 'endoso':validarArrayVacio(obtencionDatosTablaEndoso())});
		$("#btnGuardarEndoso").attr("disabled", true);
	}
	
	return false;
}

function mensajeEndoso(folioEndoso){ //Función que recibe el número de folio del endoso de la función Dajaxice.Endoso.guardar_endoso para mostrarla en un alert.
	alertify.alert('Endoso Guardado con el Folio: ' + folioEndoso);
}

function mensajeEndoso(folioEndoso){ //Función que recibe el número de folio del endoso de la función Dajaxice.Endoso.guardar_endoso para mostrarla en un alert.
	alertify.alert('El Endoso Guardado con el Folio: ' + folioEndoso);
}

function pasarComprobacionesEndoso(){ // Función que verifica si la información ingresada en el formulario es la correcta.
	return true;
}

function obtencionDatosTablaEndoso(){ // Función que obtiene la información de la tabla tbl_endoso y la agrega a un arreglo.
	var arrayEndoso = [];
	
	$('.tbl_endoso tr').each(function(){
		var fila = $(this).find('td');
	    if (fila.length > 0)
	    {
			var arrayFilas = [];
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(0).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(1).html(),',','')); 			
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(2).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(3).html(),',','')); 
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(4).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(5).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(6).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(7).html(),',',''));
			
			arrayEndoso.push(arrayFilas);
	    }
	});
	
	return arrayEndoso;
}

var replaceAll = function(text, busca, reemplaza) // Función que nos permite remplazar los caracteres de un string.
{
	while (text.toString().indexOf(busca) != -1)	
	text = text.toString().replace(busca,reemplaza);
	
	return text;	
}