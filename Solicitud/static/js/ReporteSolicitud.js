$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario teléfonos.
	activarMenu();
	$("#btnRegresar").click(regresarASolicitud);
	$("#btnImprimir").click(imprimir);
	
	var idSolicitud = String( window.location.href ).split('?')[1];	
	
	if (idSolicitud != null)
	{
		$("#varIdSolicitud").val(idSolicitud);
		buscarSolicitud(idSolicitud);
	}
}

function regresarASolicitud() { // Función que llama a la plantilla Solicitud.html y le pasa el id del solicitud para cargar la información del mismo.
	location.href = '/Solicitud/?' + $("#varIdSolicitud").val();
}

function activarMenu() { // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function imprimir() { // Función que llama a la vista previa de la impresion representando la tecla ctrl + P.
	window.print();
}

function buscarSolicitud(idSolicitud){ // Función que permite buscar la solicitud de aseguramiento pasandole el id de la solicitud para cargar su información en el reporte.
	Dajaxice.Solicitud.buscar_solicitudConId(cargarSolicitudEnControles, {'idSolicitud': idSolicitud});
}

function cargarCoberturasPrograma(dato){ //Función que obtiene los beneficiarios de una solicitud.
	var contenido = $('.tbl_coberturas tbody');
	contenido.html('');
	var coberturas = '';
	if(dato.coberturasPorPrograma)
	{
		$.each(dato.coberturasPorPrograma, function(i,elemento)
		{
			$('<tr><td>'+elemento.Descripcion+'</td></tr>').appendTo(contenido);
		});
	}	
}

function cargarTablaBeneficiariosSolicitud(dato){ //Función que obtiene los beneficiarios de una solicitud.
	var contenido = $('.tbl_beneficiarios tbody');
	contenido.html('');
	
	if(dato.beneficiariosSolicitud)
	{
		$.each(dato.beneficiariosSolicitud, function(i,elemento)
		{			
			$('<tr><td>'+elemento.NombrePersonaBeneficiario+'</td><td style="text-align:center;">'+elemento.RfcPersonaBeneficiario+'</td><td style="text-align:center;">'+elemento.DomicilioPersonaBeneficiario+'</td></tr>').appendTo(contenido);
		});
	}
}

function cargarSolicitudEnControles(data){ // Función que obtiene una solicitud de la plantilla listasolicitud y la carga en los controles de la plantilla solicitud.html	
	solicitudACargar = data.solicitudEncontrada[0];
	
	if(solicitudACargar)
	{	
		$("#varIdTipoPrograma").val(solicitudACargar.IdTipoPrograma);
		
		var contenido = $('.tbl_solicitud tbody');
		contenido.html('');	
		
		var contenido_datos_solicitante = $('.tbl_datos_solicitante tbody'); 
		contenido_datos_solicitante.html('');

		var contenido_datos_asegurado = $('.tbl_datos_asegurado tbody'); 
		contenido_datos_asegurado.html('');		
		
		var contenido_datos_contratante = $('.tbl_datos_contratante tbody'); 
		contenido_datos_contratante.html('');
		
		var contenido_tipo_seguro_1 = $('.tbl_tipo_seguro_1 tbody'); 
		contenido_tipo_seguro_1.html('');
		
		var contenido_tipo_seguro_2 = $('.tbl_tipo_seguro_2 tbody'); 
		contenido_tipo_seguro_2.html('');
		
		var contenido_observaciones = $('.tbl_observacion tbody'); 
		contenido_observaciones.html('');
		
		var fecha = new Date();		
		
		$('<tr><td>'+[fecha.getDate(), fecha.getMonth(), fecha.getFullYear()].join('/')+'</td><td style="text-align:center;">'+solicitudACargar.FolioSolicitud+'</td><td style="text-align:center;">'+solicitudACargar.DeclaracionSolicitud+'</td></tr>').appendTo(contenido);
		$('<tr><td>'+solicitudACargar.NombreSolicitante+'</td><td style="text-align:center;">'+solicitudACargar.RfcSolicitante+'</td><td style="text-align:center;">'+solicitudACargar.DomicilioPersonaSolicitante+'</td><td style="text-align:center;">'+solicitudACargar.TelefonoSolicitante+'</td></tr>').appendTo(contenido_datos_solicitante);
		$('<tr><td>'+solicitudACargar.NombreAsegurado+'</td><td style="text-align:center;">'+solicitudACargar.RfcAsegurado+'</td><td style="text-align:center;">'+solicitudACargar.DomicilioPersonaAsegurado+'</td><td style="text-align:center;">'+solicitudACargar.TelefonoAsegurado+'</td></tr>').appendTo(contenido_datos_asegurado);
		$('<tr><td>'+solicitudACargar.NombreContratante+'</td><td style="text-align:center;">'+solicitudACargar.RfcContratante+'</td><td style="text-align:center;">'+solicitudACargar.DomicilioPersonaContratante+'</td><td style="text-align:center;">'+solicitudACargar.TelefonoContratante+'</td></tr>').appendTo(contenido_datos_contratante);
		$('<tr><td>'+solicitudACargar.TipoSeguro+'</td><td style="text-align:center;">'+solicitudACargar.SubTipoSeguro+'</td><td style="text-align:center;">'+solicitudACargar.Moneda+'</td><td style="text-align:center;">'+solicitudACargar.FolioPrograma+'</td><td style="text-align:center;">'+solicitudACargar.Ejercicio+'</td></tr>').appendTo(contenido_tipo_seguro_1);
		$('<tr><td>'+solicitudACargar.NumeroContrato+'</td><td style="text-align:right;">'+solicitudACargar.Unidades+'</td><td style="text-align:right;">'+solicitudACargar.ValorUnidad+'</td><td style="text-align:right;">'+solicitudACargar.SumaAseguradaSolicitada+'</td></tr>').appendTo(contenido_tipo_seguro_2);
		$('<tr><td>'+solicitudACargar.Observaciones+'</td></tr>').appendTo(contenido_observaciones);
		$("#firmaSocio").html(solicitudACargar.NombreAsegurado);
		Dajaxice.Solicitud.buscar_beneficiarios_solicitud(cargarTablaBeneficiariosSolicitud, {'idSolicitud': solicitudACargar.IdSolicitud});
		Dajaxice.ConexosAgropecuarios.obtener_consejoAdministracion_fondo(cargarConsejoAdministracion);
		Dajaxice.Programas.obtener_cobertura_con_idprograma(cargarCoberturasPrograma, {'idPrograma':$('#varIdTipoPrograma').val()});
		return false;
	}
	else
	{
		alertify.alert("Solicitud no encontrada");
	}
}

function cargarConsejoAdministracion(data){ // Función que carga los miembros del consejo de administración.
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