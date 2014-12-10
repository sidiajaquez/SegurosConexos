$(document).on('ready',inicio); // Archivo que nos permite gestionar el funcionamiento de la acta de siniestro mediante la plantilla actasiniestro.js

var objectProcedencia // Objeto que nos permiete gestionar la información de los bienes cuando estos son procedentes.
{
	IdBienActaSiniestro = ""
	IdBienAfectado = "";
	RiesgoAfectado = "";
	UnidadesAfectadas = "";
	Solvento = "";
	Proporcion = "";
	FuePerdida = "";
	Monto = "";
	Total = "";
	TipoBienActaSiniestro = "";
}

var objectNegativa // Objeto que nos permite gestionar la información de los bienes cuando estos son negativos.
{
	IdBienActaSiniestro = "";
	IdBienAfectado = "";
	Descripcion = "";
	TipoBienActaSiniestro = "";
}

var listaBienProcedencia = []; // Array donde almacenamos objetos de tipo objectProcedencia.
var listaBienNegativa = []; // Array donde almacenamos objetos de tipo objectNegativa.
var botonSeleccionado = false; // Variable el cual indica si algun boton de la tabla tbl_bienes ha sido seleccionado.

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario acta de siniestro.
		
	$.ajaxSetup({
		beforeSend: function(xhr, settings){
			if (settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}		
	});
	
	$("#dtpFechaSiniestro").datepicker({
		firstDay: 1
	});
	
	$("#dtpFechaSiniestro").val(fechaActual());
	$('#btnGuardarModalBienProcedencia').on('click', seleccionarListadoProcedencia);
	$('#btnGuardarModalBienNegativa').on('click', seleccionarListadoNegativa);
	$('#btnGuardar').on('click', guardarActaSiniestro);
	$("#btnListadoAvisos").on("click", regresarListadoInspecciones);
	$("#btnCerrarModalBienProcedencia").on("click", limpiarModalBienProcedencia);
	$("#btnCerrarModalBienNegativa").on("click", limpiarModalBienNegativa);
					
	tabla_completar_procedencia();
	cargarBienesAfectados();
}

function regresarListadoInspecciones(){ // Función que permite regresar al listado de las declaraciones de los endosos.
	location.href = '/ListadoInspecciones/';
}

var cargarBienesAfectados = function(){ // Función que nos permite cargar los bienes afectados en la tabla
	
	$.ajax
	(
		{
			url:'/ObtenerBienesActaSiniestro/',
			type:'POST',
			data:{idActaSiniestro:$("#varIdActaSiniestro").val()},
			success:cargarBienesEncontradosEnTabla
		}
	);
}

var cargarBienesEncontradosEnTabla = function(data){ // Función que recibe los bienes encontrados mediante el id del acta de siniestro para cargarlos a la tabla de bienes.
	
	listaBienProcedencia = []
	listaBienNegativa = []
	
	if (data.bienes)
	{	
		$.each(data.bienes, function(i,bien)
		{			
			if (bien.TipoBienActaSiniestro == 'PROCEDENCIA') // Si la descripción viene en blanco esto significa que el objeto se agregara al elemento array procedencia, si no se agregara al array negativa.
			{
				agregarElementoArrayProcendecia(bien);
			}
			else
			{
				agregarElementoArrayNegativa(bien);
			}
		});
	}
}

var agregarElementoArrayProcendecia = function(bien){ // Función que nos permite agregar un objeto al array de procedencia.
	
	objectProcedencia = new Object();
	objectProcedencia.IdBienActaSiniestro = bien.IdBienActaSiniestro;
	objectProcedencia.IdBienAfectado = bien.IdBienAfectado;
	objectProcedencia.RiesgoAfectado = bien.RiesgoAfectado;
	objectProcedencia.UnidadesAfectadas = bien.UnidadesAfectadas;
	objectProcedencia.Solvento = bien.Solvento;
	objectProcedencia.Proporcion = bien.Proporcion;	
	objectProcedencia.FuePerdida = bien.FuePerdida;
	objectProcedencia.Monto = bien.Monto;
	objectProcedencia.Total = bien.Total;
	objectProcedencia.TipoBienActaSiniestro = bien.TipoBienActaSiniestro;
	listaBienProcedencia.push(objectProcedencia);
}

var agregarElementoArrayNegativa = function(bien){ // Función que nos permite agregar un objeto al array de negativa.
	
	objectNegativa = new Object();
	objectNegativa.IdBienActaSiniestro = bien.IdBienActaSiniestro;
	objectNegativa.IdBienAfectado = bien.IdBienAfectado;
	objectNegativa.Descripcion = bien.Descripcion;
	objectNegativa.TipoBienActaSiniestro = bien.TipoBienActaSiniestro;
	listaBienNegativa.push(objectNegativa);
}

var fechaActual = function(){ // Función que genera y devuelve la fecha de hoy.
	
	var currentTime = new Date();
	var day = ("0" + currentTime.getDate()).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return (day+'/'+month+'/'+year);
}

var cambiarCombo = function(data){ // Función que nos permite vaciar arrays si se selecciona otra opción en el combobox.
	
	var rowData = data.closest("tr");
	
	$("#varIdBienAfectado").val(rowData.children('td')[0].innerText);	
	var posicionProcedencia = "";

	listaBienProcedencia.forEach(function(bien, posicion){
		if ($("#varIdBienAfectado").val() == bien.IdBienAfectado)
		{
			posicionProcedencia = posicion;
		}
	});
	
	if (String(posicionProcedencia) != "")
	{
		listaBienProcedencia.splice(posicionProcedencia, 1);
	}
	
	var posicionNegativa = "";

	listaBienNegativa.forEach(function(bien, posicion){
		if ($("#varIdBienAfectado").val() == bien.IdBienAfectado)
		{
			posicionNegativa = posicion;
		}
	});
	
	if (String(posicionNegativa) != "")
	{
		listaBienNegativa.splice(posicionNegativa, 1);
	}
}

var abrirModalProcedencia = function(data) { // Función que nos permite abrir el modal procedencia.
		
	var rowData = data.closest("tr");
	
	$("#varIdBienAfectado").val(rowData.children('td')[0].innerText);
	$("#varIdBienActaSiniestro").val(rowData.children('td')[15].innerText);
	var riesgoAfectado = rowData.children('td')[2].innerText;
	var numeroBienesAfectados = rowData.children('td')[6].innerText;
	var sumaAsegurada = rowData.children('td')[5].innerText;
	var deducible = rowData.children('td')[10].innerText;
	var participacionAPerdida = rowData.children('td')[11].innerText;
	
	var valorSelect = rowData.find('option:selected').text();
	
	if (valorSelect == '--------')
	{
		alertify.alert('Se requiere seleccionar si es Procedencia/Negativa para continuar.');
	}
	else
	{
		if (valorSelect == 'PROCEDENCIA')
		{
			cargarModalProcedenciaArray(riesgoAfectado, numeroBienesAfectados, sumaAsegurada, deducible, participacionAPerdida);
			$('#modal_procedencia').modal('show');
		}
		else if (valorSelect == 'NEGATIVA')
		{
			cargarModalNegativaArray(riesgoAfectado);
			$('#modal_negativa').modal('show');
		}
	}
}

var regresarListadoInspecciones = function(){ // Función que permite regresar al listado de las inspecciones.
	location.href = '/ListadoInspecciones/';
}

var guardarActaSiniestro = function(){ // Función que nos permite guardar  de la clase ajax.py.
	
	if (pasarComprobacionesGuardar())
	{
		var arrayBienesProcedencia = JSON.stringify(listaBienProcedencia);
		var arrayBienesNegativa = JSON.stringify(listaBienNegativa);
		
		if ($("#varIdActaSiniestro").val() == "")
		{	
			$.ajax
			(
				{
					url:'/ActaSiniestroGuardar/',
					type:'POST',
					data:{ idActaSiniestro:$("#varIdActaSiniestro").val(), tipoAviso:$("#txtTipoAviso").val(), fechaSiniestro:$("#dtpFechaSiniestro").val(), montoDano:replaceAll($("#txtMontoDano").val(),',',''),
							idInspeccion:$("#varIdInspeccion").val(), horaSiniestro:$("#tpHoraSiniestro").val(), bienesProcedencia:arrayBienesProcedencia, bienesNegativa:arrayBienesNegativa},
					success:cargarMensajeGuardar
				}
			);		
		}
		else
		{
			alertify.confirm("¿Desea modificar el acta de siniestro?", function (e)
			{				
				$.ajax
				(
					{
						url:'/ActaSiniestroGuardar/',
						type:'POST',
						data:{ idActaSiniestro:$("#varIdActaSiniestro").val(), tipoAviso:$("#txtTipoAviso").val(), fechaSiniestro:$("#dtpFechaSiniestro").val(), montoDano:replaceAll($("#txtMontoDano").val(),',',''),
								idInspeccion:$("#varIdInspeccion").val(), horaSiniestro:$("#tpHoraSiniestro").val(), bienesProcedencia:arrayBienesProcedencia, bienesNegativa:arrayBienesNegativa}
					}
				);
				
				alertify.success("El acta de siniestro se modifico correctamente.");
			});
		}
	}	
}

var cargarMensajeGuardar = function(folio){ // Función que nos permite guardar el id del acta de siniestro guardada y manda un mensaje con el numero de folio con el cual se guardo el acta de siniestro.
	$("#varIdActaSiniestro").val(folio.folio);
	$("#txtFolioActa").val(folio.folio);
	cargarBienesAfectados();
	alertify.success("La Acta de Siniestro se guardo con el Folio: " + folio.folio);
}

var pasarComprobacionesGuardar = function(){ // Función que nos permite verificar si la información ingresada en el formulario es la correcta para almacenarla en la base de datos.
	
	var idBien = 0;
	var bienEncontrado = false;
	var descripcion = '';
	var agregarProcedencia = false;

	if ($("#txtTipoAviso").val() == "---------")
	{
		alertify.alert("Se requiere seleccionar el tipo de aviso para continuar.");
		return false;
	}
	
	if ($("#dtpFechaSiniestro").val() == "")
	{
		alertify.alert("Se requiere ingresar fecha de siniestro para continuar.");
		return false;
	}
	
	if ($("#txtMontoDano").val() == "")
	{
		alertify.alert("Se requiere ingresar el monto del daño para continuar.");
		return false;
	}
	
	$('.tbl_bienes tr').each(function(){
		var fila = $(this).find('td');
		
		if (fila.length > 0)
		{	
			idBien = $(this).closest("tr").find("td").eq(0).html();
			$(this).closest("tr").find("select").each(function(){
				if (this.value == '--------')
				{
					agregarProcedencia = true;
				}
				else if (this.value == 'PROCEDENCIA')
				{
					descripcion = 'PROCEDENCIA'; 
					
					listaBienProcedencia.forEach(function(bien, posicion){
						if (idBien == bien.IdBienAfectado)
						{
							bienEncontrado = true;
						}
					});
				}
				else if (this.value == 'NEGATIVA')
				{
					descripcion = 'NEGATIVA';
					
					listaBienNegativa.forEach(function(bien, posicion){
						if (idBien == bien.IdBienAfectado)
						{
							bienEncontrado = true;
						}
					});
				}
		    });
		}
	});
	
	if (agregarProcedencia)
	{
		alertify.alert("Se requiere seleccionar Procedencia/Negativa para continuar.");
		return false;
	}	
	else if (!bienEncontrado)
	{
		alertify.alert("Se requiere ingresar datos extra de la " + descripcion + " del bien para continuar.");				
		return false;
	}
		
	return true;
}

var tabla_completar_procedencia = function(){ // Función que permite seleccionar el row de la tabla.
	
	$('.tbl_bienes tbody').on('mouseover', 'tr', function(event){ // toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tbl_bienes tbody').on('mouseout', 'tr', function(event){ // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	
}

var cargarModalProcedenciaArray = function(riegoAfectado, numeroBienesAfectados, sumaAsegurada, deducible, participacionAPerdida){ // Función que nos permite encontrar un objecto dentro del arreglo listaBienProcedencia para cargar los controles del modal procendecia.
	
	var idBienBuscado = $("#varIdBienAfectado").val();	
	$("#txtProporcion").val(replaceAll(sumaAsegurada, ',',''));
	$("#txtDeducible").val(deducible);
	$("#txtParticipacionAPerdida").val(participacionAPerdida);
	$("#txtSumaAseguradaModal").val(replaceAll(sumaAsegurada, ',',''));
	
	seEncontroProcedenciaAgregada = false; // Indicador para checar si procedencia no se ah cargado ningun valor, entonces me muestra en automatico las unidades del aviso de siniestro.
	
	listaBienProcedencia.forEach(function(bien, posicion){
		if (idBienBuscado == bien.IdBienAfectado)
		{
			$("#varSumaAseguradaBien").val(bien.Proporcion);
			$("#cmdRiesgoAfectado").val(bien.RiesgoAfectado);
			$("#txtUnidadesAfectadas").val(bien.UnidadesAfectadas);
			$("#txtSolvento").val(bien.Solvento);				
			
			if(bien.FuePerdida == 0)
			{
				document.getElementById('txtProporcion').readOnly = false;
				$("input:radio[name=optionsRadios]")[0].checked = true;	
			}
			else
			{
				document.getElementById('txtProporcion').readOnly = true;
				$("#txtProporcion").val($("#varSumaAseguradaBien").val());
				$("input:radio[name=optionsRadios]")[1].checked = true;	
			}
			
			$("#txtProporcion").val(bien.Proporcion);
			$("#txtMontoIndemnizable").val(bien.Monto);
			seEncontroProcedenciaAgregada = true;
		}
	});
	
	if (!seEncontroProcedenciaAgregada)
	{
		$("#cmdRiesgoAfectado").val(riegoAfectado); 
		$("#txtUnidadesAfectadas").val(numeroBienesAfectados);
	}
	
	recalcularMontos();
	cambiarOptions();
}

var cambiarOptions = function(){ // Función que nos permite generar los calculos cuando se presiona una opcion del radio button.
	
	if($("input[name='optionsRadios']:checked").val() == 0)
	{
		document.getElementById('txtProporcion').readOnly = false;
	}
	else
	{
		document.getElementById('txtProporcion').readOnly = true;
		$("#txtProporcion").val($("#varSumaAseguradaBien").val());
	}
	
	recalcularMontos();
}

var recalcularMontos = function(){ // Función que nos permite recalcular los montos al momento de seleccionar que tipo de perdida se refiere.
	
	var varSalvamento = parseFloat($("#txtSumaAseguradaModal").val()) - parseFloat($("#txtProporcion").val());
	$("#txtSolvento").val(varSalvamento);
	var varDeducible = (parseFloat($("#txtProporcion").val()) * parseFloat($("#txtDeducible").val())) /100;
	var varParticipacionAPerdida = (parseFloat($("#txtProporcion").val()) * parseFloat($("#txtParticipacionAPerdida").val())) /100;
	
	var monto = parseFloat($("#txtProporcion").val()) - (varDeducible + varParticipacionAPerdida);
    $("#txtMontoIndemnizable").val(monto);
}

var cargarModalNegativaArray = function(){ // Función que nos permite encontrar un objecto dentro del arreglo listaBienNegativa para cargar los controles del modal negativa.
	
	var idBienBuscado = $("#varIdBienAfectado").val(); 
	
	if (idBienBuscado != '')
	{		
		listaBienNegativa.forEach(function(bien, posicion){
			if (idBienBuscado == bien.IdBienAfectado)
			{
				$("#txtDescripcionNegativa").val(bien.Descripcion);
			}
		});
	}
}

var seleccionarListadoProcedencia = function(){ // Función que nos permite guardar o modificar un elemento al arreglo listaBienProcedencia.
	
	var montoDano = 0;
	var encabezadoTabla = false;
	
	if (pasarComprobacionesModalBienProcendecia())
	{	
		var encontrado = false;
		
		var idBienBuscado = $("#varIdBienAfectado").val(); 
		
		listaBienProcedencia.forEach(function(bien, posicion){ // Se busca el bien para verificiar si ya fue agregado si se encuentra se actualiza el object.
			if (idBienBuscado == bien.IdBienAfectado)
			{
				bien.RiesgoAfectado = $("#cmdRiesgoAfectado").val();
				bien.UnidadesAfectadas = $("#txtUnidadesAfectadas").val();
				bien.Solvento = $("#txtSolvento").val();
				bien.FuePerdida = $("input[name='optionsRadios']:checked").val();
				bien.Proporcion = $("#txtProporcion").val();
				bien.Monto = $("#txtMontoIndemnizable").val();
				bien.Total = $("#txtIndemnizacionTotal").val();
				
				encontrado = true;
			}
		});
		
		if (!encontrado)
		{
			agregarListaProcedencia();
		}
		else
		{
			$('.tbl_bienes tr').each(function(){
				
				if (encabezadoTabla)
				{
					var idBienAfectado = $(this).find("td").eq(0).html();
					
					if (idBienAfectado == $("#varIdBienAfectado").val())
					{
						$(this).find("td").eq(6).text(formatCurrency($("#txtUnidadesAfectadas").val()));
						$(this).find("td").eq(9).text(formatCurrency($("#txtProporcion").val()));
						$(this).find("td").eq(12).text(formatCurrency($("#txtMontoIndemnizable").val()));
						
						montoDano = montoDano + parseFloat($("#txtMontoIndemnizable").val());
					}
					else
					{
						montoDano = montoDano + parseFloat(replaceAll($(this).find("td").eq(12).html(),',',''));
					}
				}
				
				encabezadoTabla = true;
			})
			
			$("#txtMontoDano").val(formatCurrency(montoDano));
		}	

		limpiarModalBienProcedencia();
		cerrarModalBienProcedencia();		
	}
}

var agregarListaProcedencia = function(){ // Función que nos permite agregar objetos a la lista de procedencia.
	
	var montoDano = 0;
	
	objectProcedencia = new Object();
	objectProcedencia.IdBienActaSiniestro = ''
	objectProcedencia.IdBienAfectado = $("#varIdBienAfectado").val();
	objectProcedencia.RiesgoAfectado = $("#cmdRiesgoAfectado").val();
	objectProcedencia.UnidadesAfectadas = $("#txtUnidadesAfectadas").val();
	objectProcedencia.Solvento = $("#txtSolvento").val();
	objectProcedencia.Proporcion = $("#txtProporcion").val();
	objectProcedencia.FuePerdida = $("input[name='optionsRadios']:checked").val();	
	objectProcedencia.Monto = $("#txtMontoIndemnizable").val();
	objectProcedencia.Total = $("#txtIndemnizacionTotal").val();
	listaBienProcedencia.push(objectProcedencia);
	
	var encabezadoTabla = false;
	
	$('.tbl_bienes tr').each(function(){
		
		if (encabezadoTabla)
		{
			var idBienAfectado = $(this).find("td").eq(0).html();
			
			if (idBienAfectado == $("#varIdBienAfectado").val())
			{
				$(this).find("td").eq(6).text(formatCurrency($("#txtUnidadesAfectadas").val()));
				$(this).find("td").eq(9).text(formatCurrency($("#txtProporcion").val()));
				$(this).find("td").eq(12).text(formatCurrency($("#txtMontoIndemnizable").val()));
				
				montoDano = montoDano + parseFloat($("#txtMontoIndemnizable").val());
			}
			else
			{
				montoDano = montoDano + parseFloat(replaceAll($(this).find("td").eq(12).html(),',',''));
			}
		}
		
		encabezadoTabla = true;
	})
	
	$("#txtMontoDano").val(formatCurrency(montoDano));
}

var limpiarModalBienProcedencia = function(){ // Función que nos permite limpiar los controles del modal procendecia cuando estos son guardados.
	
	$("#cmdRiesgoAfectado").val('');
	$("#txtUnidadesAfectadas").val('');
	$("#txtSolvento").val('');
	$("#txtProporcion").val('');
	$("#txtMontoIndemnizable").val('');
	$('#varSumaAseguradaBien').val('');
}

var seleccionarListadoNegativa = function(){ // Función que nos permite guardar o modificar un elemento al arreglo listaBienNegativa.
	
	if (pasarComprobacionesModalBienNegativa())
	{	
		var encontrado = false;
		
		var idBienBuscado = $("#varIdBienAfectado").val(); 
		
		listaBienNegativa.forEach(function(bien, posicion){ // Se busca el bien para verificiar si ya fue agregado si se encuentra se actualiza el object.
			if (idBienBuscado == bien.IdBienAfectado)
			{
				bien.Descripcion = $("#txtDescripcionNegativa").val();			
				encontrado = true;
			}
		});
		
		if (!encontrado)
		{
			agregarListaNegativa();
		}
		
		limpiarModalBienNegativa();
		cerrarModalBienNegativa();		
	}
}

var agregarListaNegativa = function(){ // Función que nos permite agregar objetos a la lista de negativa.

	objectNegativa = new Object();
	objectNegativa.IdBienActaSiniestro = ''
	objectNegativa.IdBienAfectado = $("#varIdBienAfectado").val();
	objectNegativa.Descripcion = $("#txtDescripcionNegativa").val();
	listaBienNegativa.push(objectNegativa);
}

var limpiarModalBienNegativa = function(){ // Función que nos permite limpiar los controles del modal negativa cuando sus datos son guardados.
	$("#txtDescripcionNegativa").val('');
}

var cerrarModalBienProcedencia = function(){ // Función que nos permite cerrar los modales. 
	$("#modal_procedencia").modal('hide');
}

var cerrarModalBienNegativa = function(){ // Función que nos permite cerrar los modales. 
	$("#modal_negativa").modal('hide');
}

var pasarComprobacionesModalBienProcendecia = function(){ // Función que nos permite pasar las comprobaciones del modal bien
	
	if ($("#cmdRiesgoAfectado").val() == '')
	{
		alertify.alert("Se requiere ingresar el bien afectado para continuar.");
		return false;
	}
	
	if ($("#txtUnidadesAfectadas").val() == '')
	{
		alertify.alert("Se requiere ingresar las unidades afectadas para continuar.");
		return false;
	}
	
	if ($("#txtSolvento").val() == '')
	{
		alertify.alert("Se requiere seleccionar una constancia continuar.");
		return false;
	}
	
	if ($("#txtProporcion").val() == '')
	{
		alertify.alert("Se requiere ingresar la proporción para continuar.");
		return false;
	}
	
	if ($("#txtFuePerdida").val() == '')
	{
		alertify.alert("Se requiere ingresar si fue perdida para continuar.");
		return false;
	}
	
	if ($("#txtMontoIndemnizable").val() == '')
	{
		alertify.alert("Se requiere ingresar el monto para continuar.");
		return false;
	}
	
	if ($("#txtIndemnizacionTotal").val() == '')
	{
		alertify.alert("Se requiere ingresar el total para continuar.");
		return false;
	}
	
	return true;
}

var pasarComprobacionesModalBienNegativa = function(){ // Función que nos permite validar el modal del bien nagativa.
	
	if ($("#txtDescripcionNegativa").val() == '')
	{
		alertify.alert("Se requiere ingresar la descripción de la negativa para continuar.");
		return false;
	}
	
	return true;
}