$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles de la solicitud.
	activarMenu();
	
	$("#FechaSolicitud").val(fechaActual());
	$("#Ejercicio").val((new Date).getFullYear());
	//$("#ValorUnidad").mask("000,000,000,000,000.00", {reverse:true});
	//$("#Unidades").mask("000,000,000,000,000", {reverse:true});
	$("#txtSumaAseguradaSolicitada").mask("000,000,000,000,000.00");
	
	$("#ValorUnidad,#Unidades").on({
		change:calcularSumaAseguradaSolicitada,
		keydown:calcularSumaAseguradaSolicitada,
		keyup:calcularSumaAseguradaSolicitada
	});
	
	$("#btnBuscarPersonaSolicitud").on('click',buscarPersonaSolicitud);
	$("#btnBuscarProgramaSolicitud").on('click',limpiarModalBusquedaProgramas);
	$("#btnGuardarSolicitud").on('click',guardar_solicitud);
	$("#btnBuscarPersonaSolicitante").on('click',fcnBuscarPersonaSolicitante);
	$("#btnBuscarPersonaAsegurada").on('click',fcnBuscarPersonaAsegurada);
	$("#btnBuscarPersonaContratante").on('click',fcnBuscarPersonaContratante);
	$("#btnBuscarPersonaBeneficiario").on('click',fcnBuscarPersonaBeneficiario);
	$("#btnBuscarProgramaSolicitudModal").on("click",buscarProgramasSolicitud);
	$("#btnCancelarSolicitud").on("click",limpiarFormularioSolicitudes);
		
	tablaBusquedaPersonaSolicitud();
	modalBusquedaProgramas();
	
	var idSolicitud = String( window.location.href ).split('?')[1];	
	
	if (idSolicitud != null)
	{
		$("#btnVistaPrevia").click(vistaPrevia);
		$("#varIdSolicitud").val(idSolicitud);
		$(".nuevaSolicitud").css("display","none");
		$("#btnListadoSolicitudes").css("display","none");
		buscarSolicitud(idSolicitud);
	}
	else
	{
		$('#btnVistaPrevia').attr('disabled', 'true');
	}
}

function vistaPrevia(){ // Función que permite mostrar la solicitud seleccionada en la plantilla lista de solicitudes.html
	location.href = '/ReporteSolicitud/?' + $("#varIdSolicitud").val();
}

function limpiarFormularioSolicitudes(){ //Función que resetea el formulario
	if ($("#varIdSolicitud").val()==''){
		$('#formulario_solicitudes').each (function(){
			  this.reset();
		});
		$("#FechaSolicitud").val(fechaActual());
		$("#DeclaracionSolicitud").focus();
		$('.tblPersonaBeneficiarioSolicitud tbody').html('');
		$("#varIdPersonaSolicitante").val('');
		$("#varIdPersonaContratante").val('');
		$("#varIdTipoPrograma").val('');
		$("#varEsSocio").val();
		$("#varIdSolicitud").val();
		$('.coberturasSolicitud').html('');
	}else{
		location.href='/Solicitudes/';
	}
	return false;
}

function fcnBuscarPersonaSolicitante(){ //Funcion para controlar que boton se esta presionando y llenar los datos del solicitante
	limpiarModalBusquedaPersonaSolicitud(1,0);
}

function fcnBuscarPersonaContratante(){ //Funcion para controlar que boton se esta presionando y llenar los datos del contratante
	limpiarModalBusquedaPersonaSolicitud(2,0);
}

function fcnBuscarPersonaBeneficiario(){ //Funcion para controlar que boton se esta presionando y llenar la tabla de beneficiarios
	limpiarModalBusquedaPersonaSolicitud(3,0);
}

function fcnBuscarPersonaAsegurada(){ //Funcion para controlar que boton se esta presionando y llenar los datos del asegurado
	limpiarModalBusquedaPersonaSolicitud(4,1);
}

function limpiarModalBusquedaPersonaSolicitud(solicitanteOContratanteOBeneficiario,esSocio){ // funcion que borra la caja de busqueda y la tabla de la ventana modal tblBusquedaPersonaSolicitud
	$("#txtSolicitanteOContratanteOBeneficiario").val(solicitanteOContratanteOBeneficiario);
	$("#varEsSocio").val(esSocio);
	$("#txtBuscarPersonaSolicitud").val('');
	var contenido = $('.tblBusquedaPersonaSolicitud tbody');
	contenido.html('');		
}

function limpiarModalBusquedaProgramas(){ //Funcion que borra la caja de busqueda de la ventana modal busqueda programas
	$("#txtBuscarProgramaSolicitud").val('');
	var contenido = $('.tblBusquedaProgramaSolicitud tbody');
	contenido.html('');	
}

function calcularSumaAseguradaSolicitada(){ //Funcion que multiplica las unidades por su valor para obtener la suma asegurada solicitada
	unidades = $("#Unidades").val();
	valorUnidad = $(this).val();
	sumaAseguradaSolicitada = unidades * valorUnidad;
	$("#txtSumaAseguradaSolicitada").val(sumaAseguradaSolicitada);
}


function guardar_solicitud(){	// Función que guarda la información de la solicitud de aseguramiento pasando comprobaciones. 
	if (pasarComprobaciones())
	{
		beneficiariosSolicitud = obtieneDatosTabla('.tblPersonaBeneficiarioSolicitud');
		if ($("#varIdSolicitud").val()==''){
			Dajaxice.Solicitud.guardar_solicitud(Dajax.process,{'frmSolicitudAseguramiento':$('#formulario_solicitudes').serialize(true),'beneficiariosSolicitud':validarArrayVacio(beneficiariosSolicitud)});
			limpiarFormularioSolicitudes();
		}else{ // Si existe valor es porque es una modificación
			alertify.confirm("¿Desea modificar la solicitud?", function (e) {
			    if (e) {
			    	Dajaxice.Solicitud.guardar_solicitud(Dajax.process,{'frmSolicitudAseguramiento':$('#formulario_solicitudes').serialize(true),'beneficiariosSolicitud':validarArrayVacio(beneficiariosSolicitud)});
					alertify.success("Solicitud Modificada");
					$("#DeclaracionSolicitud").focus();
			    }
			});			
		}
	}
	else
	{
		alertify.alert('Se requiere ingresar información');
	}
	return false;
}

function mensajeSolicitud(folioSolicitud){ //Funcion que recibe el numero de folio de solicitud de la funcion Dajaxice.Solicitud.guardar_solicitud para mostrarla en un alert
	alertify.alert('Solicitud Guardada con el Folio: '+ folioSolicitud);
}

function pasarComprobaciones(){
	listaBeneficiarios = obtieneDatosTabla(".tblPersonaBeneficiarioSolicitud");
	if ($("#DeclaracionSolicitud").val() == '' || $("#varIdPersonaSolicitante").val() == '' || $("#varIdPersonaContratante").val() == '' || $("#varIdPersonaAsegurada").val() == '' || $("#varIdTipoPrograma").val() == '' || $("#Unidades").val() == '' || $("#ValorUnidad").val() == '' || (listaBeneficiarios.length == 0)){
		return false;
	}else{
		if (isNaN($("#Unidades").val()) || isNaN($("#ValorUnidad").val())){
			alertify.alert("las Unidades y/o Valor por Unidad necesitan ser numéricos");
			return false;
		}
		return true;
	}
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function buscarPersonaSolicitud(){ // Función que busca a una persona para agregarlos a la solicitud de aseguramiento.
	esSocio = $("#varEsSocio").val();
	Dajaxice.BuscadorPersonas.buscar_todas_personas(cargarTablaBuscarPersonaSolicitud, {'datosBuscar':$("#txtBuscarPersonaSolicitud").val().toUpperCase(),'esSocio':esSocio});
	return false;
}

function buscarProgramasSolicitud(){ //Funcion que busca los programas para el ejercicio actual
	var tipoSolicitud = null;
	if ($("#DeclaracionSolicitud").val()=="ANUAL"){
		tipoSolicitud = 1;
	}
	if ($("#DeclaracionSolicitud").val()=="A DECLARACIÓN"){
		tipoSolicitud = 2;
	}
	if(tipoSolicitud){
		Dajaxice.Programas.buscar_programas_ejercicio_actual(cargarProgramaSeleccionado, {'buscarPrograma':$("#txtBuscarProgramaSolicitud").val().toUpperCase(),'tipoSolicitud':tipoSolicitud});
	}else{
		alertify.alert("No se ha elegido el tipo de solicitud");
	}
	return false;
}

function cargarProgramaSeleccionado(programa){ //Callback de la funcion buscarProgramasSolicitud que trae informacion del programa seleccionado
	var contenido = $('.tblBusquedaProgramaSolicitud tbody');
	contenido.html('');
	
	if (programa.programas){
		$.each(programa.programas, function (i, elemento){
			$('<tr><td style="display: none;">'+elemento.IdPrograma+'</td><td>'+elemento.TipoSeguro+'</td><td>'+elemento.SubTipoSeguro+'</td><td>'+elemento.DescripcionMoneda+'</td><td>'+elemento.NumeroContrato+'</td><td>'+elemento.FolioPrograma+'</td><td style="display: none;">'+elemento.Ejercicio+'</td></tr>').appendTo(contenido);
		});
		
	}else{
		alertify.alert('No se encontro infromación');
	}
		
}

function cargarTablaBuscarPersonaSolicitud(dato){ // Función que carga la información en el formulario de la solicitud de la personas encontradas.
	var contenido = $('.tblBusquedaPersonaSolicitud tbody');
	contenido.html('');
	
	if(dato.personas)
	{
		$.each(dato.personas, function(i,elemento)
		{	
			nombreCompleto = arreglarNombreMoralFisica(elemento);
			
			$('<tr><td>'+elemento.IdPersona+'</td><td>'+nombreCompleto+'</td><td>'+elemento.Rfc+'</td><td style="display: none;">'+elemento.Direccion+'</td><td style="display: none;">' + elemento.Telefono + '</td><td style="display: none;">'+elemento.CP+'</td><td style="display: none;">'+elemento.Municipio+'</td><td style="display: none;">'+elemento.Estado+'</td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function arreglarNombreMoralFisica(nombreCompletoMoralFisica){ // Funcion que concatena en una variable el nombre dependiendo si es fisica o moral
	var nombreCompleto='';
	// Se hacen validaciones de null para que no se adjunte la palabra null en la variable nombreCompleto
	if (nombreCompletoMoralFisica.PrimerNombre != null){
		nombreCompleto = nombreCompletoMoralFisica.PrimerNombre;
	}
	if (nombreCompletoMoralFisica.SegundoNombre != null){
		nombreCompleto = nombreCompleto + ' ' + nombreCompletoMoralFisica.SegundoNombre;
	}
	if (nombreCompletoMoralFisica.RazonSocial != null){
		nombreCompleto = nombreCompleto + ' ' + nombreCompletoMoralFisica.RazonSocial;
	}
	if (nombreCompletoMoralFisica.ApellidoPaterno != null){
		nombreCompleto = nombreCompleto + ' ' + nombreCompletoMoralFisica.ApellidoPaterno;
	}
	if (nombreCompletoMoralFisica.ApellidoMaterno != null){
		nombreCompleto = nombreCompleto + ' ' + nombreCompletoMoralFisica.ApellidoMaterno;
	}
	return nombreCompleto;
}

function modalBusquedaProgramas(){ //Función que permite interactuar con la ventana modal de busqueda de programas
	$("#mdlBuscarProgramaSolicitud").on('shown', function() {
	    $("#txtBuscarProgramaSolicitud").focus();
	});

	$('.tblBusquedaProgramaSolicitud tbody').on('mouseover', 'tr', function(event) { //Toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tblBusquedaProgramaSolicitud tbody').on('mouseout', 'tr', function(event) { // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});
	
	
	$('.tblBusquedaProgramaSolicitud tbody').on('click', 'tr', function(event) { // permite agregar los datos del programa en los input text correspondientes.		
		$('#txtTipoSeguroSolicitud').val($(this).children('td')[1].innerText);
		$('#txtSubTipoSeguroSolicitud').val($(this).children('td')[2].innerText);
		$('#txtMonedaSolicitud').val($(this).children('td')[3].innerText);
		$('#txtEjercicioSolicitud').val($(this).children('td')[6].innerText);
		$('#txtContratoReaseguro').val($(this).children('td')[4].innerText);
		$('#txtFolioPrograma').val($(this).children('td')[5].innerText);
		$('#varIdTipoPrograma').val($(this).children('td')[0].innerText);
		//Se cargan las coberturas para el programa seleccionado
		Dajaxice.Programas.obtener_cobertura_con_idprograma(cargarCoberturasPrograma, {'idPrograma':$('#varIdTipoPrograma').val()});
		$(".close").click();
	});		
}

function cargarCoberturasPrograma(dato){ //Callback de la funcion obtener_cobertura_con_idprograma para obtener las coberturas e imprimirlas
	var contenido = $('.coberturasSolicitud');
	contenido.html('');
	
	if(dato.coberturasPorPrograma)
	{
		$.each(dato.coberturasPorPrograma, function(i,elemento)
		{				
			$('<span class="label label-info span3" style="margin-bottom:2px;"><i class="icon-ok icon-white"></i> '+elemento.Descripcion+'</span>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información de coberturas');
	}	
}

function tablaBusquedaPersonaSolicitud(){ // Función que permite interactuar con la ventana modal de busqueda de personas.
	$(".modal").on('shown', function() {
	    $("#txtBuscarPersonaSolicitud").focus();
	});
	
	$('.tblBusquedaPersonaSolicitud tbody').on('mouseover', 'tr', function(event) { //Toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tblBusquedaPersonaSolicitud tbody').on('mouseout', 'tr', function(event) { // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});

	var idPersona;
	
	$('.tblBusquedaPersonaSolicitud tbody').on('click', 'tr', function(event) { // permite agregar a la tabla de personas principal el registro que se seleccione.		
		idPersona = $(this).children('td')[0].innerText;
		if($("#txtSolicitanteOContratanteOBeneficiario").val() == 1){
			$('#txtSolicitanteSolicitud').val($(this).children('td')[1].innerText);
			$('#txtSolicitanteRfc').val($(this).children('td')[2].innerText);
			$('#txtSolicitanteDomicilio').val($(this).children('td')[3].innerText);
			$('#txtSolicitanteTelefono').val($(this).children('td')[4].innerText);
			$('#txtSolicitanteCP').val($(this).children('td')[5].innerText);
			$('#txtSolicitanteMunicipio').val($(this).children('td')[6].innerText);
			$('#txtSolicitanteEstado').val($(this).children('td')[7].innerText);
			$('#varIdPersonaSolicitante').val(idPersona);
		}
		if($("#txtSolicitanteOContratanteOBeneficiario").val() == 2){
			$('#txtContratanteSolicitud').val($(this).children('td')[1].innerText);
			$('#txtContratanteRfc').val($(this).children('td')[2].innerText);
			$('#txtContratanteDomicilio').val($(this).children('td')[3].innerText);
			$('#txtContratanteTelefono').val($(this).children('td')[4].innerText);
			$('#txtContratanteCP').val($(this).children('td')[5].innerText);
			$('#txtContratanteMunicipio').val($(this).children('td')[6].innerText);
			$('#txtContratanteEstado').val($(this).children('td')[7].innerText);
			$('#varIdPersonaContratante').val(idPersona);
		}
		if($("#txtSolicitanteOContratanteOBeneficiario").val() == 3){
			var contenido = $('.tblPersonaBeneficiarioSolicitud tbody');
			registroDuplicado = comprobarBeneficiarioDuplicado($(this).children('td')[0].innerText);
			if (registroDuplicado.idPersonaBeneficiarioRepetida){
				alertify.alert('La persona ya se encuentra como Beneficiaria');
			}else{
				$('<tr><td style="display: none;">'+$(this).children('td')[0].innerText+'</td><td style="display: none;"></td><td>'+$(this).children('td')[1].innerText+'</td><td>'+$(this).children('td')[3].innerText+'</td><td>'+$(this).children('td')[2].innerText+'</td><td><a onclick="eliminarBeneficiariosDeTabla($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
			}
		}
		if($("#txtSolicitanteOContratanteOBeneficiario").val() == 4){
			$('#txtAseguradoSolicitud').val($(this).children('td')[1].innerText);
			$('#txtAseguradoRfc').val($(this).children('td')[2].innerText);
			$('#txtAseguradoDomicilio').val($(this).children('td')[3].innerText);
			$('#txtAseguradoTelefono').val($(this).children('td')[4].innerText);
			$('#txtAseguradoCP').val($(this).children('td')[5].innerText);
			$('#txtAseguradoMunicipio').val($(this).children('td')[6].innerText);
			$('#txtAseguradoEstado').val($(this).children('td')[7].innerText);
			$('#varIdPersonaAsegurada').val(idPersona);
		}		
		$(".close").click();
	});	
}

function eliminarBeneficiariosDeTabla(eliminarRegistro){ // Función que elimina las filas de la tabla de Beneficiarios de la solicitud
	alertify.confirm("Esto eliminará el Beneficiario, ¿Desea continuar?", function (e) {
	    if (e) {
	    	eliminarRegistro.parent().parent().remove();
			var rowEliminar = eliminarRegistro.closest("tr");
			if (rowEliminar.children('td')[1].innerText != ''){
				Dajaxice.Solicitud.eliminar_beneficiario(Dajax.process, {'idBeneficiarioSolicitud':rowEliminar.children('td')[1].innerText});
			}
			alertify.success("El Beneficiario fue eliminado correctamente");
	    }
	});	
	return false;	
}


function comprobarBeneficiarioDuplicado(idPersonaBeneficiario){ //Funcion que comprueba antes de agregar un beneficiario que no se encuentre repetido
	var registroRepetido = new Object();
	registroRepetido.idPersonaBeneficiarioRepetida = false;
	$('.tblPersonaBeneficiarioSolicitud tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 0:
					if ($(this).text() == idPersonaBeneficiario){
						registroRepetido.idPersonaBeneficiarioRepetida = true;
					}
					break;
			}
		});
	});
	return registroRepetido;	
}

function buscarSolicitud(idSolicitud){ // Función que busca la información de una solicitud de aseguramiento pasandole el id solicitud.	
	Dajaxice.Solicitud.buscar_solicitudConId(cargarSolicitudEnControles, {'idSolicitud': idSolicitud});
	Dajaxice.Solicitud.buscar_beneficiarios_solicitud(cargarTablaBeneficiariosSolicitud, {'idSolicitud': idSolicitud});
	return false;
}

function cargarSolicitudEnControles(data){ // Función que obtiene una solicitud de la plantilla listasolicitud y la carga en los controles de la plantilla solicitud.html	
	solicitudACargar = data.solicitudEncontrada[0];
	if(solicitudACargar){
		$("#varIdSolicitud").val(solicitudACargar.IdSolicitud);	
		$("#FechaSolicitud").val(solicitudACargar.FechaSolicitud);
		$("#txtSolicitanteSolicitud").val(solicitudACargar.NombreSolicitante);
		$("#FolioSolicitud").val(solicitudACargar.FolioSolicitud);
		$("#txtSolicitanteRfc").val(solicitudACargar.RfcSolicitante);
		$("#txtContratanteSolicitud").val(solicitudACargar.NombreContratante);
		$("#txtContratanteRfc").val(solicitudACargar.RfcContratante);
		$("#Observaciones").val(solicitudACargar.Observaciones);
		$("#DeclaracionSolicitud").val(solicitudACargar.DeclaracionSolicitud);
		$("#Unidades").val(solicitudACargar.Unidades);
		$("#ValorUnidad").val(solicitudACargar.ValorUnidad);
		//$("#txtSumaAseguradaSolicitada").val(solicitudACargar.Unidades * solicitudACargar.ValorUnidad);
		$("#txtSumaAseguradaSolicitada").val(solicitudACargar.SumaAseguradaSolicitada);
		$("#txtSolicitanteDomicilio").val(solicitudACargar.DomicilioPersonaSolicitante);
		$("#txtSolicitanteCP").val(solicitudACargar.CpSolicitante);
		$("#txtSolicitanteMunicipio").val(solicitudACargar.MunicipioSolicitante);
		$("#txtSolicitanteEstado").val(solicitudACargar.EstadoSolicitante);
		$("#txtSolicitanteTelefono").val(solicitudACargar.TelefonoSolicitante);
		$("#txtContratanteDomicilio").val(solicitudACargar.DomicilioPersonaContratante);
		$("#txtContratanteCP").val(solicitudACargar.CpContratante);
		$("#txtContratanteMunicipio").val(solicitudACargar.MunicipioContratante);
		$("#txtContratanteEstado").val(solicitudACargar.EstadoContratante);
		$("#txtContratanteTelefono").val(solicitudACargar.TelefonoContratante);
		$("#txtTipoSeguroSolicitud").val(solicitudACargar.TipoSeguro);
		$("#txtSubTipoSeguroSolicitud").val(solicitudACargar.SubTipoSeguro);
		$("#txtMonedaSolicitud").val(solicitudACargar.Moneda);
		$("#txtEjercicioSolicitud").val(solicitudACargar.Ejercicio);
		$("#txtContratoReaseguro").val(solicitudACargar.NumeroContrato);
		$("#txtFolioPrograma").val(solicitudACargar.FolioPrograma);
		$("#varIdPersonaSolicitante").val(solicitudACargar.IdPersonaSolicitante);
		$("#varIdPersonaContratante").val(solicitudACargar.IdPersonaContratante);
		$("#varIdPersonaAsegurada").val(solicitudACargar.IdPersonaAsegurada);
		$("#varIdTipoPrograma").val(solicitudACargar.IdTipoPrograma);
		$("#txtAseguradoSolicitud").val(solicitudACargar.NombreAsegurado);
		$("#txtAseguradoRfc").val(solicitudACargar.RfcAsegurado);
		$("#txtAseguradoDomicilio").val(solicitudACargar.DomicilioPersonaAsegurado);
		$("#txtAseguradoCP").val(solicitudACargar.CpAsegurado);
		$("#txtAseguradoMunicipio").val(solicitudACargar.MunicipioAsegurado);
		$("#txtAseguradoEstado").val(solicitudACargar.EstadoAsegurado);
		$("#txtAseguradoTelefono").val(solicitudACargar.TelefonoAsegurado);
		Dajaxice.Programas.obtener_cobertura_con_idprograma(cargarCoberturasPrograma, {'idPrograma':$('#varIdTipoPrograma').val()});
		if (solicitudACargar.TieneRelacionAnexaSolicitud){
			$("#btnGuardarSolicitud").hide();
			$("#DeclaracionSolicitud").prop("disabled",true);
			$("#btnBuscarPersonaSolicitante").hide();
			$("#btnBuscarPersonaAsegurada").hide();
			$("#btnBuscarPersonaContratante").hide();
			$("#btnBuscarPersonaBeneficiario").hide();
			$("#btnBuscarProgramaSolicitud").hide();
			$("#Unidades").prop("disabled",true);
			$("#ValorUnidad").prop("disabled",true);
			$("#Observaciones").prop("disabled",true);
		}
	}else{
		alertify.alert("Solicitud no encontrada");
		$("#btnGuardarSolicitud").attr("disabled", true);
	}
}

function cargarTablaBeneficiariosSolicitud(dato){ //Función que obtiene los beneficiarios de una solicitud
	var contenido = $('.tblPersonaBeneficiarioSolicitud tbody');
	contenido.html('');
	
	if(dato.beneficiariosSolicitud)
	{
		$.each(dato.beneficiariosSolicitud, function(i,elemento)
		{
			if (elemento.TieneRelacionAnexaSolicitud){
				linkEliminarBeneficiarios = '';
			}else{
				linkEliminarBeneficiarios = '<td><a onclick="eliminarBeneficiariosDeTabla($(this));" href="#"><i class="icon-remove"></i></a></td>';
			}
			$('<tr><td style="display: none;">'+elemento.IdPersonaBeneficiario+'</td><td style="display: none;">'+elemento.IdBeneficiario+'</td><td>'+elemento.NombrePersonaBeneficiario+'</td><td>'+elemento.DomicilioPersonaBeneficiario+'</td><td>'+elemento.RfcPersonaBeneficiario+'</td>'+linkEliminarBeneficiarios+'</tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.success('La solicitud no tiene beneficiarios');
	}
}