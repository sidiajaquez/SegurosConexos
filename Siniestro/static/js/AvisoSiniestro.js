$(document).on('ready',inicio); // Archivo que nos permite gestionar el funcionamiento del aviso de siniestro mediante la plantilla AvisoSiniestro.js

var objectValorCausaSiniestro // Objecto que permite almacenar los valores de una causa de siniestro.
{
	IdCotizadorCobertura = "";
	Deducible = "";
	ParticipacionAPerdida = "";
}

var listaValoresCausaSiniestro = []; // Array que permite almacenar los valores de la causa de siniestro.

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario aviso de siniestro.​
	 $('#tpHoraSiniestro').timepicker();
	 $('#tpHoraAviso').timepicker();
	 $("#dtpFechaSiniestro").datepicker();
	 $("#dtpFechaAviso").datepicker();
	 $("#btnBuscarConstancia").click(buscarConstancia);
	 $("#btnBuscarPersona").on("click", buscarPersonaAvisa);
	 $("#btnBuscarTecnico").on("click", buscarPersonaTecnico);
	 $("#btnGuardar").on("click", guardarAviso);
	 $("#btnListadoAvisos").on("click", regresarListadoAvisoSiniestro);
	 tabla_buscar_constancia();
	 tabla_buscar_persona_avisa();
	 tabla_buscar_persona_tecnico();
	 
	 document.getElementById('txtCausaAgravante').readOnly = true;
	 $('#cmbCausaSiniestro').prop('disabled', 'disabled');
	 
	 if ($("#varStatusAviso").val() == 1)
	 {
		 deshabilitarControlesFormulario(); 
	 }
	 
	 if ($("#varIdAvisoSiniestro").val() == '')
	 {
		 $("#dtpFechaSiniestro").datepicker('setDate',new Date());
		 $("#dtpFechaAviso").datepicker('setDate',new Date());
		 
	 }
	 else
	 {
		habilitarBotones();
		
		Dajaxice.Siniestro.buscar_causa_siniestro_programa(cargarComboCausaSiniestro, {'idPrograma':$("#varIdPrograma").val()});
		
		return false;
	 }
}

var habilitarBotones = function(){ // Función que nos permite habilitar los botones del terminar y vista previa.

	$("#btnVistaPrevia").on("click", reporteAvisoSiniestro);
	$("#btnVistaPrevia").removeAttr("disabled");
	
	if ($("#varStatusAviso").val() == 0)
	{
		$("#btnTerminar").on("click", establecerEstado);
		$("#btnTerminar").removeAttr("disabled");
	}
	
	if ($("#cmbTipoAviso option:selected").text() == 'SINIESTRO')
	{
		$('#cmbCausaSiniestro').removeAttr("disabled","disabled");
		document.getElementById('txtCausaAgravante').readOnly = true;
	}
	else if($("#cmbTipoAviso option:selected").text() == 'AGRAVANTE')
	{
		document.getElementById('txtCausaAgravante').readOnly = false;
		$('#cmbCausaSiniestro').attr("disabled","disabled");
	}		
}

var deshabilitarControlesFormulario = function(){ // Función que nos permite deshabilitar los controles del formulario para dejarlo de solo lectura. 
	$('#cmbTipoAviso').prop('disabled', 'disabled');
	document.getElementById('dtpFechaAviso').readOnly = true;
	document.getElementById('tpHoraAviso').readOnly = true;
	document.getElementById('dtpFechaSiniestro').readOnly = true;
	document.getElementById('tpHoraSiniestro').readOnly = true;
	$('#cmbViaAviso').prop('disabled', 'disabled');
	document.getElementById('txtOtros').readOnly = true;
	document.getElementById('txtQuienAvisa').readOnly = true;
	document.getElementById('txtQuienRecibe').readOnly = true;
	document.getElementById('txtBien').readOnly = true;
	document.getElementById('txtCausaAgravante').readOnly = true;
	$('#cmbCausaSiniestro').prop('disabled', 'disabled');
	
	$("#btnBuscarConstanciaModal").removeAttr("href");
	$("#btnBuscarConstanciaModal").attr("disabled","disabled");
	$("#btnBuscarPersonaModal").removeAttr("href");
	$("#btnBuscarPersonaModal").attr("disabled","disabled");
	$("#btnBuscarTecnicoModal").removeAttr("href");
	$("#btnBuscarTecnicoModal").attr("disabled","disabled");
	$("#btnTerminar").unbind("click");
	$("#btnTerminar").attr("disabled","disabled");
	$("#btnGuardar").unbind("click");
	$("#btnGuardar").attr("disabled","disabled");
	$("#btnTerminar").unbind("click");
	$("#btnTerminar").attr("disabled","disabled");
	
	$('table:input').attr('disabled','disabled'); 
	
	$('.tbl_bienes tr').each(function()
	{
		var fila = $(this).find('td');
	    if (fila.length > 0)
	    {			
			$(this).closest("tr").find("input").each(function(){
				
				$(this).attr("disabled","disabled"); 
		    });	
	    }    
	});
}

var cambiarCombo = function(){ // Función que nos permite activar cajas de texto cuando cambia el combo.
	
	var selectTipoAviso = document.getElementById("cmbTipoAviso");
	
	if (selectTipoAviso.options[selectTipoAviso.selectedIndex].text == "---------")
	{
		$('#cmbCausaSiniestro').prop('disabled', 'disabled');
		document.getElementById('txtCausaAgravante').readOnly = true;
	}	
	else if (selectTipoAviso.options[selectTipoAviso.selectedIndex].text == "AGRAVANTE")
	{
		document.getElementById('txtCausaAgravante').readOnly = false;
		$('#cmbCausaSiniestro').attr("disabled","disabled");
	}
	else if (selectTipoAviso.options[selectTipoAviso.selectedIndex].text == "SINIESTRO")
	{
		$('#cmbCausaSiniestro').removeAttr("disabled","disabled");
		document.getElementById('txtCausaAgravante').readOnly = true;
	}
}

var cambiarComboCausaSiniestro = function(){ // Función que nos permite activar la funcion cuando el cmb es activado.
	
	listaValoresCausaSiniestro.forEach(function(causa, posicion){
		if ($("#cmbCausaSiniestro").val() == causa.IdCotizadorCobertura)
		{
			$("#varDeducible").val(causa.Deducible);
			$("#varParticipacionAPerdida").val(causa.ParticipacionAPerdida);
;		}
	});
}

var establecerEstado = function(){ // Función que nos permite establecer el status de terminado al aviso del siniestro, establece el valor 1 a varStatusAviso el cual significa que esta terminado.
	$("#varStatusAviso").val(1);
	Dajaxice.Siniestro.guardar_estado_aviso(Dajax.process,{'idAviso':$('#varIdAvisoSiniestro').val(), 'idStatus':$("#varStatusAviso").val()});
	deshabilitarControlesFormulario();
	alertify.alert('Aviso terminado');
	return false;
}

var buscarConstancia = function(){ // Función que nos permite buscar la constancia mediante la función buscar_constancia de la clase ajax.py
	Dajaxice.Siniestro.buscar_constancia(cargarDatosConstancia,{'buscar':$("#txtBuscarConstancia").val()});
	return false;
}

var cargarDatosConstancia = function(data){ // Función que nos permite cargar los datos obtenidos de la busqueda de la constancia en el modal.
	var contenido = $('.tbl_buscar_constancia tbody');
	contenido.html('');
	
	if(data.constancias != null && data.constancias.length > 0)
	{
		$.each(data.constancias, function(i,constancia)
		{
			$('<tr><td>'+constancia.Constancia+'</td><td>'+constancia.Ejercicio+'</td><td>'+constancia.Asegurado+'</td><td>'+constancia.Vigencia+'</td><td style="display: none;">'+constancia.IdConstancia+'</td><td style="display: none;">'+constancia.IdPrograma+'</td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontraron constancias para generar el aviso de siniestro.');
	}
}

var tabla_buscar_constancia = function(){ // Función que permite interactuar con la ventana modal de buscar constancias.
	$(".modal").on('shown', function(){
	    $("#txtBuscarConstancia").focus();
	});
	
	$('.tbl_buscar_constancia tbody').on('mouseover', 'tr', function(event){ // toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tbl_buscar_constancia tbody').on('mouseout', 'tr', function(event){ // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	

	$('.tbl_buscar_constancia tbody').on('click', 'tr', function(event){ // evento click que selecciona el row y marca el check de la tabla		
		$("#txtConstancia").val($(this).children('td')[0].innerText);
		$("#txtEjercicio").val($(this).children('td')[1].innerText);
		$("#txtNombreAsegurado").val($(this).children('td')[2].innerText);
		$("#txtVigenciaConstancia").val($(this).children('td')[3].innerText);
		$("#varIdConstancia").val($(this).children('td')[4].innerText);
		$("#varIdPrograma").val($(this).children('td')[5].innerText);
		$(".close").click();
		
		Dajaxice.Siniestro.obtener_descripcion_bienes_constancia(cargarBienesEnTabla, {'id_constancia': $("#varIdConstancia").val()});
		return false;
	});
}

var cargarComboCausaSiniestro = function(data){ // Función que nos permite cargar el combo causa de siniestro
	
	var llenarCombo = true;
	
	if ($("#cmbCausaSiniestro").length > 1)
	{		
		llenarCombo = false;
	}
	
	$.each(data.causaSiniestro, function(i,causa)
	{
		objectValorCausaSiniestro = new Object();
		objectValorCausaSiniestro.IdCotizadorCobertura = causa.IdCotizadorCobertura;
		objectValorCausaSiniestro.Deducible = causa.Deducible;
		objectValorCausaSiniestro.ParticipacionAPerdida = causa.ParticipacionAPerdida;
		listaValoresCausaSiniestro.push(objectValorCausaSiniestro);
		
		if (llenarCombo)
		{
			$('#cmbCausaSiniestro').append(new Option(causa.Descripcion.toUpperCase(), causa.IdCotizadorCobertura));
		}		
	});
}

var cargarBienesEnTabla = function(data){ // Función que nos permite cargar los bienes en la tabla tbl_bienes.
	
	var contenido = $('.tbl_bienes tbody');
	contenido.html('');
	
	if(data.descripcionBienes)
	{
		$.each(data.descripcionBienes, function(i,descripcion)
		{
			$('<tr><td style="display: none;">' + '' + '</td><td style="display: none;">'+descripcion.IdDescripcion+'</td><td><input type="checkbox" name="checkSeleccionar" value="checked" onClick="checkedInputs()"/></td><td>'+descripcion.NombreEquipo+'</td><td>'+descripcion.Cantidad+'</td><td>'+descripcion.ValorUnitario+'</td><td>'+descripcion.SumaBien+'</td><td style="text-align:center;"><input type="text" class="input-mini" value="" style="text-align:right;"></td><td style="text-align:center;"><input type="text" class="input-mini" value="" style="text-align:left;"></td><td style="text-align:center;"><input type="text" class="input-large" value="" style="text-align:left;"></td></tr>').appendTo(contenido);
		});
	}
	
	$("#varTieneAumento").val(data.tieneAumento);
	
	Dajaxice.Siniestro.buscar_causa_siniestro_programa(cargarComboCausaSiniestro, {'idPrograma':$("#varIdPrograma").val()});
	
	return false;
}

var buscarPersonaAvisa = function(){ // Función que nos permite buscar la persona mediante la función buscar_persona_avisa de la clase ajax.py
	Dajaxice.Siniestro.buscar_persona_avisa(cargarDatosPersonaAvisa,{'datosBuscar':$("#txtBuscarPersona").val()});
	return false;
}

var cargarDatosPersonaAvisa = function(data){ // Función que nos permite cargar los datos obtenidos de la busqueda de la persona que avisa en el modal.
	var contenido = $('.tbl_buscar_persona tbody');
	contenido.html('');
	
	if(data.personas != null && data.personas.length > 0)
	{
		$.each(data.personas, function(i,persona)
		{
			$('<tr><td>'+persona.Nombre+'</td><td>'+persona.Rfc+'</td><td style="display: none;">'+persona.IdPersona+'</td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontraron personas.');
	}
}

var tabla_buscar_persona_avisa = function(){ // Función que permite interactuar con la ventana modal de buscar personas las cuales avisaron del siniestro.
	$(".modal").on('shown', function() {
	    $("#txtBuscarPersona").focus();
	});
	
	$('.tbl_buscar_persona tbody').on('mouseover', 'tr', function(event){ // toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tbl_buscar_persona tbody').on('mouseout', 'tr', function(event) { // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	
 
	$('.tbl_buscar_persona tbody').on('click', 'tr', function(event){ // evento click que selecciona el row y marca el check de la tabla		
		$("#txtQuienAvisa").val($(this).children('td')[0].innerText);
		$("#varIdPersonaAvisa").val($(this).children('td')[2].innerText);
		$(".close").click();
	});
}

var buscarPersonaTecnico = function(){ // Función que nos permite buscar la persona mediante la función buscar_persona_tecnico de la clase ajax.py
	Dajaxice.Siniestro.buscar_persona_tecnico(cargarDatosPersonaTecnico,{'datosBuscar':$("#txtBuscarTecnico").val()});
	return false;
}

var cargarDatosPersonaTecnico = function(data){ // Función que nos permite cargar los datos obtenidos de la busqueda de la persona que es tecnico y recibe el aviso de siniestro en el modal.
	var contenido = $('.tbl_buscar_tecnico tbody');
	contenido.html('');
	
	if(data.tecnicos != null && data.tecnicos.length > 0)
	{
		tecnicos = data.tecnicos;
		
		for(rowArreglo=0;rowArreglo<tecnicos.length;rowArreglo++)
		{
			$('<tr><td>'+tecnicos[rowArreglo][2]+'</td><td>'+tecnicos[rowArreglo][1]+'</td><td style="display: none;">'+tecnicos[rowArreglo][0]+'</td></tr>').appendTo(contenido);
		}
	}
	else
	{
		alertify.alert('No se encontraron tecnicos.');
	}
}

var tabla_buscar_persona_tecnico = function(){ // Función que permite interactuar con la ventana modal de buscar personas que son tecnicos del fondo las cuales recibieron el aviso del siniestro.
	$(".modal").on('shown', function() {
	    $("#txtBuscarTecnico").focus();
	});
	
	$('.tbl_buscar_tecnico tbody').on('mouseover', 'tr', function(event) { //toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tbl_buscar_tecnico tbody').on('mouseout', 'tr', function(event) { //evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	

	$('.tbl_buscar_tecnico tbody').on('click', 'tr', function(event) { //evento click que selecciona el row y marca el check de la tabla		
		$("#txtQuienRecibe").val($(this).children('td')[0].innerText);
		$("#varIdTecnico").val($(this).children('td')[2].innerText);	
		$(".close").click();
	});
}

var seleccionarOtros = function(){ // Función que nos permite deshabilitar el txtOtros cuando en el combo cmbViaAviso se ha seleccionado OTROS.
	
	var selectAviso = document.getElementById("cmbViaAviso");
	
	if (selectAviso.options[selectAviso.selectedIndex].text == "OTROS")
	{
		document.getElementById('txtOtros').readOnly = false;
	}	
	else
	{
		document.getElementById('txtOtros').readOnly = true;
		$("#txtOtros").val('');
	}
}

var guardarAviso = function(){ // Función que nos permite guardar el aviso del siniestro en la base de datos mediante la función guardar_aviso_siniestro de la clase ajax.py.

	if (pasarComprobaciones())
	{				
		if ($("#varIdAvisoSiniestro").val() == "")
		{
			Dajaxice.Siniestro.guardar_aviso_siniestro(Dajax.process,{'formulario':$('#formulario_aviso_siniestro').serialize(true), 'horaAviso':$("#tpHoraAviso").val(), 'horaSiniestro':$("#tpHoraSiniestro").val(), 'bienes':validarArrayVacio(obtenerDatosDeLaTablaBienes()), 'tieneAumento':$("#varTieneAumento").val(), 'causaSiniestro':$("#cmbCausaSiniestro option:selected").text(), 'idCotizadorCobertura':$("#cmbCausaSiniestro option:selected").val(), 'deducible':$("#varDeducible").val(), 'participacionAPerdida':$("#varParticipacionAPerdida").val()});
		}
		else
		{
			alertify.confirm("¿Desea modificar el aviso?", function (e)
			{
			    if (e)
			    {
			    	Dajaxice.Siniestro.guardar_aviso_siniestro(Dajax.process,{'formulario':$('#formulario_aviso_siniestro').serialize(true), 'horaAviso':$("#tpHoraAviso").val(), 'horaSiniestro':$("#tpHoraSiniestro").val(), 'bienes':validarArrayVacio(obtenerDatosDeLaTablaBienes()), 'tieneAumento':$("#varTieneAumento").val(), 'causaSiniestro':$("#cmbCausaSiniestro option:selected").text(), 'idCotizadorCobertura':$("#cmbCausaSiniestro option:selected").val(), 'deducible':$("#varDeducible").val(), 'participacionAPerdida':$("#varParticipacionAPerdida").val()});
			    	alertify.success("Aviso Modificado Correctamente");
			    	window.setTimeout('obtener_bienesAfectadosActualizados()', 1000)
			    }
			});	
		}
		
		return false;
	}
}

var checkedInputs = function(){ // Función que nos permite checar si un checekbox tiene su evento checked limpia los imputs de la tabla.
		
	var regresarValor = '';
	var validarSeleccionado = false;
	var count = 0
	
	$('.tbl_bienes tr').each(function()
	{
		var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {			
			$(this).closest('tr').find("input[type=checkbox]:not(:checked)").each(function(){		
				$(this).closest("tr").find("input").each(function(){
					if (count > 0)
					{
						this.value = "";
					}					
					
					count = count + 1;
				});
				
				count = 0;
		    });
	    }
	});
	
	return regresarValor;	
}

var mensajeGuardadoSiniestro = function(idAvisoSiniestro){ // Función que nos permite mostrar un mensaje cuando el aviso de siniestro es almacenado en la base de datos.
	$("#varIdAvisoSiniestro").val(idAvisoSiniestro);
	habilitarBotones();
	obtener_bienesAfectadosActualizados();
	alertify.alert('Aviso Siniestro Guardado con el Folio: ' + idAvisoSiniestro);
}

var pasarComprobaciones = function() { // Función que nos permite validar si la información ingresada en el formulario es la correcta.
	
	if ($("#varIdConstancia").val() == '')
	{
		alertify.alert("Se requiere seleccionar constancia para continuar.");
		return false;
	}
	
	var selectTipoAviso = document.getElementById("cmbTipoAviso");
	
	if (selectTipoAviso.options[selectTipoAviso.selectedIndex].text == "---------")
	{
		alertify.alert("Se requiere seleccionar tipo de aviso para continuar.");
		return false;
	}
	
	if ($("#dtpFechaAviso").val() == '')
	{
		alertify.alert("Se requiere ingresar la fecha del aviso para continuar.");
		return false;
	}
	
	if ($("#tpHoraAviso").val() == '')
	{
		alertify.alert("Se requiere ingresar la hora del aviso para continuar.");
		return false;
	}
	
	if ($("#dtpFechaSiniestro").val() == '')
	{
		alertify.alert("Se requiere ingresar la fecha del siniestro para continuar.");
		return false;
	}
	
	if ($("#tpHoraSiniestro").val() == '')
	{
		alertify.alert("Se requiere ingresar la hora del siniestro para continuar.");
		return false;
	}
	
	var selectAviso = document.getElementById("cmbViaAviso");
	
	if (selectAviso.options[selectAviso.selectedIndex].text == "---------")
	{
		alertify.alert("Se requiere seleccionar via de aviso para continuar.");
		return false;
	}
	
	if (selectAviso.options[selectAviso.selectedIndex].text == "OTROS" && $("#txtOtros").val() == '')
	{
		alertify.alert("Se requiere ingresar otra via de aviso para continuar.");
		return false;
	}
	
	if ($("#txtQuienAvisa").val() == '')
	{
		alertify.alert("Se requiere ingresar o seleccionar a la persona que avisa para continuar.");
		return false;
	}
	
	if ($("#txtQuienRecibe").val() == '')
	{
		alertify.alert("Se requiere seleccionar al tecnico que recibe para continuar.");
		return false;
	}
	
	var selectCausa = document.getElementById("cmbCausaSiniestro");
	
	if (selectCausa.options[selectCausa.selectedIndex].text == "---------")
	{
		alertify.alert("Se requiere seleccionar causa del siniestro para continuar.");
		return false;
	}
		
	mensajeValidacion = validarBienesSeleccionados();
	
	if (mensajeValidacion != '')
	{
		alertify.alert(mensajeValidacion);
		return false;
	}
		
	return true;
}

function regresarListadoAvisoSiniestro(){ // Función que permite regresar al listado de los avisos de siniestro.
	location.href = '/ListadoAvisoSiniestro/';
}

function validarBienesSeleccionados(){ // Función que nos permite validar los bienes selecionados.
	 
	var regresarValor = '';
	var validarSeleccionado = false;
	var count = 0;
	
	$('.tbl_bienes tr').each(function()
	{
		var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {			
			$(this).closest('tr').find("input[type=checkbox]:checked").each(function(){			
				validarSeleccionado = true;
				
				$(this).closest("tr").find("input").each(function(){
					
					if(count > 0 && this.value == '')
					{
						regresarValor = "Se requiere ingresar valores en bien para continuar";
						return;
					}
					
					count = count + 1;
			    });	
				
				count = 0;
		    });
	    }    
	});
	
	if (!validarSeleccionado)
	{
		regresarValor = "Se requiere seleccionar un bien afectado para continuar.";
	}
	
	return regresarValor;
}

function obtenerDatosDeLaTablaBienes(){ // Función que nos premite ingresar en un arrayBienes los datos de los bienes seleccionados en la tabla tbl_bienes.
	var arrayBienes = [];
	countInput = 0;
	
	$('.tbl_bienes tr').each(function(){
		var fila = $(this).find('td');
	    if (fila.length > 0)
	    {
	    	$(this).closest('tr').find("input[type=checkbox]:checked").each(function(){			
	    		var arrayFilas = [];
				arrayFilas.push($(this).closest("tr").find("td").eq(0).html());
				arrayFilas.push($(this).closest("tr").find("td").eq(1).html()); 	
				$(this).closest("tr").find("input").each(function(){
					if (countInput > 0)
					{
						arrayFilas.push(this.value);
					}
					
					countInput ++;
			    });
				
				countInput = 0;
				
				arrayBienes.push(arrayFilas);
		    });	    	
	    }
	});
	
	return arrayBienes;
}

function obtener_bienesAfectadosActualizados(){ // Función que nos permite obtener los bienes afectados.

	Dajaxice.Siniestro.obtener_bienes_afectados(cargarBienesAfectados,{'id_aviso':$("#varIdAvisoSiniestro").val(), 'id_constancia':$("#varIdConstancia").val()});
	return false;
}

function cargarBienesAfectados(data){ // Función que nos permite cargar los bienes afectados en la tabla tbl_bienes al momento de guardar.

	var contenido = $('.tbl_bienes tbody');
	contenido.html('');
	
	if(data.bienesAfectados)
	{
		$.each(data.bienesAfectados, function(i,bien)
		{
			if (bien.IdBienAfectado == "")
			{
				$('<tr><td style="display: none;">' + bien.IdBienAfectado + '</td><td style="display: none;">'+bien.IdDescripcion+'</td><td><input type="checkbox" name="checkSeleccionar" value="" onClick="checkedInputs();"/></td><td>'+bien.Nombre+'</td><td>'+bien.Cantidad+'</td><td>'+bien.ValorUnitario+'</td><td>'+bien.SumaAsegurada+'</td><td style="text-align:center;"><input type="text" class="input-mini" value="'+ bien.NoBienesAfectados +'" style="text-align:right;"></td><td style="text-align:center;"><input type="text" class="input-mini" value="'+ bien.EstadoDanos +'" style="text-align:left;"></td><td style="text-align:center;"><input type="text" class="input-large" value="'+ bien.Descripcion +'" style="text-align:left;"></td></tr>').appendTo(contenido);
			}
			else
			{
				$('<tr><td style="display: none;">' + bien.IdBienAfectado + '</td><td style="display: none;">'+bien.IdDescripcion+'</td><td><input type="checkbox" name="checkSeleccionar" onClick="checkedInputs();" checked /></td><td>'+bien.Nombre+'</td><td>'+bien.Cantidad+'</td><td>'+bien.ValorUnitario+'</td><td>'+bien.SumaAsegurada+'</td><td style="text-align:center;"><input type="text" class="input-mini" value="'+ bien.NoBienesAfectados +'" style="text-align:right;"></td><td style="text-align:center;"><input type="text" class="input-mini" value="'+ bien.EstadoDanos +'" style="text-align:left;"></td><td style="text-align:center;"><input type="text" class="input-large" value="'+ bien.Descripcion +'" style="text-align:left;"></td></tr>').appendTo(contenido);
			}
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

var reporteAvisoSiniestro = function(){ // Función que permite imprimir el aviso de siniestro.
	window.open('/ReporteAvisoSiniestro/' + $("#varIdAvisoSiniestro").val());
}
