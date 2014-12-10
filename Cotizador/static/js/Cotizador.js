$(document).on('ready',inicio);

var valorFondo; 
var valorReaseguro;
var totalTarifa;
var totalFondo;
var totalReaseguro;
var rowsCotizadorCoberturas; // Variable que almacena cuantos registros de coberturas contiene el cotizador para controlar la fila del total.

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario cotizador.​
	activarMenu();
	
	$('#modal_Buscar_Programa_Cotizador').on('shown', function() {
		obtenerProgramasModal();
    });
	
    $("#btnGenerarTarifa").click(generarTarifaCotizador);
    $("#btnCancelarCotizador").on("click", limpiar_formulario_cotizador);
    $("#btnListadoCotizador").on("click", regresarListadoCotizador);
    $("#btnVistaPreviaCotizador").on("click", vistaPrevia);
	$("#btnGuardarCotizador").click(guardarCotizador);
	$("#btnGenerarTarifa").click(generarTarifaCotizador);
    
    tablaBusquedaPrograma();
    
    $('.tabla_cobertura_programa').keyup(function (e) {
    	generarTarifaCotizador();
    });
}

function mensajeCotizador(folioCotizador){ //Función que recibe el número de folio del cotizador de la función Dajaxice.Cotizador.guardar_cotizador para mostrarla en un alert
	alertify.alert('Cotizador Guardado con el Folio: '+ folioCotizador);
}

function vistaPrevia(){ // Función que permite mostrar el cotizador seleccionado de la table listado_programa_tabla pasando el id del programa a la plantilla programa.html
	if ($("#varIdCotizador").val() != "")
	{
		location.href = '/ReporteCotizador/?' + $("#varIdCotizador").val();
	}
	else
	{
		alertify.alert('Se requiere guardar para continuar.');
	}	
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function guardarCotizador(){ // Función que permite guardar el cotizador en la base de datos.
	if (pasarComprobacionesGuardarCotizador())
	{		
		if ($("#varIdCotizador").val() == '')
		{			
			Dajaxice.Cotizador.guardar_cotizador(Dajax.process,{'formulario':$('#formulario_cotizador').serialize(true), 'coberturas':validarArrayVacio(obtencionDatosCoberturasProgramas()), 'prima':$("input[name='optionsRadios']:checked").val(),'tarifaTotal':totalTarifa});
			limpiar_formulario_cotizador();
		}
		else
		{
			alertify.confirm("¿Desea modificar el cotizador?", function (e) 
			{
			    if (e)
			    {
			    	Dajaxice.Cotizador.guardar_cotizador(Dajax.process,{'formulario':$('#formulario_cotizador').serialize(true), 'coberturas':validarArrayVacio(obtencionDatosCoberturasProgramas()), 'prima':$("input[name='optionsRadios']:checked").val(),'tarifaTotal':totalTarifa});
					alertify.success("Datos Actualizados Correctamente");
			    	$("#PorcentajeFondo").focus();
			    }
			});
		}
	}
	
	return false;
}

function pasarComprobacionesGuardarCotizador(){ // Función que premite verificar si la información en el formulario es la correcta para continuar.
	
	var selectVigencia = document.getElementById("cmdVigencia");
	
	if (selectVigencia.options[selectVigencia.selectedIndex].text == "---------")
	{
		alertify.alert('Se requiere seleccionar vigencia para continuar.');
		return false;
	}
	
	if (!pasarComprobacionesGenerarTarifa())
	{
		return false;
	}
	
	if (rowsCotizadorCoberturas == $('.tabla_cobertura_programa tbody tr').length)
	{
		alertify.alert('Se requiere generar la cobertura para continuar.');
		return false;
	}
	
	$('.tabla_cobertura_programa tr').each(function(){
		var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {
			if ($(this).closest('tr').find("td").eq(0).html() == '')
			{
				if ($(this).closest('tr').find("td").eq(2).html() == '')
				{
					alertify.alert('Se requiere generar la cobertura para continuar.');
					return false;
				}
			}
	    }
	});
	
	var pasarComprobacionTarifa = validarTarifaCoberturas(); 
	
	if (pasarComprobacionTarifa != '')
	{
		alertify.alert(pasarComprobacionTarifa);
		return false;
	}
	
	return true;
}

function generarTarifaCotizador(){ // Función que permite generar la tarifa del cotizador.
	if (pasarComprobacionesGenerarTarifa())
	{
		limpiarVariables();
	
		$('.tabla_cobertura_programa  tr').each(function(){
			var count = 0;
			$(this).closest('tr').find("input").each(function(){
				if (count == 0)
				{
					valorFondo = parseInt($('#PorcentajeFondo').val().replace('%','') * this.value) / 100;
					valorReaseguro = parseInt($('#PorcentajeReaseguro').val().replace('%','') * this.value) / 100;
					totalTarifa += valorFondo + valorReaseguro;
					count = 1;
				}
		    });
			
			$(this).closest('tr').find("td").eq(3).html(valorFondo.toFixed(4));
			$(this).closest('tr').find("td").eq(4).html(valorReaseguro.toFixed(4));
			totalFondo = totalFondo + valorFondo;
			totalReaseguro = totalReaseguro + valorReaseguro;
		});
		
		var contenido = $('.tabla_cobertura_programa tbody');
		$('<tr><td style="display: none;">'+ '' +'</td><td>'+'Tarifa Total '+'</td><td><input type="text" class="input-mini" value="' + totalTarifa.toFixed(4) + '" style="text-align:right;" readonly /></td><td><input type="text" class="input-mini" value="' + totalFondo.toFixed(4) + '" style="text-align:right;" readonly /></td><td><input type="text" class="input-mini" value="' + totalReaseguro.toFixed(4) +'" style="text-align:right;" readonly/></td>').appendTo(contenido);
	}
}

function limpiarVariables(){ // Función que permite limpiar las variables que se utilizan para generar tarifa.	
	
	if (($('.tabla_cobertura_programa tr').length -1) != rowsCotizadorCoberturas){
		 $('.tabla_cobertura_programa tr:last').remove();
	}
	
	valorFondo = 0;
	valorReaseguro = 0;
	totalTarifa = 0;
	totalFondo = 0;
	totalReaseguro = 0;	
}

function pasarComprobacionesGenerarTarifa(){ // Función que nos permite verificar si la información ingresada en el formulario es la adecuada.
	
	if ($("#varIdPrograma").val() == "")
	{
		alertify.alert('Se requiere seleccionar programa para continuar.');
		return false;
	}
	
	if ($("#PorcentajeFondo").val() == '')
	{
		$("#PorcentajeFondo").focus();
		alertify.alert('Se requiere ingresar procentaje del fondo para continuar.');
		return false;
	}	
	
	if ($("#PorcentajeReaseguro").val() == '')
	{
		$("#PorcentajeReaseguro").focus();
		alertify.alert('Se requiere ingresar procentaje de reaseguro para continuar.');
		return false;
	}	
	
	var sumaPorcentaje = (parseInt($("#PorcentajeFondo").val()) + parseInt($("#PorcentajeReaseguro").val()));
	
	if (sumaPorcentaje > 100 || sumaPorcentaje < 100)
	{
		$("#PorcentajeFondo").focus();
		alertify.alert('La suma de los porcentajes del fondo y del reaseguro debe ser 100%');
		return false;
	}
	
	return true;
}

function validarTarifaCoberturas(){ // Función que nos permite validar si los campos de las tarifas tienen valor.
 
	var regresarValor = '';
	
	$('.tabla_cobertura_programa tr').each(function()
	{
		var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {			
			$(this).closest('tr').find("input").each(function(){			
				if (this.value == '')
				{
					regresarValor = 'Se requiere ingresar la tarifa de '+ $(this).closest('tr').find("td").eq(1).html() +'.';
					return;
				}
		    });
	    }    
	});
	
	return regresarValor;
}

function obtenerProgramasModal(){ // Función que carga los programas a elegir en el modal.
	Dajaxice.Programas.obtener_programas_ejercicio_actual(cargarProgramasEnModal);
	return false;
}

function cargarProgramasEnModal(dato){ // Función que carga los programas obtenidos de la función obtener_programas_ejercicio en la tabla buscar_programa que se encuentra en la plantilla cotizador.html
	var contenido = $('.tabla_buscar_programa tbody');
	contenido.html('');
	
	if(dato.programasActuales)
	{
		$.each(dato.programasActuales, function(i,programa)
		{
			var moneda;
			
			if (programa.IdTipoMoneda == 1)
			{
				moneda = "PESO MEXICANO";
			}
			else
			{
				moneda = "DÓLAR ESTADOUNIDENSE";
			}
			
			$('<tr><td style="display: none;">'+programa.IdPrograma+'</td><td>'+programa.TipoSeguro+'</td><td>'+programa.SubTipoSeguro+'</td><td>'+moneda+'</td><td>'+programa.FolioPrograma+'</td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function tablaBusquedaPrograma(){ // Función que permite interactuar con la ventana modal para buscar programas.
	
	$('.tabla_buscar_programa tbody').on('mouseover', 'tr', function(event) { //Toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tabla_buscar_programa tbody').on('mouseout', 'tr', function(event) { // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});

	var idPersona;
	
	$('.tabla_buscar_programa tbody').on('click', 'tr', function(event) { // permite agregar a la tabla de personas principal el registro que se seleccione.		
		$("#varIdPrograma").val($(this).children('td')[0].innerText);
		$("#txtTipoSeguro").val($(this).children('td')[1].innerText);
		$("#txtSubTipoSeguro").val($(this).children('td')[2].innerText);
		$("#txtMoneda").val($(this).children('td')[3].innerText);
		$("#txtFolio").val($(this).children('td')[4].innerText);
		$(".close").click();
		obtenerCoberturasPrograma();
	});	
}

function obtenerCoberturasPrograma(){ // Función que obtiene las coberturas del programa pasandole el id del programa.
	Dajaxice.Programas.obtener_cobertura_con_idprograma(cargarCoberturasPrograma,{'idPrograma':$("#varIdPrograma").val()});
	return false;
}

function cargarCoberturasPrograma(data){ // Función que carga las coberturas del programa en la tabla cobertura_programa.
	rowsCotizadorCoberturas = 0;
	celremocion = 0;
	
	var contenido = $('.tabla_cobertura_programa tbody');
	contenido.html('');
	
	if(data.coberturasPorPrograma)
	{			
		$.each(data.coberturasPorPrograma, function(i,cobertura)
		{
			remocion = '<td></td>';
			
			if (cobertura.Remocion == 1)
			{
				remocion = '<td><input type="text" class="input-mini" value="" style="text-align:right;" /></td>';
				celremocion = 1;
				
				if ($('#encabezado').children('th').length < 9)
				{
					$('#encabezado').append('<th style="text-align:center;">% Remocion</th>');
				}
			}
			
			$('<tr><td style="display: none;">'+ cobertura.IdCoberturaPrograma +'</td>' +
					'<td>'+cobertura.Descripcion+'</td>' +
					'<td><input type="text" class="input-mini" value="" style="text-align:right;" /></td>' +
					'<td style="text-align:right;">'+''+'</td>' +
					'<td style="text-align:right;">'+''+'</td>' +
					'<td style="display: none;">'+''+'</td>' +
					'<td><input type="text" class="input-mini" value="" style="text-align:right;" /></td>' +
					'<td><input type="text" class="input-mini" value="" style="text-align:right;" /></td>' +
					remocion +'</tr>').appendTo(contenido);
			rowsCotizadorCoberturas = rowsCotizadorCoberturas + 1
			
			remocion = '<td></td>';
		});
		
		$('<tr><td style="display: none;">'+ '' +'</td>' +
				'<td>'+"Total Tarifa "+'</td>' +
				'<td><input type="text" class="input-mini" value="" style="text-align:right;" readonly /></td>' +
				'<td><input type="text" class="input-mini" value="" style="text-align:right;" readonly /></td>' +
				'<td><input type="text" class="input-mini" value="" style="text-align:right;" readonly /></td>' +
				remocion +'</tr>').appendTo(contenido);
		
		if (celremocion == 0)
		{			
			$('.tabla_cobertura_programa').find('th:eq(8)').remove();
			$(".tabla_cobertura_programa td:last-child").remove();
		}
	}	
}

function obtencionDatosCoberturasProgramas(){ // Función que obtiene la información de la tabla cobertura_programa y la agrega a un arreglo.
	var arrayCobertura = [];
	
	$('.tabla_cobertura_programa tr').each(function(){
		var fila = $(this).find('td');
	    if (fila.length > 0)
	    {
			var arrayFilas = [];
			arrayFilas.push($(this).closest("tr").find("td").eq(0).html());			
			arrayFilas.push($(this).closest("tr").find("td").eq(1).html());		
			arrayFilas.push($(this).closest("tr").find("td").eq(3).html());
			arrayFilas.push($(this).closest("tr").find("td").eq(4).html());
			arrayFilas.push($(this).closest("tr").find("td").eq(5).html());
			
			$(this).closest("tr").find("input").each(function(){
				arrayFilas.push(parseFloat(this.value));
		    });
			
			if (arrayFilas.length == 8)
			{
				arrayFilas.push(parseFloat(0));
			}
			
			if ($(this).closest("tr").find("td").eq(0).html() != '')
			{
				arrayCobertura.push(arrayFilas);
			}
			else
			{
				totalTarifa = $(this).closest("tr").find("td").eq(2).html();
			}
	    }
	});
		
	return arrayCobertura;
}

function limpiar_formulario_cotizador(){ // Función que se encarga de limpiar el formulario de la plantilla Cotizador.html
		
	if ($("#varIdCoizador").val() == null)
	{
		document.getElementById("formulario_cotizador").reset();
		var contenido = $('.tabla_cobertura_programa tbody');
		contenido.html('');
		$("#varIdPrograma").val('');
		$("#varIdCotizador").val('');
		$("#varFolioPrograma").val('');
		$("#varIdProgramaAnterior").val('');
	}
	else
	{
		regresarListadoCotizador();
	}		
}

function regresarListadoCotizador() { // Función que permite regresar el listado al cotizador.
	location.href = '/Cotizadores/';
}

function actualizarVariableIdProgramaAnterior(){ // Función que permite actualizar la variable id programa anterior despues que el programa fue actualizado.
	$("#varIdProgramaAnterior").val($("#varIdPrograma").val());
}