$(document).on('ready',inicio);

function inicio(){ //Función que inicia las variables y los eventos de los controles del listado de solicitudes
	$("#FechaEmision").val(fechaActual());
	$("#btnCancelarConstancia").on("click",limpiarFormulario);
	$("#btnGuardarConstancia").on("click",guardarConstancia);
	if ($("#varIdConstancia").val() == ""){
		$("#btnVistaPrevia").attr("disabled",true);
	}
	activarMenu();
	limpiarFormulario();
	$("#btnVistaPrevia").on("click",vistaPreviaConstancia);
}

var vistaPreviaConstancia = function(){ //Funcion que manda llamar el reporte para la impresion de la constancia
	location.href = '/ReporteConstancia/'+ $("#varIdConstancia").val();
	return false;
}

function limpiarFormulario(){ //Funcion para limpiar los input del formulario
	$('#formulario_constancia').each (function(){
		  this.reset();
	});
	$("#FechaEmision").val(fechaActual());
	var formulario = $("#formulario_constancia")[0];
	var porcentajeBeneficiario = formulario.elements['porcentajeBeneficiario[]'];
	if (porcentajeBeneficiario){
		if (porcentajeBeneficiario.length >0 ){
			porcentajeBeneficiario[0].focus();
		}else{
			formulario.elements['porcentajeBeneficiario[]'].value=100;
			formulario.elements['porcentajeBeneficiario[]'].disabled=true;
		}
	}
	return false;
}

function guardarConstancia(){ //Funcion para guardar la constancia
	if (pasarComprobaciones()){
		coberturas = obtieneDatosTabla (".tblCoberturas");
		porcentajeBeneficiario = $("#formulario_constancia")[0].elements['porcentajeBeneficiario[]'];
		var beneficiarioPorcentaje = [];
		idPorcentajeBeneficiario = obtieneDatosTabla(".tblPersonaBeneficiarioConstancia");
		if (porcentajeBeneficiario.length >0 ){
			$.each(porcentajeBeneficiario, function(i,elemento){
				beneficiarioPorcentaje.push([idPorcentajeBeneficiario[i][0],elemento.value]); 
			});
		}else{
			beneficiarioPorcentaje.push([idPorcentajeBeneficiario[0][0],porcentajeBeneficiario.value]);
		}
		Dajaxice.Constancias.guardar_constancia(Dajax.process,{'frmConstancia':$('#formulario_constancia').serialize(true),'Coberturas':validarArrayVacio(coberturas),'beneficiarioPorcentaje':validarArrayVacio(beneficiarioPorcentaje)});
	}
	return false;
}

function mensajeConstancia(datosConstancia){ //Funcion que recibe el numero de la relacion anexa al acta de verificacion, de la funcion Dajaxice.Solicitud.guardar_relacion_anexa_acta_verificacion para mostrarla en un alert
	alertify.alert('Constancia Guardada con el Folio: '+ datosConstancia[0]);
	$("#varIdConstancia").val(datosConstancia[1]);
	$("#btnVistaPrevia").attr("disabled",false);
	$("#btnGuardarConstancia").attr("disabled",true);
	$("#btnCancelarConstancia").attr("disabled",true);
}

function pasarComprobaciones(){
	//se quitan las comas a los valores de la suma asegurada y la cuota neta
	$("#SumaAseguradaTotal").val($.trim(replaceAll($("#SumaAseguradaBienes").val(),",","")));
	$("#CuotaNeta").val($.trim(replaceAll($("#Cuota").val(),",","")));
	var porcentajeBeneficiario = $("#formulario_constancia")[0].elements['porcentajeBeneficiario[]'];
	var sumaPorcentaje = 0
	if (porcentajeBeneficiario.length >0 ){
		$.each(porcentajeBeneficiario, function(i,elemento){
			sumaPorcentaje += parseInt(elemento.value); 
		});
	}else{
		sumaPorcentaje = porcentajeBeneficiario.value;
	}
	if (sumaPorcentaje<100){
		alertify.alert('La cantidad de porcentaje de los beneficiarios es menor al 100%');
	}
	if (sumaPorcentaje>100){
		alertify.alert('La cantidad de porcentaje de los beneficiarios es mayor al 100%');
	}
	if (isNaN(sumaPorcentaje)){
		alertify.alert('Especifique cantidades validas en los porcentajes de los beneficiarios');
	}
	if (sumaPorcentaje == 100){
		return true;
	}
	return false;
}

function replaceAll( text, busca, reemplaza ){ //Reemplaza todos los caracteres que se encuentren en una cadena de texto
	while (text.toString().indexOf(busca) != -1)
		text = text.toString().replace(busca,reemplaza);
	return text;
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}