$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario endoso.​
	activarMenu();
	
	$("#btnBuscarConstancia").on("click", buscarConstanciasParaElEndoso);
	$("#btnAgregar").on("click", calcularEndoso);  
	$("#btnBuscarConstanciaModal").on("click", limpiarBuscadorConstancia);
	$("#btnLimpiarTabla").on("click", limpiarTablaEndoso);
	$("#btnGuardarDeclaracion").on("click", guardarDeclaracionEndoso); 
	$("#btnListadoDeclaracion").on("click", regresarListadoDeclaracionesEndoso);	
	$("#btnCancelarDeclaracion").on("click", limpiar_formulario_endoso);
	$("#btnQuitar").on("click", quitarUltimoRowTablaDeclaracionDia);
	
    document.getElementById("txtRfc").readOnly = true;
	document.getElementById("txtNombre").readOnly = true;
	document.getElementById("txtDomicilio").readOnly = true;
	document.getElementById("txtTelefono").readOnly = true;
	document.getElementById("txtFolioConstancia").readOnly = true;
	document.getElementById("txtNumeroSolicitud").readOnly = true;
	document.getElementById("txtMoneda").readOnly = true;
	document.getElementById("txtEjercicio").readOnly = true;
    
	tabla_buscar_constancia();
	
	$("#dtpPeriodoInicio").datepicker({
		firstDay: 1
	});
	
	$("#dtpPeriodoFin").datepicker({
		firstDay: 1
	});
	
	if ($("#varIdEndoso").val() != '' || $("#varIdConstancia").val() != '')
	{
		validarControles();
		habilitarBotonVistaPrevia();
	}
	else
	{
		$("#dtpPeriodoInicio").val(fechaPrimeraMes());		
		$("#dtpPeriodoFin").val(fechaUltimaMes());
	}
}

var quitarUltimoRowTablaDeclaracionDia = function(){ // Función que nos permite quitar el ultimo renglon de la tabla de declaración por dia.
	
	if ($('.tabla_endoso tr').length > 1)
	{		
		var varExistenciaUltimaFila = parseFloat(replaceAll($('.tabla_endoso tr:last td:gt(3)').html(),',',''));
		var varPrecioUltimaFila = parseFloat(replaceAll($('.tabla_endoso tr:last td:gt(4)').html(),',',''));
		var varValorUltimaFila = parseFloat(replaceAll($('.tabla_endoso tr:last td:gt(5)').html(),',',''));
		var varTarifaMensualUltimaFila = parseFloat(replaceAll($('.tabla_endoso tr:last td:gt(6)').html(),',',''));
		var varTarifaDiariaUltimaFila = parseFloat(replaceAll($('.tabla_endoso tr:last td:gt(7)').html(),',',''));
		var varCuotaUltimaFila = parseFloat(replaceAll($('.tabla_endoso tr:last td:gt(8)').html(),',',''));
		var diasUltimos = parseInt($("#varTotalDias").val()) - 1;
		
		$('.tabla_endoso tr:last').remove();
		
		$('.tabla_endoso_totales tbody').children('tr').each(function(indice){
			
			var varSumaPromedioDiario = (parseFloat(replaceAll($(this).closest("tr").find("td").eq(1).html(),',','')) * parseInt($("#varTotalDias").val())) - varExistenciaUltimaFila;
 			$("#varSumaPromedioDiario").val(varSumaPromedioDiario);
			var promedioDiario = varSumaPromedioDiario / diasUltimos;
						
			var varPrecio = (parseFloat(replaceAll($(this).closest("tr").find("td").eq(2).html(),',','')) * parseInt($("#varTotalDias").val())) - varPrecioUltimaFila;
			$("#varSumaPrecio").val(varPrecio);
			var promedioPrecio = varPrecio / diasUltimos;
			
			var varSumaValorExistencia = (parseFloat(replaceAll($(this).closest("tr").find("td").eq(3).html(),',','')) * parseInt($("#varTotalDias").val())) - varValorUltimaFila;
			$("#varSumaValorExistencia").val(varSumaValorExistencia);
			var promedioValorExperiencia = varSumaValorExistencia / diasUltimos;
			
			var varSumaCuotaMensual = (parseFloat(replaceAll($(this).closest("tr").find("td").eq(4).html(),',','')) * parseInt($("#varTotalDias").val())) - varTarifaMensualUltimaFila;
			$("#varSumaCuotaMensual").val(varSumaCuotaMensual);
			var promedioCuotaMensual = varSumaCuotaMensual / diasUltimos;
			
			var varSumaCuotaPeriodo1 = parseFloat(replaceAll($(this).closest("tr").find("td").eq(5).html(),',','')) - varTarifaDiariaUltimaFila;
			$("#varSumaCuotaPeriodo1").val(varSumaCuotaPeriodo1);
			
			var varSumaCuotaPeriodo2 = parseFloat(replaceAll($(this).closest("tr").find("td").eq(6).html(),',','')) - varCuotaUltimaFila;
			$("#varSumaCuotaPeriodo2").val(varSumaCuotaPeriodo2);
			
	    	$(this).closest("tr").find("td").eq(1).text(formatCurrency(promedioDiario));
	    	$(this).closest("tr").find("td").eq(2).text(formatCurrency(promedioPrecio));
	    	$(this).closest("tr").find("td").eq(3).text(formatCurrency(promedioValorExperiencia));
	    	$(this).closest("tr").find("td").eq(4).text(formatCurrency(promedioCuotaMensual));
	    	$(this).closest("tr").find("td").eq(5).text(formatCurrency(varSumaCuotaPeriodo1));
	    	$(this).closest("tr").find("td").eq(6).text(formatCurrency(varSumaCuotaPeriodo2));
		});
		
		$("#varUltimoDiaIngresado").val(diasUltimos);
		$("#varTotalDias").val(diasUltimos);
	}
	else
	{
		alertify.alert("No se encuentran dias capturados.");
	}
}

var pasarComprobacionesActualizarTabla = function(){ // Función que nos permite validar los datos ingresados para actualizar la descripcion por dia.
	
	if ($("#txtEntrada").val() == "" && $("#txtSalida").val() == "" && $("#txtPrecio").val() == "")
	{
		alertify.alert('Se requiere ingresar salida, entrada o precio para continuar.');
		
		return false;
	}
	
	return true;
}

var actualizarTablaDeclaracionDia = function(rowSeleccionado){ // Función que nos permite actualizar los valores de la tabla declaración de endoso por dia.
	
	if (pasarComprobacionesActualizarTabla())
	{
		var rowData = rowSeleccionado.closest("tr");
		
		if ($("#txtEntrada").val() != "")
		{
			rowData.children('td')[2].innerText = formatCurrency($("#txtEntrada").val());
		}
		
		if ($("#txtSalida").val() != "")
		{
			rowData.children('td')[3].innerText = formatCurrency($("#txtSalida").val());
		}
		
		if ($("#txtPrecio").val() != "")
		{
			rowData.children('td')[5].innerText = formatCurrency($("#txtPrecio").val());
		}
		
		$("#txtEntrada").val("");
		$("#txtSalida").val("");
		$("#txtPrecio").val("");
		
		recalcularTablaDeclaracionDia();
	}
}

var recalcularTablaDeclaracionDia = function(){ // Función que nos permite recalcular los datos de la declaración cuando algun row de la tabla es modificado.
	
	var arrayDeclaracionTransporte = [];
	$("#varTotalExistencia").val(parseFloat($("#txtExistenciaInicial").val()));	
	var primaCotizador = 100;
	
	if ($("#varPrima").val() == 1)
	{
		primaCotizador = 1000;
		$("#varSumaPromedioDiario").val(0);
		$("#varSumaPrecio").val(0);
		$("#varSumaValorExistencia").val(0);
		$("#varSumaCuotaMensual").val(0);
		$("#varSumaCuotaPeriodo1").val(0);
		$("#varSumaCuotaPeriodo2").val(0);
	}
	
	$('.tabla_endoso tbody').children('tr').each(function(indice){

		var entrada = parseFloat(replaceAll($(this).closest("tr").find("td").eq(2).html(),',',''));
    	var salida = parseFloat(replaceAll($(this).closest("tr").find("td").eq(3).html(),',',''));
    	var precio = parseFloat(replaceAll($(this).closest("tr").find("td").eq(5).html(),',',''));
    	var tarifaMensual = parseFloat(replaceAll($(this).closest("tr").find("td").eq(7).html(),',',''));
    	var totalExistencia = (parseFloat($("#varTotalExistencia").val()) + entrada) - salida;
    	$("#varTotalExistencia").val(totalExistencia);
    	var valor =  parseFloat($("#varTotalExistencia").val()) * precio;
    	var tarifaDiaria = tarifaMensual / 30;
    	var cuota = (valor * tarifaDiaria) / primaCotizador;
    	$("#varSumaPrecio").val(parseFloat($("#varSumaPrecio").val()) + precio);
        $("#varSumaPromedioDiario").val(parseFloat($("#varSumaPromedioDiario").val()) + totalExistencia);
		$("#varSumaValorExistencia").val(parseFloat($("#varSumaValorExistencia").val()) + valor);
		$("#varSumaCuotaMensual").val(parseFloat($("#varSumaCuotaMensual").val()) + tarifaMensual);
		$("#varSumaCuotaPeriodo1").val(parseFloat($("#varSumaCuotaPeriodo1").val()) + tarifaDiaria);
		$("#varSumaCuotaPeriodo2").val(parseFloat($("#varSumaCuotaPeriodo2").val()) + cuota);
    	
    	$(this).closest("tr").find("td").eq(4).text(formatCurrency(totalExistencia));
    	$(this).closest("tr").find("td").eq(6).text(formatCurrency(valor));
    	$(this).closest("tr").find("td").eq(8).text(formatCurrency(tarifaDiaria));
    	$(this).closest("tr").find("td").eq(9).text(formatCurrency(cuota));
	});
	
	$('.tabla_endoso_totales tbody').children('tr').each(function(indice){
		
		var varSumaPromedioDiario = parseFloat($("#varSumaPromedioDiario").val()) / parseInt($("#varUltimoDiaIngresado").val())
		$("#varSumaPromedioDiario").val(varSumaPromedioDiario);
		var varPrecio = parseFloat($("#varSumaPrecio").val());
		var varSumaValorExistencia = parseFloat($("#varSumaValorExistencia").val());
		var varSumaCuotaMensual = parseFloat($("#varSumaCuotaMensual").val()) / parseInt($("#varUltimoDiaIngresado").val());
		var varSumaCuotaPeriodo1 = parseFloat($("#varSumaCuotaPeriodo1").val());
		var varSumaCuotaPeriodo2 = parseFloat($("#varSumaCuotaPeriodo2").val());
		
    	$(this).closest("tr").find("td").eq(1).text(formatCurrency(varSumaPromedioDiario));
    	$(this).closest("tr").find("td").eq(2).text(formatCurrency(varPrecio));
    	$(this).closest("tr").find("td").eq(3).text(formatCurrency(varSumaValorExistencia));
    	$(this).closest("tr").find("td").eq(4).text(formatCurrency(varSumaCuotaMensual));
    	$(this).closest("tr").find("td").eq(5).text(formatCurrency(varSumaCuotaPeriodo1));
    	$(this).closest("tr").find("td").eq(6).text(formatCurrency(varSumaCuotaPeriodo2));
	});
}

function habilitarBotonVistaPrevia(){ // Función que nos permite habilitar el boton de vista previa.
	$("#btnVistaPreviaDeclaracion").on("click", declaracionEndosoImpresion);
	$("#btnVistaPreviaDeclaracion").removeAttr("disabled");
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

function declaracionEndosoImpresion(){ // Función que permite imprimir el endoso de la declaración.
	window.open('/DeclaracionEndosoImpresion/' + $("#varIdEndoso").val());
}

function regresarListadoDeclaracionesEndoso(){ // Función que permite regresar al listado de las declaraciones de los endosos.
	location.href = '/ListadoDeclaracionEndoso/';
}

function limpiarBuscadorConstancia(){ // Función que cierra el formulario modal buscadorConstancia.
	$("#txtBuscarConstancia").val('');
	var contenido = $('.tbl_buscar_constancia tbody');
	contenido.html('');
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

function guardarDeclaracionEndoso(){ // Función que envia el formulario para guardarlo en la base de datos.
	
	if (pasarComprobacionesEndoso())
	{
		fechaPeriodoInicio = $("#dtpPeriodoInicio").val();
		fechaPeriodoFin = $("#dtpPeriodoFin").val();
		
		if ($("#varIdEndoso").val() == '')
		{
			Dajaxice.Endoso.guardar_declaracion_endoso(Dajax.process,{'formulario':$('#formulario_endoso').serialize(true), 'endosoPorDia':validarArrayVacio(obtencionDatosTablaDeclaracionEndoso()),'fechaPeriodoInicio':fechaPeriodoInicio, 'fechaPeriodoFin':fechaPeriodoFin});
			deshabilitarBotonLimpiar();
		}
		else
		{
			alertify.confirm("¿Desea modificar la declaración de endoso?", function (e)
			{
			    if (e)
			    {
			    	Dajaxice.Endoso.guardar_declaracion_endoso(Dajax.process,{'formulario':$('#formulario_endoso').serialize(true), 'endosoPorDia':validarArrayVacio(obtencionDatosTablaDeclaracionEndoso()),'fechaPeriodoInicio':fechaPeriodoInicio, 'fechaPeriodoFin':fechaPeriodoFin});
			    	deshabilitarBotonLimpiar();
			    	alertify.success("Declaración Modificada");
			    	window.setTimeout('obtener_declaracionesendosopordia()', 1000)
			    }
			});
		}
	}
	
	return false;
}

function obtener_declaracionesendosopordia() // Función que permite actualizar los valores de la declaración de endoso por día.
{
	Dajaxice.Endoso.obtener_declaracionendoso_por_dia(cargarDeclaracionEndosoPorDia,{'idDeclaracionEndoso':$("#varIdEndoso").val()});
	return false;
}

function cargarDeclaracionEndosoPorDia(data) // Función que permite cargar las declaraciones de endoso por dia en la tabla
{
	var contenido = $('.tabla_endoso tbody');
	contenido.html('');
	
	if(data.declaracionesEndosoPorDia)
	{
		$.each(data.declaracionesEndosoPorDia, function(i,declaracion)
		{
			$('<tr><td style="display: none;">'+declaracion.IdDeclaracionEndosoPorDia+'</td><td>'+declaracion.Dia+'</td><td>'+formatCurrency(declaracion.Entrada)+'</td><td>'+formatCurrency(declaracion.Salida)+'</td><td>'+formatCurrency(declaracion.Precio)+'</td><td>'+formatCurrency(declaracion.Existencia)+'</td><td>'+formatCurrency(declaracion.Valor)+'</td><td>'+formatCurrency(declaracion.TarifaMensual)+'</td><td>'+formatCurrency(declaracion.TarifaDiaria)+'</td><td>'+formatCurrency(declaracion.Cuota)+'</td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

var formatCurrency = function(total) // Función que nos permite darle formato a una cantidad.
{
    var neg = false;
    
    if(total < 0) 
    {
        neg = true;
        total = Math.abs(total);
    }
    return parseFloat(total, 10).toFixed(4).replace(/(\d)(?=(\d{3})+\.)/g, "$1,").toString();
}

function deshabilitarBotonLimpiar() // Función que nos permite habilitar el boton de vista previa.
{
	var diasDif = $("#dtpPeriodoFin").datepicker( 'getDate' ).getTime() - $("#dtpPeriodoInicio").datepicker( 'getDate' ).getTime();
	var dias = Math.round(diasDif/(1000 * 60 * 60 * 24)) + 1;
	
	if (($(".tabla_endoso  tr").length -1) == dias)
	{
		$("#btnLimpiarTabla").unbind("click");
		$("#btnLimpiarTabla").attr("disabled","disabled");
	}
}

function recargarDatosActualizados(){ // Función que permite recargar los datos actualizados de la declaración de endoso cuando es guardado por primera vez.	
	location.href = '/DeclaracionEndoso/' + $("#varIdEndoso").val();
}

function limpiar_formulario_endoso(){ // Función que limpia todo el formulario y las variables para permitir ingresar una nueva declaración.
	if ($("#varIdEndoso").val() == '')
	{
		document.getElementById("formulario_endoso").reset();
		var contenido = $('.tabla_endoso tbody');
		contenido.html('');
		var contenido1 = $('.tabla_endoso_totales tbody');
		contenido1.html('');
		$("#varIdConstancia").val('');
		$("#varIdPersona").val('');
		$("#varTotalTarifa").val('');
		$("#varPrima").val('');
		$("#varTotalExistencia").val('');
		$("#varUltimoDiaIngresado").val('');
		$("#varSumaPromedioDiario").val('');
		$("#varSumaPrecio").val('');
		$("#varSumaValorExistencia").val('');
		$("#varSumaCuotaMensual").val('');
		$("#varSumaCuotaPeriodo1").val('');
		$("#varSumaCuotaPeriodo2").val('');
		$("#varTotalDias").val('');
		
		$("#dtpPeriodoInicio").val(fechaPrimeraMes());
		
		$("#dtpPeriodoInicio").datepicker({
			firstDay: 1
		});
		
		$("#dtpPeriodoFin").val(fechaUltimaMes());
		
		$("#dtpPeriodoFin").datepicker({
			firstDay: 1
		});
		tabla_buscar_constancia
		$('#dtpPeriodoInicio').attr('disabled',false);
		$('#dtpPeriodoFin').attr('disabled',false);
		document.getElementById("txtExistenciaInicial").readOnly = false;
	}
	else
	{
		regresarListadoDeclaracionesEndoso();
	}
}

function mensajeDeclaracionEndoso(folioEndoso){ //Función que recibe el número de folio del endoso de la función Dajaxice.Endoso.guardar_endoso para mostrarla en un alert.
	$("#varIdEndoso").val(folioEndoso);	
	habilitarBotonVistaPrevia();
	obtener_declaracionesendosopordia();
	alertify.alert('Declaración de Endoso Guardado con el Folio: ' + folioEndoso);
}

function obtencionDatosTablaDeclaracionEndoso(){ // Función que obtiene la información de la tabla tabla_endoso y la agrega a un arreglo.
	var arrayDeclaracionTransporte = [];
	
	$('.tabla_endoso tr').each(function(){
		var fila = $(this).find('td');
	    if (fila.length > 0)
	    {
			var arrayFilas = [];
			arrayFilas.push($(this).closest("tr").find("td").eq(0).html());
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(1).html(),',','')); 			
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(2).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(3).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(4).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(5).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(6).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(7).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(8).html(),',',''));
			arrayFilas.push(replaceAll($(this).closest("tr").find("td").eq(9).html(),',',''));
			
			arrayDeclaracionTransporte.push(arrayFilas);
	    }
	});
	
	return arrayDeclaracionTransporte;
}

var replaceAll = function(text, busca, reemplaza) // Función que nos permite remplazar los caracteres de un string.
{
	while (text.toString().indexOf(busca) != -1)	
	text = text.toString().replace(busca,reemplaza);
	
	return text;	
}

function pasarComprobacionesEndoso() // Función que nos permite verificiar si los datos ingresados en el formulario son los correctos.
{
	if ($("#varIdConstancia").val() == 0 || $("#varIdConstancia").val() == '')
	{
		alertify.alert("Se requiere seleccionar constancia para continuar.");
		return false;
	}
	
	if ($("#txtExistenciaInicial").val() == '' || $("#txtExistenciaInicial").val() == 0)
	{
		alertify.alert("Se requiere ingresar la existencia inicial para continuar.");
		return false;
	}

	return true;
}

function limpiarTablaEndoso(){ // Función que permite quitar los rows de la talbla de los endosos.
	
	alertify.confirm("Esto eliminará la información, ¿Desea continuar?", function (e)
	{
	    if (e)
	    {
	    	var contenido = $('.tabla_endoso tbody');
	    	contenido.html('');
	    	var contenido1 = $('.tabla_endoso_totales tbody');
	    	contenido1.html('');
	    	$("#varTotalExistencia").val(0);
	    	$("#varUltimoDiaIngresado").val(0);
	    	$("#varSumaPromedioDiario").val(0);
	    	$("#varSumaPrecio").val(0);
	    	$("#varSumaValorExistencia").val(0);
	    	$("#varSumaCuotaMensual").val(0);
	    	$("#varSumaCuotaPeriodo1").val(0);
	    	$("#varSumaCuotaPeriodo2").val(0);
	    	$("#varTotalDias").val(0);	
	    	$('#dtpPeriodoInicio').attr('disabled',false);
	    	$('#dtpPeriodoFin').attr('disabled',false);
	    	document.getElementById("txtExistenciaInicial").readOnly = false;
	    	
	    	$("#dtpPeriodoInicio").datepicker({
	    		firstDay: 1
	    	});
	    	
	    	$("#dtpPeriodoFin").datepicker({
	    		firstDay: 1
	    	});	
	    	
	    	$("#txtEntrada").val("");
	    	$("#txtSalida").val("");
	    	$("#txtPrecio").val("");
	    }
	});
}

function buscarConstanciasParaElEndoso(){ // Función que busca la lista de constancias.
	Dajaxice.Endoso.obtener_constancias(cargarModalConstancias,{'datosABuscar':$("#txtBuscarConstancia").val()});	
	return false;
};

function cargarModalConstancias(data){ // Obtiene la información de la busqueda de la persona que recibe del método buscar_persona de ajax.py, los datos de la busqueda se agregan a la tabla busquedaPersona de la ventana modal.
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
			
			$('<tr><td>'+constancias[rowArreglo][5]+'</td><td>'+constancias[rowArreglo][1]+"</td><td>"+moneda+"</td><td>"+constancias[rowArreglo][3]+'</td><td style="display: none;">'+constancias[rowArreglo][0]+'</td><td style="display: none;">'+constancias[rowArreglo][4]+'</td><td style="display: none;">'+constancias[rowArreglo][6]+'</td><td style="display: none;">'+constancias[rowArreglo][7]+'</td><td style="display: none;">'+constancias[rowArreglo][11]+'</td><td style="display: none;">'+constancias[rowArreglo][12]+'</td><td style="display: none;">'+constancias[rowArreglo][13]+'</td><td style="display: none;">'+constancias[rowArreglo][14]+'</td><td>'+constancias[rowArreglo][8]+'</td><td>'+constancias[rowArreglo][9]+'</td></tr>').appendTo(contenido);
		}
	}
	else
	{
		alertify.alert("No se encontro constancia.");
	}
}

function tabla_buscar_constancia(){ // Función que permite interactuar con la ventana modal de buscar constancias.
	$(".modal").on('shown', function() {
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
		$("#txtVigenciaFin").val($(this).children('td')[11].innerText);			
		$(".close").click();
	});
}

function calcularEndoso(){ // Función que calcula los endosos.
	
	if (pasarComprobacionesCalcularEndoso())
	{
		if ($("#varTotalExistencia").val() == 0 || $("#varTotalExistencia").val() == '')
		{
			$("#varTotalExistencia").val(parseFloat($("#txtExistenciaInicial").val()));			
			$("#varUltimoDiaIngresado").val(0);
			$("#varSumaPromedioDiario").val(0);
			$("#varSumaPrecio").val(0);
			$("#varSumaValorExistencia").val(0);
			$("#varSumaCuotaMensual").val(0);
			$("#varSumaCuotaPeriodo1").val(0);
			$("#varSumaCuotaPeriodo2").val(0);
			$("#varTotalDias").val(0);
		}
		
		agregarATablaEndoso();
		validarControles();
	}
}

function pasarComprobacionesCalcularEndoso(){ // Función que permite pasar las comprobaciones para verificar que se puede calcular.
	
	var fechaFinal = new Date($("#dtpPeriodoFin").datepicker('getDate'));
	var ultimoDiaPeriodo = fechaFinal.getDate();
	
	if ($("#varUltimoDiaIngresado").val() == ultimoDiaPeriodo)
	{
		alertify.alert("Se ingresaron todos los dias correspondientes al período");
		$("#txtEntrada").val("");
		$("#txtSalida").val("");
		$("#txtPrecio").val("");
		return false;
	}
	
	if ($("#varIdConstancia").val() == "")
	{
		alertify.alert("Se requiere seleccionar una constancia para continuar");
		return false;
	}
	
	if ($("#txtExistenciaInicial").val() == "")
	{
		alertify.alert("Se requiere ingresar la existencia inicial para continuar");
		return false;
	}
	
	if ($("#txtEntrada").val() == "")
	{
		alertify.alert("Se requiere ingresar la entrada para continuar");
		return false;
	}
	
	if ($("#txtSalida").val() == "")
	{
		alertify.alert("Se requiere ingresar la salida para continuar");
		return false;
	}
	
	if ($("#txtPrecio").val() == "")
	{
		alertify.alert("Se requiere ingresar precio para continuar");
		return false;
	}
	 
	return true;
}

function validarControles(){ // Función que valida los controles del formulario cuando se agrega un nuevo row a la tabla.
	document.getElementById("txtExistenciaInicial").readOnly = true;
	$('#dtpPeriodoInicio').attr('disabled',true);
	$('#dtpPeriodoFin').attr('disabled',true);
	$("#txtEntrada").val("");
	$("#txtSalida").val("");
	$("#txtPrecio").val("");
}

function agregarATablaEndoso(){ // Función que permite agregar endosos a la tabla.
	
	var salida = 0;
	
	var dia = parseInt($("#varUltimoDiaIngresado").val());
	
	$("#varTotalDias").val(parseInt($("#varTotalDias").val()) + 1);
	
	if ($("#varUltimoDiaIngresado").val() == 0 || $("#varUltimoDiaIngresado").val() == '')
	{
		var fechaInicial = new Date($("#dtpPeriodoInicio").datepicker('getDate'));
		dia = fechaInicial.getDate();
	}
	else
	{
		dia = dia + 1;
	}
	
	var entrada = 0;
	var precio = parseFloat($("#txtPrecio").val());
	var tarifaMensual = parseFloat($("#varTotalTarifa").val());
	var tarifaDiaria = tarifaMensual / 30;
	var primaCotizador = 100;
	
	if ($("#varPrima").val() == 1)
	{
		primaCotizador = 1000;
	}
	
	if ($("#txtEntrada").val() != '')
	{
		entrada = parseFloat($("#txtEntrada").val());
	}
	
	if ($("#txtSalida").val() != '')
	{
		salida = parseFloat($("#txtSalida").val());
	}
	
	$("#varTotalExistencia").val((parseFloat($("#varTotalExistencia").val()) + entrada) - salida);
	
	var valorExistencia = parseFloat($("#varTotalExistencia").val()) * precio;	
	var cuota = (valorExistencia * tarifaDiaria) / primaCotizador;
	
	var contenido = $('.tabla_endoso tbody');
	$('<tr><td style="display:none;">'+''+'</td><td>'+dia+'</td><td>'+formatCurrency($("#txtEntrada").val())+'</td><td>'+formatCurrency($("#txtSalida").val())+'</td><td>'+ formatCurrency($("#varTotalExistencia").val())+'</td><td>'+formatCurrency(precio.toFixed(4))+'</td><td>'+formatCurrency(valorExistencia.toFixed(4))+'</td><td>'+formatCurrency(tarifaMensual.toFixed(4))+'</td><td>'+formatCurrency(tarifaDiaria)+'</td><td>'+formatCurrency(cuota)+"</td><td><a href='#' title='Editar' onclick='actualizarTablaDeclaracionDia($(this));'><i class='icon-refresh'></i></a></td></tr>").appendTo(contenido);
	$("#varSumaPromedioDiario").val(parseFloat($("#varSumaPromedioDiario").val()) + parseFloat($("#varTotalExistencia").val()));
	
	$("#varSumaPrecio").val(parseFloat($("#varSumaPrecio").val()) + precio);
	$("#varSumaValorExistencia").val(parseFloat($("#varSumaValorExistencia").val()) + valorExistencia);
	$("#varSumaCuotaMensual").val(parseFloat($("#varSumaCuotaMensual").val()) + tarifaMensual);
	$("#varSumaCuotaPeriodo1").val(parseFloat($("#varSumaCuotaPeriodo1").val()) + tarifaDiaria);
	$("#varSumaCuotaPeriodo2").val(parseFloat($("#varSumaCuotaPeriodo2").val()) + cuota);
	
	var contenido1 = $('.tabla_endoso_totales tbody');
	contenido1.html('');
	$('<tr><td>'+''+'</td><td>'+formatCurrency((parseFloat($("#varSumaPromedioDiario").val()) / parseInt($("#varTotalDias").val())).toFixed(4))+'</td><td>'+formatCurrency((parseFloat($("#varSumaPrecio").val()) / parseInt($("#varTotalDias").val())).toFixed(4))+'</td><td>'+formatCurrency((parseFloat($("#varSumaValorExistencia").val()) / parseInt($("#varTotalDias").val())).toFixed(4))+'</td><td>'+formatCurrency((parseFloat($("#varSumaCuotaMensual").val()) / parseInt($("#varTotalDias").val())).toFixed(4))+'</td><td>'+formatCurrency(parseFloat($("#varSumaCuotaPeriodo1").val()).toFixed(4))+'</td><td>'+formatCurrency(parseFloat($("#varSumaCuotaPeriodo2").val()).toFixed(4))+'</td></tr>').appendTo(contenido1);
	
	$("#varUltimoDiaIngresado").val(dia);
}

function daysInMonth(humanMonth, year) { // Función que regresa el número de dias del mes.
	  return new Date(year || new Date().getFullYear(), humanMonth, 0).getDate();
}