$(document).on('ready',inicio); // Archivo que nos permite gestionar el funcionamiento de la inspección mediante la plantilla inspeccion.js

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario inspección.
	
	$("#btnBuscarAvisoSiniestro").click(buscarAvisoSiniestroTerminado);
	$("#btnBuscarTecnico").on('click', buscarTecnicos);
	$("#btnGuardar").on('click', guardarAviso);
	$("#btnListadoAvisos").on('click', regresarListadoInspecciones);
	
	tabla_buscar_aviso_siniestro();
	tabla_buscar_tecnicos();
	
	if($("#varIdInspeccion").val() != "")
	{
		$("#btnBuscarAvisoSiniestroModal").removeAttr("href");
		$("#btnBuscarAvisoSiniestroModal").attr("disabled","disabled");
	}
}

var regresarListadoInspecciones = function(){ // Función que permite regresar al listado de las inspecciones.
	location.href = '/ListadoInspecciones/';
}

var buscarAvisoSiniestroTerminado = function(){ // Función que nos permite buscar los avisos de siniestros terminados mediante la clase ajax.py
	Dajaxice.Siniestro.obtener_avisos_siniestro_terminados(cargarDatosATablaAvisoSiniestro,{'buscar':$("#txtBuscarAvisoSiniestro").val()});
	return false;
}

var cargarDatosATablaAvisoSiniestro = function(data){ // Función que nos permite cargar los datos obtenidos de la busqueda de los avisos de siniestro terminados en el modal.
	var contenido = $('.tbl_buscar_aviso_siniestro tbody');
	contenido.html('');
	
	if(data.avisos != null && data.avisos.length > 0)
	{
		avisos = data.avisos
		for(rowArreglo=0;rowArreglo<avisos.length;rowArreglo++)
		{	
			
			fechaVigencia = avisos[rowArreglo][16] + " al " + avisos[rowArreglo][17]
			$('<tr><td style="display: none;">'+avisos[rowArreglo][0]+'</td><td>'+avisos[rowArreglo][1]+'</td><td>'+avisos[rowArreglo][2]+'</td><td>'+avisos[rowArreglo][5]+'</td><td>'+ fechaVigencia +
				'</td><td style="display: none;">'+avisos[rowArreglo][3]+'</td><td style="display: none;">'+avisos[rowArreglo][4] +	'</td><td style="display: none;">'+avisos[rowArreglo][6] + 
				'</td><td style="display: none;">'+avisos[rowArreglo][8]+'</td><td style="display: none;">'+avisos[rowArreglo][7]+'</td><td style="display: none;">'+avisos[rowArreglo][9] +
				'</td><td style="display: none;">'+avisos[rowArreglo][10]+'</td><td style="display: none;">'+avisos[rowArreglo][11]+'</td><td style="display: none;">'+avisos[rowArreglo][12] +
				'</td><td style="display: none;">'+avisos[rowArreglo][13]+'</td><td style="display: none;">'+avisos[rowArreglo][14]+'</td><td>'+avisos[rowArreglo][15] +
				'</td><td style="display: none;">'+avisos[rowArreglo][18] +'</td></tr>').appendTo(contenido);
		}
	}
	else
	{
		alertify.alert('No se encontraron avisos de siniestro terminados para continuar.');
	}
}

var tabla_buscar_aviso_siniestro = function(){ // Función que permite interactuar con la ventana modal de buscar constancias.
	$(".modal").on('shown', function(){
	    $("#txtBuscarAvisoSiniestro").focus();
	});
	
	$('.tbl_buscar_aviso_siniestro tbody').on('mouseover', 'tr', function(event){ // toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tbl_buscar_aviso_siniestro tbody').on('mouseout', 'tr', function(event){ // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	

	$('.tbl_buscar_aviso_siniestro tbody').on('click', 'tr', function(event){ // evento click que selecciona el row y marca el check de la tabla		
		
		var otro = "";
		viaAviso = "";
		
		if ($(this).children('td')[8].innerText == 1)
		{
			otro = $(this).children('td')[9].innerText;
		}
		else
		{
			viaAviso = $(this).children('td')[9].innerText;
		}
				
		$("#varIdAvisoSiniestro").val($(this).children('td')[0].innerText);
		$("#txtNumeroAviso").val($(this).children('td')[1].innerText);
		$("#txtNumeroAviso").val($(this).children('td')[1].innerText);
		$("#txtTipoAviso").val($(this).children('td')[2].innerText);
		$("#dtpFechaSiniestro").val($(this).children('td')[3].innerText);
		$("#txtVigenciaConstancia").val($(this).children('td')[4].innerText);
		$("#dtpFechaAviso").val($(this).children('td')[5].innerText);				
		$("#tpHoraAviso").val($(this).children('td')[6].innerText);
		$("#tpHoraSiniestro").val($(this).children('td')[7].innerText);
		$("#txtOtros").val(otro);
		$("#txtViaAviso").val(viaAviso);
		$("#txtQuienAvisa").val($(this).children('td')[10].innerText);
		$("#txtQuienRecibe").val($(this).children('td')[11].innerText);
		$("#txtCausaSiniestro").val($(this).children('td')[12].innerText);
		$("#txtBien").val($(this).children('td')[13].innerText);
		$("#txtConstancia").val($(this).children('td')[14].innerText);
		$("#txtEjercicio").val($(this).children('td')[15].innerText);
		$("#txtNombreAsegurado").val($(this).children('td')[16].innerText);
		$("#varIdConstancia").val($(this).children('td')[17].innerText);
		$(".close").click();
		
		Dajaxice.Siniestro.obtener_bienes_seleccionados_afectados(cargarBienesEnTabla, {'id_aviso':$("#varIdAvisoSiniestro").val(), 'id_constancia':$("#varIdConstancia").val()});
		return false;
	});
}

var cargarBienesEnTabla = function(data){ // Función que nos permite cargar los bienes en la tabla tbl_bienes.
	
	var contenido = $('.tbl_bienes tbody');
	contenido.html('');
	
	if(data.bienesAfectados)
	{
		$.each(data.bienesAfectados, function(i,descripcion)
		{
			$('<tr><td style="display: none;">' + '' + '</td><td style="display: none;">'+descripcion.IdDescripcion+'</td><td><input type="checkbox" name="checkSeleccionar" value="checked" onClick="checkedInputs()" checked readonly/></td><td>'+descripcion.Nombre+'</td><td>'+descripcion.Cantidad+'</td><td>'+descripcion.ValorUnitario+'</td><td>'+descripcion.SumaAsegurada+'</td><td style="text-align:center;"><input type="text" class="input-mini" value="' + descripcion.NoBienesAfectados + '" style="text-align:right;" readonly></td><td style="text-align:center;"><input type="text" class="input-mini" value="' + descripcion.EstadoDanos + '" style="text-align:left;" readonly></td><td style="text-align:center;"><input type="text" class="input-large" value="' + descripcion.ValorUnitario + '" style="text-align:left;" readonly></td></tr>').appendTo(contenido);
		});
	}
}

var buscarTecnicos = function(){ // Función que nos permite buscar los avisos de siniestros terminados mediante la clase ajax.py
	Dajaxice.Siniestro.obtener_tecnicos(cargarDatosATablaTecnico,{'buscar':$("#txtBuscarTecnico").val()});
	return false;
}

var cargarDatosATablaTecnico = function(data){ // Función que nos permite cargar los datos obtenidos de la busqueda de los tecnicos en el modal.
	var contenido = $('.tbl_buscar_tecnico tbody');
	contenido.html('');
	
	if(data.tecnicos != null && data.tecnicos.length > 0)
	{
		tecnicos = data.tecnicos
		for(rowArreglo=0;rowArreglo<tecnicos.length;rowArreglo++)
		{	
			$('<tr><td>'+tecnicos[rowArreglo][0]+'</td><td>'+tecnicos[rowArreglo][1]+'</td><td style="display: none;">'+tecnicos[rowArreglo][2]+'</td></tr>').appendTo(contenido);
		}
	}
	else
	{
		alertify.alert('No se encontraron técnicos para continuar.');
	}
}

var guardarAviso = function(){ // Función que nos permite guardar el aviso del siniestro en la base de datos mediante la función guardar_aviso_siniestro de la clase ajax.py.
	
	if (pasarComprobaciones())
	{
		if ($("#varIdInspeccion").val() == "")
		{
			Dajaxice.Siniestro.guardar_inpeccion(Dajax.process,{'formulario':$('#formulario_inspeccion').serialize(true)});
		}
		else
		{
			alertify.confirm("¿Desea modificar la inspección?", function (e)
			{
			    if (e)
			    {
			    	Dajaxice.Siniestro.guardar_inpeccion(Dajax.process,{'formulario':$('#formulario_inspeccion').serialize(true)});
			    	alertify.success("Inspección Modificada Correctamente");
			    }
			});	
		}
		
		return false;
	}	
}

var pasarComprobaciones = function(){ // Función que nos permite verificar si la información ingresada en el formulario es la correcta.
	
	if ($('#txtTecnico').val() == '')
	{
		alertify.alert("Se requiere técnico para continuar.");
		return false;
	}
	
	return true;
}

var tabla_buscar_tecnicos = function(){ // Función que permite interactuar con la ventana modal de buscar tecnicos.
	$(".modal").on('shown', function(){
	    $("#txtBuscarTecnico").focus();
	});
	
	$('.tbl_buscar_tecnico tbody').on('mouseover', 'tr', function(event){ // toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tbl_buscar_tecnico tbody').on('mouseout', 'tr', function(event){ // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	

	$('.tbl_buscar_tecnico tbody').on('click', 'tr', function(event){ // evento click que selecciona el row y marca el check de la tabla	
		
		$("#txtTecnico").val($(this).children('td')[1].innerText);
		$("#varIdPersonalApoyo").val($(this).children('td')[2].innerText);
		$(".close").click();
	});
}

var mensajeGuardadoInspeccion = function(idInspeccion){ // Función que nos permite mostrar un mensaje cuando la inspección es almacenada en la base de datos.
	$("#varIdInspeccion").val(idInspeccion);
	alertify.alert('Inspección de Siniestro guardada correctamente: ' + idInspeccion);
}