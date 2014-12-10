$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario teléfonos.
	activarMenu();
	$("#btnRegresar").on("click",regresarAConstancia);
	$("#btnImprimir").on("click",imprimirConstancia);	
}

function activarMenu() { // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

var imprimirConstancia = function(){ //manda el dialogo para imprimir
	window.print();
}

var regresarAConstancia = function(){ //regresa a la pagina anterior
	history.back();
}