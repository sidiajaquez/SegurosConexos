$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario persona.
	$.ajaxSetup({
		beforeSend: function(xhr, settings){
			if (settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
			$("#loading").html("<img src='/static/img/horizontalEight.gif' /> ");
		}
	});	
	activarMenu();
	$("#txtFechaFinal").val(fechaActual());
	$("#txtFechaInicio").val(primerDiaMes());
	$("#txtFechaFinal").datepicker({
		firstDay: 1
	});
	$("#txtFechaInicio").datepicker({
		firstDay: 1
	});
	//Configuracion del chosen de los contratos de reaseguro del fondo
	$("#cmbContrato").chosen({allow_single_deselect:true,no_results_text:'No se encontro'});
	//Configuracion del chosen para el tipo de moneda segun el contrato seleccionado
	$("#cmbMoneda").chosen({allow_single_deselect:true,no_results_text:'No se encontro'});
	//Configuracion del evento chosen de los contratos
	$("#cmbContrato").chosen().change(function(evt,params){
		$("#cmbMoneda").html("");
		if (!params){
			//Limpiar caja de texto de las monedas cuando no exista nada
			$("#cmbMoneda").trigger('chosen:updated');
		}else{
			cargarCmbMonedas(params.selected);
		}
	});
	//funciones de los botones
	$("#btnLimpiar").on("click",limpiarCampos);
	$("#btnGenerarReporte").on("click",generarReporte);
	$("#btnExportarBordereaux").on("click",exportarExcel);
	//se oculta la tabla del reporte bordereaux y el boton de exportar
	$(".tblBordereaux").hide();
	$("#tabla").hide();
	$("#btnExportarBordereaux").hide();
}

//Creacion del objeto para el envio de parametros
dataBordereaux = new Object();

var exportarExcel = function(){ //Exportar reporte con informacion a excel
	document.location.href = "/ExportarExcelBordereaux/"+dataBordereaux.IdContratoFondo+"/"+dataBordereaux.IdTipoMoneda+"/"+dataBordereaux.FechaInicio+"/"+dataBordereaux.FechaFinal;
	return false;
}

var CBExportarExcelBordereaux = function(){
	alert('bien');
}

var generarReporte = function(){ //Generacion del reporte bordereaux segun parametros del usuario
	FechaInicio = $("#txtFechaInicio").val();
	FechaFinal = $("#txtFechaFinal").val();
	dataBordereaux.IdContratoFondo = $("#cmbContrato").val();
	dataBordereaux.IdTipoMoneda = $("#cmbMoneda").val();
	dataBordereaux.FechaInicio = FechaInicio.substr(6,4) + "-" + FechaInicio.substr(3,2) + "-" + FechaInicio.substr(0,2);
	dataBordereaux.FechaFinal = FechaFinal.substr(6,4) + "-" + FechaFinal.substr(3,2) + "-" + FechaFinal.substr(0,2);
	FechaInicio = FechaInicio.substr(3,2) + "/" + FechaInicio.substr(0,2) + "/" + FechaInicio.substr(6,4);
	FechaFinal = FechaFinal.substr(3,2) + "/" + FechaFinal.substr(0,2) + "/" + FechaFinal.substr(6,4);
	if (dataBordereaux.IdContratoFondo==0){
		alertify.alert('Es necesario seleccionar un contrato de reaseguro');
		limpiarCampos();
	}else if ((Date.parse(FechaInicio)) > (Date.parse(FechaFinal))){
		alertify.alert('Error en fechas, la fecha de inicio no debe ser mayor a la fecha final del reporte');
		limpiarCampos();
	}else{
		//se envian los datos para el procesamiento via ajax
		//$.post('ReporteBordereaux/',{ReporteBordereaux:JSON.stringify(dataBordereaux)}, CBBordereaux);
		$.ajax({
			type:'POST',
			url: 'ReporteBordereaux/',
			data: {ReporteBordereaux:JSON.stringify(dataBordereaux)},
			success: CBBordereaux,
			error: function(xhr){
				alert('error: '+ xhr.statusText + xhr.responseText);
			},
			complete: function(){
				$("#loading").html('');
			}
		});
	}
	return false;
}

var CBBordereaux = function(bordereaux){ //Callback del reporte bordereaux
	var contenido = $('.tblBordereaux tbody');
	contenido.html('');
	if (bordereaux.length > 0) {
		$("#tabla").show();
		$(".tblBordereaux").show();
		$("#btnExportarBordereaux").show();		
		bordereaux.forEach(function (campo, valor){
			$('<tr><td>'+campo.NumeroConstancia+'</td><td></td><td>'+campo.NumeroEndoso+'</td><td>'+campo.TipoEndoso+'</td><td>'+campo.SocioAsegurado+'</td><td>'+campo.Producto+'</td><td>'+
			campo.VODesde+'</td><td>'+campo.VOHasta+'</td><td></td><td></td><td>'+campo.Estado+'</td><td>'+campo.Municipio+'</td><td>'+campo.CP+'</td><td></td><td>'+campo.NombreDelBien+'</td><td>'+
			campo.NumeroBienes+'</td><td></td><td></td><td>'+campo.SumaAseguradaContenidos+'</td><td>'+campo.SumaAseguradaTotal+'</td><td>'+campo.Ramo+'</td><td>'+
			campo.RiesgoProtegido+'</td><td>'+campo.PorcentajeFondo+'</td><td>'+campo.ImporteFondo+'</td><td>'+campo.PorcentajeReaseguro+'</td><td>'+
			campo.ImporteReaseguro+'</td><td>'+campo.PorcentajeTotal+'</td><td>'+campo.ImporteTotal+'</td><td></td><td></td><td></td><td>'+campo.FechaPago+'</td><td>'+campo.FormaPago+'</td><td></td><td></td><td></td><td>'+campo.Observaciones+'</td><tr>').appendTo(contenido);
		});
	}else{
		alertify.alert('No existe informacion para mostrar');
		limpiarCampos();
	}
}

var cargarCmbMonedas = function(idContratoReaseguro){ //Se carga el tipo de la moneda segun el contrato seleccionado
	Dajaxice.Reporteador.MonedaContratoReaseguro(CBMoneda,{'IdContratoReaseguro':idContratoReaseguro});
}

var CBMoneda = function(data){ //CallBack de la funcion de ajax MonedaContratoReaseguro
	data.Monedas.forEach(function (descripcion, valor){
		$('#cmbMoneda').append("<option value='"+descripcion.IdMoneda+"'>"+descripcion.DescripcionMoneda+"</option>");
	});
	$("#cmbMoneda").trigger('chosen:updated');	
}

var limpiarCampos = function(){ //Funcion para limpiar los campos del reporte bordereaux
	$("#cmbContrato").val('').trigger('chosen:updated');
	$("#cmbMoneda").html("");
	$("#cmbMoneda").trigger('chosen:updated');
	$("#txtFechaFinal").val(fechaActual());
	$("#txtFechaInicio").val(primerDiaMes());
	$(".tblBordereaux").hide();
	$("#tabla").hide();
	$("#btnExportarBordereaux").hide();
	return false;
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

var fechaActual = function(){ // Función que genera y devuelve la fecha de hoy.
	var currentTime = new Date();
	var day = ("0" + currentTime.getDate()).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return (day+'/'+month+'/'+year);
}

var primerDiaMes = function(){ //Funcion para poner en fecha Inicial el primer dia del mes
	var currentTime = new Date();
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return ('01/'+month+'/'+year);
}