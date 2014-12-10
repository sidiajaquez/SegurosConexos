$(document).on('ready',inicio);                 

function inicio(){ //Inicio de las funciones
	$("#FechaContrato").datepicker({
		firstDay: 1
	});
	
	$("#VigenciaContrato").on("change",validarCmbVigenciaContrato);
	
	$("#FechaContrato").val(fechaActual());
	$("#btnAgregarContratosModal").click(agregarContratoFondo);
	$("#btnMdlContratosFondoModal").click(borrarInformacionModalContratos);
	
	$(".modal").on('shown', function() {
	    $("#VigenciaContrato").focus();
	});
}

function validarCmbVigenciaContrato(){ // funcion que valida si la vigencia del contrato es anual para que pida el año
	if ($('#VigenciaContrato').val() != 'ANUAL'){
		$('#Ejercicio').val('');
		$('#Ejercicio').prop('disabled',true);
	}else{
		var ano = (new Date).getFullYear();
		$('#Ejercicio').val(ano);
		$('#Ejercicio').prop('disabled',false);
	}
}

function borrarInformacionModalContratos(){ // Función que limpia los textos del formulario.
	$('#VigenciaContrato').val('');
	$('#Ejercicio').val('');
	$('#FechaContrato').val(fechaActual());
	$('#NumeroContrato').val('');
	$('#IdReaseguradora').val('');
}

function agregarContratoFondo(){ // Función que agrega un contrato al fondo a la tabla en el formulario de DatosFondo de la plantilla datosFondo.html
	if (pasarComprobacionesAgregarContratoFondo())
    {
		var contenido = $('.tblcontratosFondo tbody');
		var selectReaseguradora = document.getElementById("IdReaseguradora");
		$('<tr><td style="display: none;">'+''+'</td><td>'+$('#VigenciaContrato').val()+'</td><td>'+$('#Ejercicio').val()+'</td><td>'+$('#FechaContrato').val()+'</td><td>'+$('#NumeroContrato').val().toUpperCase()+'</td><td>'+ selectReaseguradora.options[selectReaseguradora.selectedIndex].text +'</td><td style="display: none;">'+ $('#IdReaseguradora').val() +'</td><td style="display: none;">'+$('#IdContratoReaseguro').val()+'</td><td style="display: none;">'+$('#IdMoneda').val()+'</td><td>'+$('#IdContratoReaseguro option:selected').html()+'</td><td>'+$('#IdMoneda option:selected').html() +'</td><td><a onclick="eliminarContratoFondo($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		$("#VigenciaContrato").val('');
		$("#Ejercicio").val('');
		$("#FechaContrato").val('');
		$("#NumeroContrato").val('');
		$("#IdReaseguradora").val('');
		$("#IdContratoReaseguro").val('');
		$("#IdMoneda").val('');
		$(".close").click();
    }
}

function pasarComprobacionesAgregarContratoFondo(){ // Función que nos permite pasar las comprobaciones que indica si la información ingresada es la requerida.
	
	validarControlesFormulario();
	
	if ($("#VigenciaContrato").val() == '' || $("#FechaContrato").val() == '' || $("#NumeroContrato").val() == '' || $("#IdReaseguradora").val() == '' || $("#IdContratoReaseguro").val() == '' || $("#IdMoneda").val() == '' ||($("#VigenciaContrato").val() == "ANUAL" && $("#Ejercicio").val() == ''))
	{
		alertify.alert('Se requiere ingresar información para continuar');
		return false;
	}
	
	if (isNaN($("#Ejercicio").val()))
	{
		alertify.alert('Se requiere ingresar año en el ejercicio');
		return false;
	}
	
	if (($("#Ejercicio").val()<((new Date).getFullYear()) && ($("#VigenciaContrato").val() == "ANUAL"))){
		alertify.alert('El ejercicio no puede ser menor al año actual');
		return false;		
	}
	
	return true;
}

function obtencionDatosTablaContratoFondo(){ // Función que obtiene la información de la tabla contratosFondo y la agrega a un arreglo.
	var arrayContratoFondo = [];

	$(".tblcontratosFondo tr").each(function() {
	    var arrayFilas = [];
	    var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {
	    	fila.each(function()
	    	{
	    		arrayFilas.push($(this).text()); 
	    	});
	    	arrayContratoFondo.push(arrayFilas);
	    }
	});
	
	return arrayContratoFondo;
}

function buscarContratosFondo(idDatosFondo){ // Función que busca los contratos del fondo.
	Dajaxice.ConexosAgropecuarios.obtener_contratos_fondo(cargarTablaContratoFondo, {'idDatosFondo':idDatosFondo});	
}

function cargarTablaContratoFondo(dato){ // Función que nos permite cargar en la tabla de tblcontratosFondo de la plantilla DatosFondo.html.
	var contenido = $('.tblcontratosFondo tbody');
	contenido.html('');
	
	if(dato.contratos)
	{
		$.each(dato.contratos, function(i,elemento)
		{
			linkEliminarContrato = '';
			if (!(elemento.ContratoUtilizado)){
				linkEliminarContrato = '<a onclick="eliminarContratoFondo($(this));" href="#"><i class="icon-remove"></i></a>';
			}
			$('<tr><td style="display: none;">'+ elemento.IdContratoFondo +'</td><td>'+elemento.VigenciaContrato+'</td><td>'+elemento.Ejercicio+'</td><td>'+elemento.FechaContrato+'</td><td>'+elemento.NumeroContrato+'</td><td>'+elemento.Reaseguradora+'</td><td style="display: none;">'+ '' +'</td><td style="display: none;">'+ '' +'</td><td style="display: none;">'+ '' +'</td><td>'+elemento.ContratoReaseguro+'</td><td>'+elemento.Moneda+'</td><td>'+linkEliminarContrato+'</td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function eliminarContratoFondo(eliminar){ // Función que elimina las filas de la tabla de contratosFondo que se encuentra en la plantilla datosFondo.html
	alertify.confirm("Esto eliminará el contrato, ¿Desea continuar?", function (e) {
	    if (e) {
			eliminar.parent().parent().remove();
			var rowEliminar = eliminar.closest("tr");	
			Dajaxice.ConexosAgropecuarios.eliminar_contratos_fondo(Dajax.process, {'idContratoFondo':rowEliminar.children('td')[0].innerText});
			alertify.success("El contrato fue eliminado correctamente");
	    }
	});	
	return false;	
}


