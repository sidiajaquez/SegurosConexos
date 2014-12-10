$(document).on('ready',inicio);

var map;

function inicio(){ // Función que inicia las variables y los eventos de los controles
	activarMenu();
	$("#SumaAseguradaSolicitada").mask("000,000,000,000,000.00", {reverse:true});
	$("#ValorPorUnidad").mask("000,000,000,000,000.00", {reverse:true});
	generarMapa();
	$("#MedidasSeguridad").focus();
	$("#btnAgregarMedidaSeguridad").on("click",agregarMedidasSeguridadaTabla);
	$('#btnCancelarActaVerificacionSolicitud').on("click",limpiarFormularioActaVerificacion);
	$("#btnGuardarActaVerificacionSolicitud").on("click",guardarActaVerificacion);
	$("#btnActaVerificacionCampo").on("click",generarActaVerificacionCampo);
		
	if ($("#varIdActaVerificacionSolicitud").val() == '')
	{
		$('#btnVistaPrevia').attr('disabled', 'true');
	}
	else
	{
		$("#btnVistaPrevia").on("click", vistaPrevia);
	}
}

function vistaPrevia(){ // Función que permite mostrar la solicitud seleccionada.
	location.href = '/ReporteActaVerificacion/' + $("#varIdSolicitud").val();
}

var generarActaVerificacionCampo = function(){ //Función que permite generar el acta de verificacion de campo para dictaminar la solicitud una vez realizada la inspeccion de campo
	alertify.set({ labels: {
	    ok     : "Positivo",
	    cancel : "Negativo"
	}});
	
	alertify.confirm("¿Se dictamina que la verificación fue?", function (e) {
	    if (e) {
	    	Dajaxice.Solicitud.dictaminar_solicitud(Dajax.process,{'idSolicitud':$("#varIdSolicitud").val(), 'idActaVerificacionSolicitud':$("#varIdActaVerificacionSolicitud").val(),'dictamen':1});
			alertify.success("La solicitud se ha especificado como positiva");
	    }else{
	    	Dajaxice.Solicitud.dictaminar_solicitud(Dajax.process,{'idSolicitud':$("#varIdSolicitud").val(),'idActaVerificacionSolicitud':$("#varIdActaVerificacionSolicitud").val(),'dictamen':0});
	    	alertify.success("La solicitud se ha especificado como negativa");
	    }
		$("#btnGuardarActaVerificacionSolicitud").attr("disabled", true);
		$("#btnActaVerificacionCampo").attr("disabled", true);
	});
	return false;
}

var guardarActaVerificacion = function(){ //Funcion para guardar el acta de verificacion
	if (pasarComprobaciones()){
		medidasSeguridad = obtieneDatosTabla (".tblMedidaSeguridad");
		if ($("#varIdActaVerificacionSolicitud").val() == ''){
			Dajaxice.Solicitud.guardar_acta_verificacion(Dajax.process,{'dictamenInspeccion':$("#DictamenInspeccion").val(), 'medidaSeguridad':validarArrayVacio(medidasSeguridad), 'idSolicitud':$("#varIdSolicitud").val(),'idActaVerificacionSolicitud':$("#varIdActaVerificacionSolicitud").val()});
			$("#btnGuardarActaVerificacionSolicitud").attr("disabled", true);
			$("#btnCancelarActaVerificacionSolicitud").attr("disabled", true);
		}else{ //Es una modificación
			alertify.set({ labels: {
			    ok     : "Aceptar",
			    cancel : "Cancelar"
			} });
			alertify.confirm("¿Desea modificar el acta de verificación?", function (e) {
			    if (e) {
			    	Dajaxice.Solicitud.guardar_acta_verificacion(Dajax.process,{'dictamenInspeccion':$("#DictamenInspeccion").val(), 'medidaSeguridad':validarArrayVacio(medidasSeguridad), 'idSolicitud':$("#varIdSolicitud").val(),'idActaVerificacionSolicitud':$("#varIdActaVerificacionSolicitud").val()});
					alertify.success("Acta de verificación modificada");
					$("#MedidasSeguridad").val('');
					$("#MedidasSeguridad").focus();
			    }
			});
		}
	}else{
		alertify.alert("Falta información");
	}
	return false;
}

var pasarComprobaciones = function(){ //Funcion que comrpueba los datos antes de ser almacenados en la base de datos
	listaMedidaSeguridad = obtieneDatosTabla (".tblMedidaSeguridad");
	if ($("#DictamenInspeccion").val() == '' || (listaMedidaSeguridad.length == 0)){
		return false;
	}
	return true;	
}

var limpiarFormularioActaVerificacion = function(){ //Funcion que limpia los campos habilitados del formulario acta verificacion
	$("#MedidasSeguridad").val('');
	$(".tblMedidaSeguridad tbody").html('');
	$("#DictamenInspeccion").val('');
	$("#MedidasSeguridad").focus();
	return false;
}

var agregarMedidasSeguridadaTabla = function(){ //Funcion que permite agregar las medidas de seguridad seleccionadas de un combo a una tabla
	var contenido = $(".tblMedidaSeguridad tbody");
	medidaSeguridad = $("#MedidasSeguridad option:selected").val();
	registroDuplicado = comprobarMedidaSeguridadDuplicada(medidaSeguridad);
	if (medidaSeguridad != ''){
		if (registroDuplicado){
			alertify.alert('La medida de seguridad ya se encuentra registrada');
		}else{
			$('<tr><td style="display:none;"></td><td>'+medidaSeguridad+'</td><td><a onclick="eliminarMedidaSeguridad($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		}
	}else{
		alertify.alert('No se ha elegido una medida de seguridad');
	}
}

var eliminarMedidaSeguridad = function (eliminarRegistro){ //Funcion que elimina las medidas de seguridad de la tabla tblmedidaSeguridad
	alertify.set({ labels: {
	    ok     : "Aceptar",
	    cancel : "Cancelar"
	} });
	alertify.confirm("¿Eliminar Registro?", function (e) {
	    if (e) {
	    	eliminarRegistro.parent().parent().remove();
			var rowEliminar = eliminarRegistro.closest("tr");
			if (rowEliminar.children('td')[0].innerText != ''){
				Dajaxice.Solicitud.eliminar_medida_seguridad(Dajax.process, {'idMedidaSeguridad':rowEliminar.children('td')[0].innerText});
			}
			alertify.success("La medida de seguridad fue eliminada correctamente");
			$("#MedidasSeguridad").focus();
	    }
	});	
	return false;	
}

function comprobarMedidaSeguridadDuplicada(Medida){ //Funcion que regresa true si la medida de seguridad se encuentra agregado en la tabla de Medidas de seguridad
	registroRepetido = false;
	$('.tblMedidaSeguridad tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 1:
					if ($(this).text() == Medida){
						registroRepetido = true;
					}
					break;
			}
		});
	});
	return registroRepetido;	
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

var generarMapa = function(){ //Se crea una marca de acuerdo a las coordenadas capturadas
    map = new GMaps({
        div: '#map',
        lat: $('#UbicacionBienLat').val(),
        lng: $('#UbicacionBienLng').val()
      });
    map.addMarker({
        lat: $('#UbicacionBienLat').val(),
        lng: $('#UbicacionBienLng').val(),
        title: $('#SubTipoSeguroSolicitud').val(),
        click: function(e){
        	alertify.log($('#ObservacionesSolicitud').val());
        }
    });	
}

function mensajeActaVerificacion(folioActaVerificacion){ //Funcion que recibe el numero del acta de verificacion  de la funcion Dajaxice.Solicitud.guardar_acta_verificacion para mostrarla en un alert
	alertify.alert('Acta de Verificacion Guardada con el Folio: '+ folioActaVerificacion);
}