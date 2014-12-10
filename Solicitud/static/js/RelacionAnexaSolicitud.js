$(document).on('ready',inicio);

var map;

function inicio(){	// Función que inicia las variables y los eventos de los controles del listado de solicitudes.
	$("#UbicacionBienLat").focus();
	$("#ValorUnitario").mask("000,000,000,000,000.00", {reverse:true});
	$("#Cantidad").mask("000,000,000,000,000", {reverse:true});
	$("#SumaAseguradaSolicitada").mask("000,000,000,000,000.00", {reverse:true});
	$("#ValorPorUnidad").mask("000,000,000,000,000.00", {reverse:true});
	tablaBusquedaMdlCP();
	$("#btnBuscarCP").on("click",buscarCPSepomex);
	$("#btnBuscarMdlCP").on("click",limpiarMdlBusquedaCP);
		
	$("#FechaBien").val(fechaActual());
	$("#FechaBien").datepicker({
		firstDay: 1
	});
	activarMenu();
	if ($("#UbicacionBienLat").val() != '' && $("#UbicacionBienLng").val()!=''){
		generarMapa();
	}else{
		Mapa();
	}
	$("#UbicacionBienLat,#UbicacionBienLng").on({
		change:generarMapa,
		keydown:generarMapa,
		keyup:generarMapa
	});
	$("#btnAgregarBienModal").on("click",limpiarModalAgregarBien);
	modalDescripcionBienes();
	$("#btnAgregarBien").on("click",agregarBienTabla);	
	$("#btnCancelarRelacionAnexaSolicitud").on("click",limpiarFormularioRelacionAnexaSolicitud);
	$("#btnGuardarRelacionAnexaSolicitud").on("click",guardarRelacionAnexaSolicitud);
	
	if ($("#RestanteSumaAseguradaSolicitadaTotal").val() == 0){
		$("#btnAgregarBienModal").attr("disabled", true);
	}
	
	if ($("#varIdRelacionAnexaSolicitud").val() == null || $("#varIdRelacionAnexaSolicitud").val() == '')
	{
		$('#btnVistaPrevia').attr('disabled', 'true');
	}
	$("#btnVistaPrevia").on("click", vistaPrevia);
}

function tablaBusquedaMdlCP(){ //Funcion para interactuar con la tabla de la ventana modal Busqueda CP
	$("#mdlBuscarCP").on('shown', function() {
	    $("#txtBuscarCP").focus();
	});
	$('.tblBusquedaCP tbody').on('mouseover', 'tr', function(event) { //toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});
	$('.tblBusquedaCP tbody').on('mouseout', 'tr', function(event) { //evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});
	$('.tblBusquedaCP tbody').on('click', 'tr', function(event) { // permite agregar los datos del programa en los input text correspondientes.		
		//Comprobar si el municipio de la ubicacion del bien esta dentro del area de influencia del programa
		areaInfluencia = comprobarAreaInfluencia (($(this).children('td')[3].innerText).toUpperCase());
		if (areaInfluencia.municipioAutorizado){
			$('#CP').val($(this).children('td')[0].innerText);
			$(".close").click();
		}else{
			$("#txtBuscarCP").focus();
			alertify.alert("El área no se encuentra en cobertura por el programa de aseguramiento");
			$("#txtBuscarCP").val('');
		}
	});
}

function comprobarAreaInfluencia(municipio){ //Funcion que verifica el municipio de la busqueda del catalogo de sepomex para compararlo con el area de influencia del programa
	var registro = new Object();
	registro.municipioAutorizado = false;
	$('.tblMunicipios tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 0:
					if ($(this).text() == municipio){
						registro.municipioAutorizado = true;
					}
					break;
			}
		});
	});
	return registro;	
}

function buscarCPSepomex(){ //Funcion para buscar el Codigo Postal en el catalogo de sepomex
	datosBuscar = $('#txtBuscarCP').val();
	if ($('#txtBuscarCP').val() != ''){
		Dajaxice.Direcciones.buscar_sepomex(sepomexCallBack,{'datosBuscar':datosBuscar});
	}
	return false;
}

function limpiarMdlBusquedaCP(){ //Limpia el text de busqueda y la tabla del resultado SEPOMEX
	$('#txtBuscarCP').val('');
	$('.tblBusquedaCP tbody').html('');
}

function sepomexCallBack(data){ //Obtiene la informacion de la busqueda de la direccion de sepomex que recibe del metodo buscar_sepomex de ajax.py, los datos de la busqueda se agregan a la tabla busquedaSepomex de la ventana modal
	var contenido = $('.tblBusquedaCP tbody');
	contenido.html('');
	if(data.sepomex){
		$.each(data.sepomex, function(i,elemento){
			$('<tr><td>'+elemento.Cp+'</td><td>'+elemento.Asentamiento+'</td><td>'+elemento.Ciudad+'</td><td>'+elemento.Municipio+'</td><td>'+elemento.Estado+'</td></tr>').appendTo(contenido);
		});
	}else{
		alertify.alert('No se encontro información');
	}
}

function vistaPrevia(){ // Función que permite mostrar la plantilla reporte de las relaciones anexas de la solicitud de aseguramiento.
	location.href = '/ReporteRelacionAnexa/' + $("#varIdSolicitud").val();
}

function guardarRelacionAnexaSolicitud(){ //Funcion que permite guardar la relacion anexa a la solicitud de aseguramiento
	if (pasarComprobaciones()){
		descripcionContenidos = obtieneDatosTabla (".tblDescripcionDetalladaBien");
		if ($("#varIdRelacionAnexaSolicitud").val()==''){
			Dajaxice.Solicitud.guardar_relacion_anexa(Dajax.process,{'frmRelacionAnexa':$('#FormularioRelacionAnexaSolicitudAseguramiento').serialize(true),'contenidos':validarArrayVacio(descripcionContenidos)});
			$("#btnGuardarRelacionAnexaSolicitud").attr("disabled", true);
			$("#btnCancelarRelacionAnexaSolicitud").attr("disabled", true);
		}else{ // Si existe valor es porque es una modificacion
			alertify.confirm("¿Desea modificar la relación anexa?", function (e) {
			    if (e) {
			    	Dajaxice.Solicitud.guardar_relacion_anexa(Dajax.process,{'frmRelacionAnexa':$('#FormularioRelacionAnexaSolicitudAseguramiento').serialize(true),'contenidos':validarArrayVacio(descripcionContenidos)});
					alertify.success("Relación anexa modificada");
					$("#UbicacionBienLat").focus();
			    }
			});
		}
	}else{
		alertify.alert("Se requiere ingresar información");
	}
	return false;
}

function mensajeRelAnexa(folioRelAnexa){ //Funcion que recibe el numero de la relacion anexa de la funcion Dajaxice.Solicitud.guardar_relacion_anexa para mostrarla en un alert
	$("#varIdRelacionAnexaSolicitud").val(folioRelAnexa);
	alertify.alert('Relación Anexa Guardada con el Folio: '+ folioRelAnexa);
	$('#btnVistaPrevia').attr('disabled', false);
}

function pasarComprobaciones(){ //Comprobar el formulario de relacion anexa a la solicitud para guardar la informacion
	listaBienes = obtieneDatosTabla (".tblDescripcionDetalladaBien");
	if ($("#UbicacionBienLat").val() == '' || $("#UbicacionBienLng").val() == '' || $("#DescripcionBienAsegurado").val() == '' || $('#CP').val() == '' || (listaBienes.length == 0)){
		return false;
	}
	if ($("#RestanteSumaAseguradaSolicitadaTotal").val()!=0){
		alertify.alert("No se ha especificado el total de la suma asegurada solicitada");
		return false;
	}
	return true;
}

function limpiarFormularioRelacionAnexaSolicitud(){ //Limpia la informacion de la relacion anexa
	$("#UbicacionBienLat").val('');
	$("#UbicacionBienLng").val('');
	$("#DescripcionBienAsegurado").val('');
	$("#ObservacionesSolicitante").val('');
	$("#SumaAseguradaSolicitadaTotal").val('0');
	$("#SumaAseguradaBienTemporal").val('');
	$("#RestanteSumaAseguradaSolicitadaTotal").val($("#SumaAseguradaSolicitada").val());
	$('.tblDescripcionDetalladaBien tbody').html('');
	$("#UbicacionBienLat").focus();
	$("#btnAgregarBienModal").attr("disabled", false);
	return false;
}

function agregarBienTabla(){ //Funcion que agrega la descripcion del Bien en la tabla de los bienes
	var contenido = $('.tblDescripcionDetalladaBien tbody');
	
	if (validarModalDescripcionBienes()){
		cantidad = replaceAll($("#Cantidad").val(),",","");
		valorUnitario = replaceAll($("#ValorUnitario").val(),",","");
		sumaAsegurada = cantidad * valorUnitario;		
		sumaAseguradaSolicitada = replaceAll($("#SumaAseguradaSolicitadaTotal").val(),",","");
		sumaAseguradaSolicitadaAcumulada = parseFloat(sumaAsegurada.toFixed(2)) + parseFloat(sumaAseguradaSolicitada);
		restaSumaAseguradaSolicitada = replaceAll($("#SumaAseguradaSolicitada").val(),",","");
		restaSumaAseguradaAcumulada = parseFloat(restaSumaAseguradaSolicitada) - parseFloat(sumaAseguradaSolicitadaAcumulada);
		
		if (parseFloat(restaSumaAseguradaAcumulada.toFixed(2)) >= 0){
			$("#SumaAseguradaBienTemporal").val(sumaAsegurada.toFixed(2));
			$("#SumaAseguradaBienTemporal").mask("000,000,000,000,000.00", {reverse:true});
			$("<tr><td style='display:none;'></td><td>"+$("#NombreEquipo").val().toUpperCase()+"</td><td>"+$("#Marca").val().toUpperCase()+"</td><td>"+$("#Modelo").val().toUpperCase()+"</td><td>"+$("#Serie").val().toUpperCase()+"</td><td>"+$("#DocumentacionEvaluacion").val()+"</td><td>"+$("#FechaBien").val()+"</td><td style='display:none;'>"+cantidad+"</td><td style='display:none;'>"+valorUnitario+"</td><td>"+$("#Cantidad").val()+"</td><td>"+$("#ValorUnitario").val()+"</td><td>"+$("#SumaAseguradaBienTemporal").val()+"</td><td><a onclick='eliminarDescripcionBien($(this));' href='#'><i class='icon-remove'></i></a></td></tr>").appendTo(contenido);
			$("#SumaAseguradaSolicitadaTotal").val(sumaAseguradaSolicitadaAcumulada.toFixed(2));
			$("#SumaAseguradaSolicitadaTotal").mask("000,000,000,000,000.00", {reverse:true});
			$("#RestanteSumaAseguradaSolicitadaTotal").val(restaSumaAseguradaAcumulada.toFixed(2));
			$("#RestanteSumaAseguradaSolicitadaTotal").mask("000,000,000,000,000.00", {reverse:true});
			$(".close").click();
		}else{
			alertify.alert("La suma asegurada solicitada es mayor que la especificada en la solicitud, falta por especificar: " + $("#RestanteSumaAseguradaSolicitadaTotal").val());
		}
		if (parseFloat(restaSumaAseguradaAcumulada.toFixed(2)) == 0){
			$("#btnAgregarBienModal").attr("disabled", true);
		}
	}
}

function eliminarDescripcionBien(eliminarRegistro){ //Funcion que elimina lla descripcion de los bienes y reajusta la suma asegurada solicitada
	alertify.confirm("¿Eliminar Registro?", function (e) {
	    if (e) {
	    	eliminarRegistro.parent().parent().remove();
			var rowEliminar = eliminarRegistro.closest("tr");
			if (rowEliminar.children('td')[0].innerText != ''){
				Dajaxice.Solicitud.eliminar_descripcion_bien(Dajax.process, {'idDescripcionBien':rowEliminar.children('td')[0].innerText, 'opcion':1});
				cantidadRegresada = replaceAll(rowEliminar.children('td')[9].innerText,",","");
			}else{
				cantidadRegresada = replaceAll(rowEliminar.children('td')[11].innerText,",","");				
			}
			alertify.success("El equipo fue eliminado correctamente");
			sumaAseguradaSolicitada = replaceAll($("#SumaAseguradaSolicitadaTotal").val(),",","");
			sumaAseguradaAcumulada = parseFloat(sumaAseguradaSolicitada) - parseFloat(cantidadRegresada);
			restaSumaAseguradaSolicitada = replaceAll($("#RestanteSumaAseguradaSolicitadaTotal").val(),",","");
			restaSumaAseguradaAcumulada = parseFloat(restaSumaAseguradaSolicitada) + parseFloat(cantidadRegresada);
			$("#SumaAseguradaSolicitadaTotal").val(sumaAseguradaAcumulada.toFixed(2));
			$("#SumaAseguradaSolicitadaTotal").mask("000,000,000,000,000.00", {reverse:true});
			$("#RestanteSumaAseguradaSolicitadaTotal").val(restaSumaAseguradaAcumulada.toFixed(2));
			$("#RestanteSumaAseguradaSolicitadaTotal").mask("000,000,000,000,000.00", {reverse:true});
			$("#btnAgregarBienModal").attr("disabled", false);
			$("#btnAgregarBienModal").focus();
	    }
	});	
	return false;	
}

function replaceAll( text, busca, reemplaza ){ //Reemplaza todos los caracteres que se encuentren en una cadena de texto
	while (text.toString().indexOf(busca) != -1)
		text = text.toString().replace(busca,reemplaza);
	return text;
}

function validarModalDescripcionBienes(){ //permite validar la ventana modal para agregar la descripcion detallada de los bienes o contenidos
	if ($("#NombreEquipo").val() == '' || $("#DocumentacionEvaluacion").val() == '' || $("#Cantidad").val() == '' || $("#ValorUnitario").val() == ''){
		alertify.alert("Faltan datos por especificar");
		return false;
	}
	return true;
}

function modalDescripcionBienes(){ //Manejo del Focus en la ventana modal para agregar la descripcion detallada de los bienes asegurados
	$("#mdlDescripcionBien").on('shown', function() {
	    $("#NombreEquipo").focus();
	});
}

function limpiarModalAgregarBien(){ //Funcion que Limpia los campos de texto de la ventana modal
	$("#NombreEquipo").val('');
	$("#Marca").val('');
	$("#Modelo").val('');
	$("#Serie").val('');
	$("#DocumentacionEvaluacion").val('');
	$("#Cantidad").val('');
	$("#ValorUnitario").val('');
	$("#FechaBien").val(fechaActual());
}

function generarMapa(){ //Se crea una marca de acuerdo a las coordenadas capturadas
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

function Mapa(){ //Creacion del mapa
	latitud=28.441525;
	longitud=-106.910126;
	map = new GMaps({
        el: '#map',
        lat: latitud,
        lng: longitud,
        zoom: 5,
        zoomControl : true,
        zoomControlOpt: {
            style : 'SMALL',
            position: 'TOP_LEFT'
        },
        panControl : true,
        streetViewControl : true,
        mapTypeControl: true,
        overviewMapControl: true
      });
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}