$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario endoso.​
	activarMenu();
	
	$("#btnBuscarConstancia").on("click", buscarConstanciasParaElDeclaracionEndoso);
	$("#btnAgregar").on("click", agregarElementoAtabla);
	$("#btnGuardarDeclaracion").on("click",guardarDeclaracionTransporte);
	$("#btnCancelarDeclaracion").on("click", limpiar_formulario_transporte);
	$("#btnListadoDeclaracion").on("click", regresarListadoDeclaracionesTransporte);
	$("#btnLimpiarTabla").on("click", limpiarTablaTransporte);
	$("#btnBuscarConstanciaModal").on("click", limpiarBuscadorConstancia);
	
    document.getElementById("txtRfc").readOnly = true;
	document.getElementById("txtNombre").readOnly = true;
	document.getElementById("txtDomicilio").readOnly = true;
	document.getElementById("txtTelefono").readOnly = true;
	document.getElementById("txtFolioConstancia").readOnly = true;
	document.getElementById("txtNumeroSolicitud").readOnly = true;
	document.getElementById("txtMoneda").readOnly = true;
	document.getElementById("txtEjercicio").readOnly = true;
	document.getElementById("txtSumaAseguradaTotal").readOnly = true;
	
	$("#dtpPeriodoInicio").datepicker({
		firstDay: 1
	});
	
	$("#dtpPeriodoFin").datepicker({
		firstDay: 1
	});
	
	$("#dtpFecha").datepicker({
		firstDay: 1
	});
	
	$("#txtCantidad,#txtSumaAseguradaUnitaria").on({
		change:calcularSumaAseguradaTotal,
		keydown:calcularSumaAseguradaTotal,
		keyup:calcularSumaAseguradaTotal
	});

	if ($("#varIdDeclaracionTransporte").val() != ''){
		validarControles();
		habilitarBotones();
	}
	else
	{
		$("#dtpFecha").val(fechaActual());
		$("#dtpPeriodoInicio").val(fechaPrimeraMes());		
		$("#dtpPeriodoFin").val(fechaUltimaMes());	
		deshabilitarBotones();
	}
	
	tabla_buscar_constancia();
}

function habilitarBotones(){ // Función que nos permite habilitar el boton de vista previa y el boton de cerrar periodo.
	$("#btnVistaPreviaDeclaracion").on("click", declaracionTransporteImpresion);
	$("#btnVistaPreviaDeclaracion").removeAttr("disabled");
	$("#btnCerrarPeriodo").on("click", cerrarPeriodo);
	$("#btnCerrarPeriodo").removeAttr("disabled");
}

function deshabilitarBotones(){ // Función que nos permite deshabilitar el boton de vista previa y el boton de cerrar periodo.
	$("#btnVistaPreviaDeclaracion").unbind("click");
	$("#btnVistaPreviaDeclaracion").attr("disabled","disabled");
	$("#btnCerrarPeriodo").unbind("click");
	$("#btnCerrarPeriodo").attr("disabled","disabled");
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

function declaracionTransporteImpresion() { // Función que permite imprimir la declaracion de endoso.
	window.open('/DeclaracionTransporteImpresion/' + $("#varIdDeclaracionTransporte").val());
}

function limpiarBuscadorConstancia(){ // Función que cierra el formulario modal buscadorConstancia.
	$("#txtBuscarConstancia").val('');
	var contenido = $('.tbl_buscar_constancia tbody');
	contenido.html('');	
}

function limpiarTablaTransporte(){ // Función que permite quitar los rows de la tabla de transporte.
	var contenido = $('.tabla_declaracion_transporte tbody');
	contenido.html('');
	var contenido1 = $('.tabla_endoso_totales tbody');
	contenido1.html('');
	$("#varCantidadFletes").val(0);
	$("#varSumaAseguradaUnitaria").val(0);
	$("#varSumaAseguradaTotal").val(0);
	$("#varImporteCuota").val(0);
	$('#dtpPeriodoInicio').attr('disabled',false);
	$('#dtpPeriodoFin').attr('disabled',false);
	
	$("#dtpPeriodoInicio").datepicker({
		firstDay: 1
	});
	
	$("#dtpPeriodoFin").datepicker({
		firstDay: 1
	});	
}

function limpiar_formulario_transporte(){ // Función que limpia los controles y las variables del formulario de la declaración transporte.
	if ($("#varIdDeclaracionTransporte").val() == '')
	{
		document.getElementById("formulario_transporte").reset();
		var contenido = $('.tabla_declaracion_transporte tbody');
		contenido.html('');
		var contenido1 = $('.tabla_endoso_totales tbody');
		contenido1.html('');
		$("#varDeclaracionTransporte").val('');
		$("#varIdConstancia").val('');
		$("#varIdPersona").val('');
		$("#varTotalTarifa").val('');
		$("#varPrima").val('');
		$("#varCantidadFletes").val('');
		$("#varSumaAseguradaUnitaria").val('');
		$("#varSumaAseguradaTotal").val('');
		$("#varImporteCuota").val('');
		
		$("#dtpPeriodoInicio").val(fechaPrimeraMes());
		
		$("#dtpPeriodoInicio").datepicker({
			firstDay: 1
		});
		
		$("#dtpPeriodoFin").val(fechaUltimaMes());
		
		$("#dtpPeriodoFin").datepicker({
			firstDay: 1
		});
		
		$('#dtpPeriodoInicio').attr('disabled',false);
		$('#dtpPeriodoFin').attr('disabled',false);
	}
	else
	{
		regresarListadoDeclaracionesTransporte();
	}
}

function regresarListadoDeclaracionesTransporte() { // Función que permite regresar al listado de las declaraciones de transportes.
	location.href = '/ListadoDeclaracionTransporte/';
}

function cerrarPeriodo() // Función que permite enviar un false a la declaración para indicar que esta ocupada.
{	
	alertify.confirm("Esto cerrara el periodo de la declaración de transporte ¿Desea continuar?", function (e)
	{
	    if (e)
	    {
	    	Dajaxice.Endoso.actualizar_cierre_periodo_transporte(Dajax.process,{'idDeclaracionTransporte':$("#varIdDeclaracionTransporte").val()});
	    	$('#btnCerrarPeriodo').attr('disabled', 'true');
	    	$('#btnCerrarPeriodo').unbind('click');
	    	alertify.success("Declaración transporte cerrada");
	    }
	});
	return false;
}

function validarControles(){ // Función que valida los controles del formulario cuando se agrega un nuevo row a la tabla.
	$('#dtpPeriodoInicio').attr('disabled',true);
	$('#dtpPeriodoFin').attr('disabled',true);
}

function calcularSumaAseguradaTotal(){ // Función que calcula la suma asegurada total cuando se ingresa un valor a la suma asegurada unitaria y a la total.
	
	var cantidad = $("#txtCantidad").val();
	var sumaAseguradaUnitaria = $("#txtSumaAseguradaUnitaria").val();
	
	if (cantidad == "")
	{
		cantidad = 0;
	}
	
	if (sumaAseguradaUnitaria == "")
	{
		sumaAseguradaUnitaria = 0;
	}
	
	var sumaAseguradaTotal = cantidad * sumaAseguradaUnitaria;
	$("#txtSumaAseguradaTotal").val(sumaAseguradaTotal);
}

function fechaActual(){ // Función que genera y devuelve la fecha de hoy.
	var currentTime = new Date();
	var day = ("0" + currentTime.getDate()).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return (day+'/'+month+'/'+year);
}

function obtencionDatosTablaEndoso(){ // Función que obtiene la información de la tabla tabla_declaracion_transporte y la agrega a un arreglo.
	var arrayEndoso = [];
	
	$('.tabla_declaracion_transporte tr').each(function(){
		var fila = $(this).find('td');
		
	    if (fila.length > 0)
	    {
			var arrayFilas = [];
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(0).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(1).html(),',','')); 			
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(2).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(3).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(4).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(5).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(6).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(7).html(),',',''));
			
			arrayEndoso.push(arrayFilas);
	    }
	});
	
	return arrayEndoso;
}

function guardarDeclaracionTransporte() // Función que envia el formulario para guardarlo en la base de datos.
{	
	if (pasarComprobacionesGuardar())
	{
		fechaPeriodoInicio = $("#dtpPeriodoInicio").val();
		fechaPeriodoFin = $("#dtpPeriodoFin").val();
				
		if ($("#varIdDeclaracionTransporte").val() == '')
		{
			Dajaxice.Endoso.guardar_declaracion_transporte(Dajax.process,{'formulario':$('#formulario_transporte').serialize(true), 'transportePorDia':validarArrayVacio(obtencionDatosTablaEndoso()),'fechaPeriodoInicio':fechaPeriodoInicio, 'fechaPeriodoFin':fechaPeriodoFin});
		}
		else
		{
			alertify.confirm("¿Desea modificar la declaración de transporte?", function (e)
			{
			    if (e)
			    {
			    	Dajaxice.Endoso.guardar_declaracion_transporte(Dajax.process,{'formulario':$('#formulario_transporte').serialize(true), 'transportePorDia':validarArrayVacio(obtencionDatosTablaEndoso()),'fechaPeriodoInicio':fechaPeriodoInicio, 'fechaPeriodoFin':fechaPeriodoFin});
			    	alertify.success("Declaración Modificada");
			    	window.setTimeout('obtener_declaracionesTransportePorUnidad()', 1000)
			    }
			});	
		}
	}
	
	return false;
}

function obtener_declaracionesTransportePorUnidad() // Función que permite cargar las declaraciones de transporte por unidad en la tabla.
{
	Dajaxice.Endoso.obtener_declaraciontransporte_por_unidad(cargarDeclaracionTransporte,{'idDeclaracionTransporte':$("#varIdDeclaracionTransporte").val()});
	return false;
}

function cargarDeclaracionTransporte(data) // Función que permite cargar las declaraciones de transporte por unidad en la tabla
{
	var contenido = $('.tabla_declaracion_transporte tbody');
	contenido.html('');
	
	if(data.declaracionesTransportePorUnidad)
	{
		$.each(data.declaracionesTransportePorUnidad, function(i,declaracion)
		{
			$('<tr><td style="display: none;">'+declaracion.IdDeclaracionTransportePorUnidad+'</td><td>'+formatCurrency(declaracion.Romaneaje,',','')+'</td><td>'+declaracion.Fecha+'</td><td>'+formatCurrency(declaracion.Cantidad,',','')+'</td><td>'+formatCurrency(declaracion.SumaAseguradaUnitaria,',','')+'</td><td>'+formatCurrency(declaracion.SumaAseguradaTotal,',','')+'</td><td>'+declaracion.Origen+'</td><td>'+declaracion.Destino+"</td><td><a href='#' title='Editar' onclick='actualizarTablaDeclaracionUnidad($(this));'><i class='icon-refresh'></i></a></td><td><a href='#' title='Editar' onclick='eliminarFilaUnidadPorDia($(this));'><i class='icon-remove-circle'></i></a></td></tr>").appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function mensajeDeclaracionTransporte(folioDelcaracionTransporte){ //Función que recibe el número de folio de la declaración de transporte de la función Dajaxice.Endoso.guardar_declaracion_transporte para mostrarla en un alert.
	$("#varIdDeclaracionTransporte").val(folioDelcaracionTransporte);
	habilitarBotones();
	obtener_declaracionesTransportePorUnidad();
	alertify.alert('Declaración de Transporte Guardado con el Folio: ' + folioDelcaracionTransporte);
}

function pasarComprobacionesGuardar(){ // Función que permite verificar que la información ingresada sea la correcta para mandar a guardar en la base de datos.
	if ($("#varIdConstancia").val() == "")
	{
		alertify.alert("Se requiere seleccionar una constancia continuar");
		return false;
	}
	
	return true;
}

function agregarElementoAtabla() // Función que permite agregar la información de los texts en la tabla.
{
	if (pasarComprobacionesAgregarElemento())
	{
		asignarValores();
		var varCantidadFletes = parseInt($("#varCantidadFletes").val()) + 1;
		$("#varCantidadFletes").val(varCantidadFletes);
		var varSumaAseguradaUnitaria = (parseFloat(replaceAll($("#varSumaAseguradaUnitaria").val(),',','')) + parseFloat($("#txtSumaAseguradaUnitaria").val())) / varCantidadFletes;
		$("#varSumaAseguradaUnitaria").val(varSumaAseguradaUnitaria);
		var varSumaAseguradaTotal = parseFloat(replaceAll($("#varSumaAseguradaTotal").val(),',','')) + parseFloat($("#txtSumaAseguradaTotal").val())		
		$("#varSumaAseguradaTotal").val(varSumaAseguradaTotal);
		var varImporteCuota = parseFloat(replaceAll($("#varSumaAseguradaTotal").val(),',','')) * parseFloat(replaceAll($("#varTotalTarifa").val(),',',''));
		$("#varImporteCuota").val(varImporteCuota);
		
		$("#varUltimaFechaIngresada").val($("#dtpFecha").val());
		
		var contenido = $('.tabla_declaracion_transporte tbody');
		$('<tr><td style="display:none;">'+''+'</td><td>'+formatInt($("#txtRomaneaje").val())+'</td><td>'+$("#dtpFecha").val()+'</td><td>'+formatInt($("#txtCantidad").val())+'</td><td>'+formatCurrency($("#txtSumaAseguradaUnitaria").val())+'</td><td>'+formatCurrency($("#txtSumaAseguradaTotal").val())+'</td><td>'+$("#txtOrigen").val().toUpperCase()+'</td><td>'+$("#txtDestino").val().toUpperCase()+"</td><td><a href='#' title='Editar' onclick='actualizarTablaDeclaracionUnidad($(this));'><i class='icon-refresh'></i></a></td><td><a href='#' title='Editar' onclick='eliminarFilaUnidadPorDia($(this));'><i class='icon-remove-circle'></i></a></td></tr>").appendTo(contenido);
		var contenidoTotales = $('.tabla_endoso_totales tbody');
		contenidoTotales.html('');
		$('<tr><td>'+''+'</td><td>'+formatInt($("#varCantidadFletes").val())+'</td><td>'+formatCurrency($("#varSumaAseguradaUnitaria").val())+'</td><td>'+formatCurrency($("#varSumaAseguradaTotal").val())+'</td><td>'+formatCurrency($("#varTotalTarifa").val())+'</td><td>'+formatCurrency($("#varImporteCuota").val())+'</td></tr>').appendTo(contenidoTotales);
		limpiarFormulario();
		validarControles();
	}
}

function formatInt(x) { // Función que nos permite formatear una cantidad entera con comas.
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var actualizarTablaDeclaracionUnidad = function(rowActualizar){ // Función que nos permite actualizar la fila seleccionada
	
	if (pasarComprobacionesActualizarTabla())
	{
		var rowData = rowActualizar.closest("tr");
		
		if ($("#txtRomaneaje").val() != "")
		{
			rowData.children('td')[1].innerText = formatInt($("#txtRomaneaje").val());
		}
		
		if ($("#txtOrigen").val() != "")
		{
			rowData.children('td')[6].innerText = $("#txtOrigen").val().toUpperCase();
		}
		
		if ($("#txtDestino").val() != "")
		{
			rowData.children('td')[7].innerText = $("#txtDestino").val().toUpperCase();
		}
		
		if ($("#txtCantidad").val() != "")
		{
			rowData.children('td')[3].innerText = formatInt($("#txtCantidad").val());			
		}
		
		if ($("#txtSumaAseguradaUnitaria").val() != "")
		{
			rowData.children('td')[4].innerText = formatCurrency($("#txtSumaAseguradaUnitaria").val());
		}
		
		$("#txtRomaneaje").val("");
		$("#txtOrigen").val("");
		$("#txtDestino").val("");
		$("#txtCantidad").val("");
		$("#txtSumaAseguradaUnitaria").val("");
		$("#txtSumaAseguradaTotal").val("");
		
		recalcularTablaDeclaracionUnidad();
	}
}

var pasarComprobacionesActualizarTabla = function(){ // Función que nos permite pasar las comprobaciones al actualizar la tabla de unidades por dia.
	
	if ($("#txtRomaneaje").val() == "" && $("#txtOrigen").val() == "" && $("#txtDestino").val() == "" && $("#txtCantidad").val() == "")
	{
		alertify.alert("Se requiere ingresar datos para actualizar.");
		return false;
	}
	
	return true;
}

var recalcularTablaDeclaracionUnidad = function(){ // Función que nos permite recalcular los montos cuando se actualizo un valor en algun row de la tabla.
	
	$("#varSumaAseguradaUnitaria").val(0);
	$("#varSumaAseguradaTotal").val(0);
	$("#varImporteCuota").val(0);
	
	$('.tabla_declaracion_transporte tbody').children('tr').each(function(indice){
		
		var total = parseFloat(replaceAll($(this).closest("tr").find("td").eq(3).html(),',','')) * parseFloat(replaceAll($(this).closest("tr").find("td").eq(4).html(),',',''));
		$(this).closest("tr").find("td").eq(5).text(formatCurrency(total));
		
		$("#varSumaAseguradaUnitaria").val(parseFloat($("#varSumaAseguradaUnitaria").val()) + parseFloat(replaceAll($(this).closest("tr").find("td").eq(4).html(),',','')) / parseInt($("#varCantidadFletes").val()));
		$("#varSumaAseguradaTotal").val(parseFloat($("#varSumaAseguradaTotal").val()) + parseFloat(replaceAll($(this).closest("tr").find("td").eq(5).html(),',','')));
		$("#varImporteCuota").val(parseFloat($("#varSumaAseguradaTotal").val()) * parseFloat($("#varTotalTarifa").val()));
	});
	
	var contenidoTotales = $('.tabla_endoso_totales tbody');
	contenidoTotales.html('');
	$('<tr><td>'+''+'</td><td>'+formatInt($("#varCantidadFletes").val())+'</td><td>'+formatCurrency($("#varSumaAseguradaUnitaria").val())+'</td><td>'+formatCurrency($("#varSumaAseguradaTotal").val())+'</td><td>'+formatCurrency($("#varTotalTarifa").val())+'</td><td>'+formatCurrency($("#varImporteCuota").val())+'</td></tr>').appendTo(contenidoTotales);	
}

var eliminarFilaUnidadPorDia = function(filaAEliminar){ // Función que nos permite eliminar el row seleccionado.
	alertify.confirm("Esto eliminará la fila seleccionada, ¿Desea continuar?", function (e) {
	    if (e) {
	    	
			var sumaUnitaria = parseFloat(replaceAll(filaAEliminar.closest("tr").find("td").eq(4).html(),',',''));
			var sumaUnitariaTotal = parseFloat(replaceAll(filaAEliminar.closest("tr").find("td").eq(5).html(),',',''));
			
			filaAEliminar.closest("tr").remove();
			var varCantidadFletesAnterior = parseInt($("#varCantidadFletes").val())
			var varCantidadFletes = varCantidadFletesAnterior - 1; 
			
			$('.tabla_endoso_totales tbody').children('tr').each(function(indice){
				
				$("#varCantidadFletes").val(varCantidadFletes)
				
				var varSumaAseguradaUnitaria = 0;
				
				if (varCantidadFletes >= 1)
				{
					var varSumaAseguradaUnitaria = ((parseFloat(replaceAll($(this).closest("tr").find("td").eq(2).html(),',','')) * varCantidadFletesAnterior) -  sumaUnitaria) / varCantidadFletes;
				}
				else
				{
					$(this).closest("tr").find("td").eq(4).text(formatCurrency(0));
					$(this).closest("tr").find("td").eq(5).text(formatCurrency(0));
				}
				
				var varSumaAseguradaTotal = (parseFloat(replaceAll($(this).closest("tr").find("td").eq(3).html(),',','')) - sumaUnitariaTotal);
				
				$(this).closest("tr").find("td").eq(1).text(formatInt(varCantidadFletes));
				$(this).closest("tr").find("td").eq(2).text(formatCurrency(varSumaAseguradaUnitaria));
				$(this).closest("tr").find("td").eq(3).text(formatCurrency(varSumaAseguradaTotal));
				
				return false;
			});
	    }
	});	
	return false;	
}

function asignarValores(){ // Función que permite asignar valores a las variables del formulario si estas se encuentran null. 

	if ($("#varCantidadFletes").val() == "")
	{
		$("#varCantidadFletes").val(0);
	}
	
	if ($("#varSumaAseguradaUnitaria").val() == "")
	{
		$("#varSumaAseguradaUnitaria").val(0);
	}
	
	if ($("#varSumaAseguradaTotal").val() == "")
	{
		$("#varSumaAseguradaTotal").val(0);
	}
	
	if ($("#varCuota").val() == "")
	{
		$("#varCuota").val(0);
	}
	
	if ($("#varImporteCuota").val() == "")
	{
		$("#varImporteCuota").val(0);
	}
}

function limpiarFormulario() // Función que limpia los texts del formulario al agregar un row a la tabla.
{
	$("#txtRomaneaje").val('');
	$("#txtCantidad").val('');
	$("#txtSumaAseguradaUnitaria").val('');
	$("#txtSumaAseguradaTotal").val('');
	$("#txtOrigen").val('');
	$("#txtDestino").val('');
}

function validarControles(){ // Función que valida los controles del formulario cuando se agrega un nuevo row a la tabla.
	$('#dtpPeriodoInicio').attr('disabled',true);
	$('#dtpPeriodoFin').attr('disabled',true);
}

function pasarComprobacionesAgregarElemento() // Función que permite verificar si la información ingresada en el formulario es la correcta.
{
	if ($("#dtpVigenciaInicio").val() == "")
	{
		alertify.alert("Se requiere ingresar la vigencia de inicio para continuar");
		return false;
	}
	
	if ($("#dtpVigenciaFin").val() == "")
	{
		alertify.alert("Se requiere ingresar la vigencia de fin para continuar");
		return false;
	}
	
	if ($("#dtpFecha").val() == "")
	{	
		alertify.alert("Se requiere ingresar la fecha para continuar");
		return false;
	}
	
	if ($("#txtRomaneaje").val() == "")
	{
		alertify.alert("Se requiere ingresar el romaneaje para continuar");
		return false;
	}
		
	if ($("#txtOrigen").val() == "")
	{
		alertify.alert("Se requiere ingresar el origen para continuar");
		return false;
	}
	
	if ($("#txtDestino").val() == "")
	{
		alertify.alert("Se requiere ingresar el destino para continuar");
		return false;
	}
	
	if ($("#txtCantidad").val() == "")
	{
		alertify.alert("Se requiere ingresar la cantidad para continuar");
		return false;
	}
	
	if ($("#txtSumaAseguradaUnitaria").val() == "")
	{
		alertify.alert("Se requiere ingresar la suma asegurada unitaria para continuar");
		return false;
	}
	
	if ($("#txtSumaAseguradaTotal").val() == "")
	{
		alertify.alert("Se requiere ingresar la suma asegurada total para continuar");
		return false;
	}
	
	if ($("#txtSumaAseguradaTotal").val() == "")
	{
		alertify.alert("Se requiere ingresar el destino para continuar");
		return false;
	}
	
	if ($("#txtDescripcionBienAsegurado").val() == "")
	{
		alertify.alert("Se requiere ingresar la descripción de bien asegurado para continuar");
		return false;
	}
	
	if ($("#varUltimaFechaIngresada").val() > $("#dtpFecha").val())
	{
		alertify.alert("La fecha ingresada es menor a las fechas ingresadas en la declaración");
		return false;
	}
	
	if ($("#dtpFecha").datepicker('getDate') > $("#dtpPeriodoFin").datepicker( 'getDate' ))
	{
		alertify.alert("La fecha ingresada es mayor al periodo de declaración");
		return false;
	}	
	
	if ($("#dtpFecha").datepicker('getDate') < $("#dtpPeriodoInicio").datepicker( 'getDate' ))
	{
		alertify.alert("La fecha ingresada es menor al periodo de declaración");
		return false;
	}
	
	return true;
}

function fechaUltimaMes(){ // Función que obtiene la ultima dia del mes.
	var currentTime = new Date();
	var day = ("0" + currentTime.getDate()).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	var ultimoDia = daysInMonth(month, year)
	
	return (ultimoDia+'/'+month+'/'+year);
}

function fechaPrimeraMes(){ // Función que genera y devuelve la fecha de hoy.
	var currentTime = new Date();
	var day = ("0" + 1).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return (day+'/'+month+'/'+year);
}

function buscarConstanciasParaElDeclaracionEndoso(){ // Función que busca la lista de constancias.
	Dajaxice.Endoso.obtener_constancias_transporte(cargarModalConstancias,{'datosABuscar':$("#txtBuscarConstancia").val()});	
	return false;
}

function cargarModalConstancias(data){ // Obtiene la información de la busqueda de las constancias.
	var contenido = $('.tbl_buscar_constancia tbody');
	contenido.html('');
	
	if(data.constancias && data.constancias.length > 0)
	{
		constancias = data.constancias;
		for(rowArreglo=0;rowArreglo<constancias.length;rowArreglo++)
		{
			if (constancias[rowArreglo][2] == 1)
			{
				moneda = "PESOS";
			}
			else
			{
				moneda = "DOLARES";
			}
			
			$('<tr><td>'+constancias[rowArreglo][5]+'</td><td>'+constancias[rowArreglo][1]+"</td><td>"+moneda+"</td><td>"+constancias[rowArreglo][3]+'</td><td style="display: none;">'+constancias[rowArreglo][0]+'</td><td style="display: none;">'+constancias[rowArreglo][4]+'</td><td style="display: none;">'+constancias[rowArreglo][6]+'</td><td style="display: none;">'+constancias[rowArreglo][7]+'</td><td style="display: none;">'+constancias[rowArreglo][11]+'</td><td style="display: none;">'+constancias[rowArreglo][12]+'</td><td style="display: none;">'+constancias[rowArreglo][13]+'</td><td style="display: none;">'+constancias[rowArreglo][14]+'</td><td>'+constancias[rowArreglo][8]+'</td><td>'+constancias[rowArreglo][9]+'</td><td style="display: none;">'+''+'</td><td style="display: none;">'+''+'</td></tr>').appendTo(contenido);
		}
	}
	else
	{
		alertify.alert("No se encontro constancia.");
	}
}

function tabla_buscar_constancia(){ // Función que permite interactuar con la ventana modal de buscar constancias.
	$(".modal").on('shown', function() {mensajeDeclaracionTransporte
	    $("#txtBuscarConstancia").focus();
	});
	
	$('.tbl_buscar_constancia tbody').on('mouseover', 'tr', function(event) { //toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tbl_buscar_constancia tbody').on('mouseout', 'tr', function(event) { //evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	

	$('.tbl_buscar_constancia tbody').on('click', 'tr', function(event) { //evento click que selecciona el row y marca el check de la tabla		
		$("#txtNumeroSolicitud").val($(this).children('td')[1].innerText);
		$("#txtMoneda").val($(this).children('td')[2].innerText);
		$("#txtEjercicio").val($(this).children('td')[3].innerText);
		$("#varIdConstancia").val($(this).children('td')[5].innerText);
		$("#txtFolioConstancia").val($(this).children('td')[0].innerText);
		$("#varTotalTarifa").val($(this).children('td')[6].innerText);
		$("#varPrima").val($(this).children('td')[7].innerText);
		$("#txtNombre").val($(this).children('td')[8].innerText);
		$("#txtRfc").val($(this).children('td')[9].innerText);
		$("#txtDomicilio").val($(this).children('td')[10].innerText);
		$("#txtTelefono").val($(this).children('td')[11].innerText);
		$("#txtVigenciaInicio").val($(this).children('td')[12].innerText);
		$("#txtVigenciaFin").val($(this).children('td')[13].innerText);	
		$("#varTotalTarifa").val($(this).children('td')[6].innerText);
		$("#varPrima").val($(this).children('td')[7].innerText);
		$(".close").click();
	});
}

function daysInMonth(humanMonth, year) { // Función que regresa el número de dias del mes.
	  return new Date(year || new Date().getFullYear(), humanMonth, 0).getDate();
}