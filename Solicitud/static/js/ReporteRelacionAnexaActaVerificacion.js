$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario teléfonos.
	activarMenu();
	$("#btnRegresar").click(regresarActaVerificacion);
	$("#btnImprimir").click(imprimir);	
}

function regresarActaVerificacion() { // Funcion que se regresa al formulario de la relacion anexa al acta de verificacion
	history.back(); 
}

function activarMenu() { // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function imprimir() { // Función que llama a la vista previa de la impresion representando la tecla ctrl + P.
	window.print();
}