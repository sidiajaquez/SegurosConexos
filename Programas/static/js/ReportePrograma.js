$(document).on('ready',inicio);

function inicio(){	// Función que inicializa las variables utilizadas para cargar la información del programa seleccionado para mostrar la vista previa.
	activarMenu();
	
	var idPrograma = String( window.location.href ).split('?')[1];	
	
	if (idPrograma != null)
	{
		$("#varIdPrograma").val(idPrograma);
		buscarPrograma(idPrograma);
	}
	
	$("#btnImprimir").click(imprimir);	
	$("#btnRegresar").click(regresarAProgramas);
}

function regresarAProgramas() { // Función que llama a la plantilla Programa.html y le pasa el id del programa para cargar la información del mismo.
	location.href = '/Programa/' + $("#varIdPrograma").val();
}

function activarMenu() { // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(5)').addClass('active');
}

function imprimir() { // Función que llama a la vista previa de la impresion representando la tecla ctrl + P.
	window.print();
}

function buscarPrograma(idPrograma){ // Función que busca la información del programa seleccionado.
	Dajaxice.Programas.buscar_programa(cargarInformacionPrograma, {'idPrograma': idPrograma});	
	Dajaxice.Programas.buscar_cobertura_programa_descripcion(cargarCoberturas, {'idPrograma':idPrograma});
	Dajaxice.Programas.buscar_area_influencia_descripcion(cargarAreaInfluencia, {'idPrograma':idPrograma});
	Dajaxice.ConexosAgropecuarios.obtener_consejoAdministracion_fondo(cargarConsejoAdministracion);
	return false;
}

function cargarConsejoAdministracion(data){ // Función que carga los miembros del consejo de adminsitración.
	var contenido = $('.tbl_footer_pagina tbody');
	contenido.html('');
		
	if(data.miembrosConsejo)
	{
		var nombrePresidente;
		var nombreSecretario;
		var nombreTesorero;
		
		$.each(data.miembrosConsejo, function(i,elemento)
		{				
			if (elemento.Cargo == "PRESIDENTE")
			{
				nombrePresidente = elemento.Nombre;
			}
			else if (elemento.Cargo == "SECRETARIO")
			{
				nombreSecretario = elemento.Nombre;
			}
			else if (elemento.Cargo == "TESORERO")
			{
				nombreTesorero = elemento.Nombre;
			}
		});
		
		$('<tr><td>'+nombrePresidente+'</td><td>'+nombreSecretario+'</td><td>'+nombreTesorero+'</td></tr>').appendTo(contenido);
	}
}

function cargarInformacionPrograma(data){ // Función que carga la encontrada del programa en el formulario de la plantilla programa.html
	var programaACargar = data.programaEncontrado[0];
	
	var contenido = $('.tbl_encabezado_reporte_programa_1 tbody');
	contenido.html('');
	var contenido_1 = $('.tbl_encabezado_reporte_programa_2 tbody');
	contenido_1.html('');
	var fecha = new Date();		
	
	var moneda;
	
	if (programaACargar.IdTipoMoneda == 1)
	{
		moneda = "PESO MEXICANO";
	}
	else
	{
		moneda = "DOLLAR ESTADUNIDENSE";
	}
	
	$('<tr><td>'+[fecha.getDate(), fecha.getMonth(), fecha.getFullYear()].join('/')+'</td><td>'+programaACargar.FolioPrograma+'</td><td>'+programaACargar.NumeroContrato+'</td><td>'+programaACargar.TipoSeguro+'</td><td>'+programaACargar.SubTipoSeguro+'</td></tr>').appendTo(contenido);
	$('<tr><td>'+moneda+'</td><td>'+programaACargar.Ejercicio+'</td><td>'+programaACargar.RazonSocial+'</td><td>'+programaACargar.Observaciones+'</td></tr>').appendTo(contenido_1);		
}

function cargarCoberturas(data){ // Función que carga las áreas de influencia del programa.
	var contenido = $('.tbl_cobertura tbody');
	contenido.html('');
	
	if(data.coberturasprograma)
	{
		$.each(data.coberturasprograma, function(i,elemento)
		{				
			$('<tr><td>'+elemento.Descripcion+'</td></tr>').appendTo(contenido);
		});
	}
}

function cargarAreaInfluencia(data){ // Función que carga las áreas de influencia del programa.
	var contenido = $('.tbl_area_influencia tbody');
	contenido.html('');
	
	if(data.areasInfluenciaDescripcion)
	{
		$.each(data.areasInfluenciaDescripcion, function(i,elemento)
		{				
			$('<tr><td>'+elemento.Descripcion+'</td></tr>').appendTo(contenido);
		});
	}
}