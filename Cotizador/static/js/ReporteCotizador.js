$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario teléfonos.
	activarMenu();
	
	var idCotizador = String( window.location.href ).split('?')[1];	
	
	if (idCotizador != null)
	{
		$("#varIdCotizador").val(idCotizador);
		buscarCotizador(idCotizador);
	}
	
	$("#btnImprimir").click(imprimir);	
	$("#btnRegresar").click(regresarACotizador);
}

function regresarACotizador() { // Función que llama a la plantilla Programa.html y le pasa el id del programa para cargar la información del mismo.
	location.href = '/Cotizador/?' + $("#varIdCotizador").val();
}

function activarMenu() { // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(5)').addClass('active');}

function imprimir() { // Función que llama a la vista previa de la impresion representando la tecla ctrl + P.
	window.print();
}

function buscarCotizador(idCotizador) { // Función que nos permite buscar el cotizador, recibiendo el parametro que contiene el id del cotizador.
	Dajaxice.Cotizador.buscar_cotizador(cargarInformacionCotizador, {'idCotizador': idCotizador});
	return false;
}

function cargarInformacionCotizador(data) { // Función que nos permite cargar la información del cotizador obtenida.
	cotizadorACargar = data.cotizadorEncontrado[0];
	
	var moneda = 'PESO MEXICANO';
		
	if (cotizadorACargar.IdTipoMoneda == 2)
	{
		moneda = 'DOLLAR ESTADUNIDENSE';
	}
	
	var prima = "PORCENTAJE";
	
	if (cotizadorACargar.Prima == 1)
	{
		prima = "MILLAR";
	}
		
	var porcentajeFondo = cotizadorACargar.PorcentajeFondo + "%"; 
	var porcentajeReaseguro = cotizadorACargar.PorcentajeReaseguro + "%";
	
	var contenido = $('.tbl_cotizador tbody');
	contenido.html('');
	var contenido_1 = $('.tbl_cotizador_programa tbody');
	contenido_1.html('');
	var fecha = new Date();		
	
	
	$('<tr><td>'+[fecha.getDate(), fecha.getMonth(), fecha.getFullYear()].join('/')+'</td><td>'+cotizadorACargar.FolioCotizador+'</td><td>'+porcentajeFondo+'</td><td>'+porcentajeReaseguro+'</td><td>'+prima+'</td></tr>').appendTo(contenido);
	$('<tr><td>'+cotizadorACargar.FolioPrograma+'</td><td>'+moneda+'</td><td>'+cotizadorACargar.TipoSeguro+'</td><td>'+cotizadorACargar.SubTipoSeguro+'</td></tr>').appendTo(contenido_1);
	
	Dajaxice.Cotizador.buscar_cotizador_cobertura(cargarCotizadorCoberturas, {'idCotizador': $("#varIdCotizador").val()});
	Dajaxice.ConexosAgropecuarios.obtener_consejoAdministracion_fondo(cargarConsejoAdministracion);
	return false;
}

function cargarCotizadorCoberturas(data){ // Función que permite cargar las cotizaciones y las coberturas en la tabla  cobertura_programa.
	rowsCotizadorCoberturas = 0;
	
	var totalTarifa = 0;
	var totalFondo = 0;
	var totalReaseguro = 0;
	
	var contenido = $('.tbl_coberturas tbody');
	contenido.html('');
	
	if(data.cotizadorEncontrado)
	{
		$.each(data.cotizadorEncontrado, function(i,cotizador)
		{
			rowsCotizadorCoberturas = rowsCotizadorCoberturas + 1;
			$('<tr><td>'+cotizador.Descripcion+'</td><td>'+ cotizador.Tarifa +'</td><td>'+cotizador.Fondo+'</td><td>'+cotizador.Reaseguro+'</td><td>'+cotizador.Remocion+'</td></tr>').appendTo(contenido);
			
			totalTarifa =  totalTarifa + parseFloat(cotizador.Tarifa);
			totalFondo = totalFondo + parseFloat(cotizador.Fondo);
			totalReaseguro = totalReaseguro + parseFloat(cotizador.Reaseguro);
		});
	}
	
	$('<tr><td>'+'Tarifa Total'+'</td><td>'+ totalTarifa.toFixed(2) +'</td><td>'+ totalFondo.toFixed(2) +'</td><td>'+ totalReaseguro.toFixed(2) +'</td></tr>').appendTo(contenido);
}

function cargarConsejoAdministracion(data){ // Función que carga las áreas de influencia del programa.
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