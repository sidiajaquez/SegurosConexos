$(document).on('ready',inicio);

var map;

function inicio(){ // Función que inicia las variables y los eventos de los controles
	activarMenu();
	$("#SumaAseguradaSolicitada").mask("000,000,000,000,000.00", {reverse:true});
	$("#ValorPorUnidad").mask("000,000,000,000,000.00", {reverse:true});
	$("#ValorUnitario").mask("000,000,000,000,000.00", {reverse:true});
	$("#Cantidad").mask("000,000,000,000,000", {reverse:true});
	$("#btnCancelarRelacionAnexaActaVerificacion").on("click",cancelarRelacionAnexaActaVerificacion);
	generarMapa();
	$("#UbicacionBienLat").focus();
	$("#btnAgregarBienModal").on("click",limpiarModalAgregarBien);
	$("#btnAceptarBienEditable").on("click",modificarBien);
	$("#FechaBien").val(fechaActual());
	$("#FechaBien").datepicker({
		firstDay: 1
	});
	modalDescripcionBienes();
	$("#btnAgregarBien").on("click",agregarBienTabla);
	$("#btnGuardarRelacionAnexaActaVerificacion").on("click",guardarRelacionAnexaActaVerificacion);
	tablaBusquedaMdlCP();
	$("#btnBuscarCP").on("click",buscarCPSepomex);
	$("#btnBuscarMdlCP").on("click",limpiarMdlBusquedaCP);
	if ($("#varIdRelacionAnexaActaVerificacion").val()!=''){
		$("#btnVistaPrevia").attr("disabled",false);
	}
	$("#btnVistaPrevia").on("click",reporteActaVerificacionRelacionAnexa);
}

var reporteActaVerificacionRelacionAnexa = function(){ //Envia el IdSolicitud para generar la impresion de la relacion anexa al acta de verificacion
	location.href = '/ReporteRelacionAnexaActaVerificacion/'+ $("#varIdSolicitud").val();
	return false;
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

var guardarRelacionAnexaActaVerificacion = function(){ //Funcion que permite guardar la relacion anexa al acta de verificacion 
	if (pasarComprobaciones()){
		descripcionContenidos = obtieneDatosTabla (".tblDescripcionDetalladaBien");
		if ($("#varIdRelacionAnexaActaVerificacion").val()==''){
			Dajaxice.Solicitud.guardar_relacion_anexa_acta_verificacion(Dajax.process,{'frmRelacionAnexaActaVerificacion':$('#FormularioRelacionAnexaActaVerificacion').serialize(true),'contenidos':validarArrayVacio(descripcionContenidos)});
			$("#btnGuardarRelacionAnexaActaVerificacion").attr("disabled", true);
			$("#btnVistaPrevia").attr("disabled",false);
		}else{ // Si existe valor es porque es una modificacion
			alertify.confirm("¿Desea modificar la relación anexa?", function (e) {
			    if (e) {
			    	Dajaxice.Solicitud.guardar_relacion_anexa_acta_verificacion(Dajax.process,{'frmRelacionAnexaActaVerificacion':$('#FormularioRelacionAnexaActaVerificacion').serialize(true),'contenidos':validarArrayVacio(descripcionContenidos)});
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

function mensajeRelAnexa(folioRelAnexa){ //Funcion que recibe el numero de la relacion anexa al acta de verificacion, de la funcion Dajaxice.Solicitud.guardar_relacion_anexa_acta_verificacion para mostrarla en un alert
	alertify.alert('Relación Anexa Guardada con el Folio: '+ folioRelAnexa);
}

function pasarComprobaciones(){ //Comprobar el formulario de relacion anexa al acta de verificacion para guardar la informacion
	listaBienes = obtieneDatosTabla (".tblDescripcionDetalladaBien");
	if ($("#UbicacionBienLat").val() == '' || $("#UbicacionBienLng").val() == '' || $("#DescripcionBienAsegurado").val() == '' || $('#CP').val() == '' || (listaBienes.length == 0)){
		return false;
	}
	return true;
}

function agregarBienTabla(){ //Funcion que agrega la descripcion del Bien en la tabla de los bienes
	var contenido = $('.tblDescripcionDetalladaBien tbody');
	
	if (validarModalDescripcionBienes()){
		cantidad = replaceAll($("#Cantidad").val(),",","");
		valorUnitario = replaceAll($("#ValorUnitario").val(),",","");
		sumaAsegurada = cantidad * valorUnitario;		
		$("#SumaAseguradaBienTemporal").val(sumaAsegurada.toFixed(2));
		$("#SumaAseguradaBienTemporal").mask("000,000,000,000,000.00", {reverse:true});
		$("<tr><td style='display:none;'></td><td>"+$("#NombreEquipo").val().toUpperCase()+"</td><td>"+$("#Marca").val().toUpperCase()+"</td><td>"+$("#Modelo").val().toUpperCase()+"</td><td>"+$("#Serie").val().toUpperCase()+"</td><td>"+$("#DocumentacionEvaluacion").val()+"</td><td>"+$("#FechaBien").val()+"</td><td style='display:none;'>"+cantidad+"</td><td style='display:none;'>"+valorUnitario+"</td><td>"+$("#Cantidad").val()+"</td><td>"+$("#ValorUnitario").val()+"</td><td>"+$("#SumaAseguradaBienTemporal").val()+"</td><td><a onclick='quitarBien($(this),2);'><i class='icon-remove'></i></a></td></tr>").appendTo(contenido);
		recalcularSumaAsegurada();
		$(".close").click();
	}
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

var cancelarRelacionAnexaActaVerificacion = function(){ //Funcion que regresa al listado de las actas de verificacion
	location.href= '/ListadoActasVerificacion/';
	return false;
}

var eliminarBien = function(eliminarRegistro){ //funcion que elimina los bienes directamente desde la tabla
	alertify.confirm("¿Eliminar Registro?", function (e) {
	    if (e) {
	    	eliminarRegistro.parent().parent().remove();
			var rowEliminar = eliminarRegistro.closest("tr");
			Dajaxice.Solicitud.eliminar_descripcion_bien(Dajax.process, {'idDescripcionBien':rowEliminar.children('td')[0].innerText,'opcion':2});
			alertify.success("Registro eliminado correctamente");
			recalcularSumaAsegurada();
	    }
	});	
	return false;
}

var quitarBien = function(quitarRegistro,opcion){ //Quita el bien de la tabla descripcion detallada de los bienes
	if (opcion == 1){
		quitarRegistro.parent().parent().parent().parent().parent().remove();
	}else{
		quitarRegistro.parent().parent().remove();
	}
   	recalcularSumaAsegurada();
	return false;	
}

var limpiarModalAgregarBien = function(){ //Funcion que Limpia los campos de texto de la ventana modal
	$("#NombreEquipo").val('');
	$("#Marca").val('');
	$("#Modelo").val('');
	$("#Serie").val('');
	$("#DocumentacionEvaluacion").val('');
	$("#Cantidad").val('');
	$("#ValorUnitario").val('');
	$("#FechaBien").val(fechaActual());
	$("#btnAceptarBienEditable").css("display","none");
	$("#btnAgregarBien").css("display","inline");
}

var editarBienModal = function(editarRegistro){ //Funcion que permite editar los datos de la tabla de la descripcion de los bienes en la ventana modal
	var bienEditable = new bienAsegurable(editarRegistro);
	$("#idBien").val(bienEditable.idBien);
	$("#NombreEquipo").val(bienEditable.nombreEquipo);
	$("#Marca").val(bienEditable.marca);
	$("#Modelo").val(bienEditable.modelo);
	$("#Serie").val(bienEditable.noSerie);
	$("#DocumentacionEvaluacion").val(bienEditable.documentacion);
	$("#FechaBien").val(bienEditable.fechaBien);
	$("#Cantidad").val(bienEditable.cantidad);
	$("#ValorUnitario").val(bienEditable.valorUnitario);
	$("#btnAgregarBien").css("display","none");
	$("#btnAceptarBienEditable").css("display","inline");
}

var modificarBien = function () { //Funcion para aceptar la modificacion del bien una vez que se modifiquen sus valores
	$('.tblDescripcionDetalladaBien tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 0:
					if ($(this).text() == $("#idBien").val()){ //Se edita el renglon de la tabla
						$(this).parent().children('td')[1].innerText = $("#NombreEquipo").val().toUpperCase();
						$(this).parent().children('td')[2].innerText = $("#Marca").val().toUpperCase();
						$(this).parent().children('td')[3].innerText = $("#Modelo").val().toUpperCase();
						$(this).parent().children('td')[4].innerText = $("#Serie").val().toUpperCase();
						$(this).parent().children('td')[5].innerText = $("#DocumentacionEvaluacion").val();
						$(this).parent().children('td')[6].innerText = $("#FechaBien").val();
						cantidad = replaceAll($("#Cantidad").val(),",","");
						valorUnitario = replaceAll($("#ValorUnitario").val(),",","");
						sumaAsegurada = cantidad * valorUnitario;
						$("#SumaAseguradaBienTemporal").val(sumaAsegurada.toFixed(2));
						$("#SumaAseguradaBienTemporal").mask("000,000,000,000,000.00", {reverse:true});						
						$(this).parent().children('td')[7].innerText = cantidad;
						$(this).parent().children('td')[8].innerText = valorUnitario;
						$(this).parent().children('td')[9].innerText = $("#Cantidad").val();
						$(this).parent().children('td')[10].innerText = $("#ValorUnitario").val();
						$(this).parent().children('td')[11].innerText = $("#SumaAseguradaBienTemporal").val();
						recalcularSumaAsegurada();
					}
					break;
			}
		});
	});
	$(".close").click();
}

var recalcularSumaAsegurada = function (){ //Funcion que recalcula la cantidad de suma asegurada
	sumaAseguradaAcumulada = 0;
	$('.tblDescripcionDetalladaBien tbody').children('tr').each(function(i){
		$(this).children('td').each(function(i2){
			switch(i2){
				case 11:
					sumaAseguradaBien = replaceAll($(this).text(),",","");
					sumaAseguradaAcumulada = parseFloat(sumaAseguradaAcumulada) + parseFloat(sumaAseguradaBien);
			}
		});
	});						
	$("#SumaAseguradaTotal").val(sumaAseguradaAcumulada.toFixed(2));
	$("#SumaAseguradaTotal").mask("000,000,000,000,000.00", {reverse:true});	
}

function replaceAll( text, busca, reemplaza ){ //Reemplaza todos los caracteres que se encuentren en una cadena de texto
	while (text.toString().indexOf(busca) != -1)
		text = text.toString().replace(busca,reemplaza);
	return text;
}

var bienAsegurable = function (data){ //Clase para definir lols atributos del bien asegurable
	var rowData = data.closest("tr");
	this.idBien = rowData.children('td')[0].innerText;
	this.nombreEquipo = rowData.children('td')[1].innerText;
	this.marca = rowData.children('td')[2].innerText;
	this.modelo = rowData.children('td')[3].innerText;
	this.noSerie = rowData.children('td')[4].innerText;
	this.documentacion = rowData.children('td')[5].innerText;
	this.fechaBien = rowData.children('td')[6].innerText;
	this.cantidad = rowData.children('td')[9].innerText;
	this.valorUnitario = rowData.children('td')[10].innerText;
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