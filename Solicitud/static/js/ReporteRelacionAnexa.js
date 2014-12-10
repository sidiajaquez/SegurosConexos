$(document).on('ready',inicio);

var map;

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario teléfonos.
	activarMenu();
	$("#btnRegresar").click(regresarARelacionAnexa);
	$("#btnImprimir").click(imprimir);
	generarMapa();
}

function regresarARelacionAnexa() { // Función que llama a la plantilla Solicitud.html y le pasa el id del solicitud para cargar la información del mismo.
	location.href = '/RelacionAnexaSolicitudAseguramiento/' + $("#varIdSolicitud").val(); 
}

function activarMenu() { // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function imprimir() { // Función que llama a la vista previa de la impresion representando la tecla ctrl + P.
	window.print();
}

function generarMapa(){ //Se crea una marca de acuerdo a las coordenadas capturadas	
	descripcionContenidos = obtieneDatosTabla (".tblUbicacionBien");
    map = new GMaps({
        div: '#map',
        lat: descripcionContenidos[0][0],
        lng: descripcionContenidos[0][1]

      });
    map.addMarker({
        lat: descripcionContenidos[0][0],
        lng: descripcionContenidos[0][1],
    });
}