$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario telefonos.
	$("#Numero").mask("(999) 999-9999");	
	$("#btnAgregarTelefono").on('click',agregarTelefono);
}

function agregarTelefono(){ // Función que agrega un teléfono a la tabla en el formulario de telefonos de la plantilla fisica.html
	if (pasarComprobacionesAgregarTelefono())
    {
		var contenido = $('.telefonos_tabla tbody');
		$('<tr><td style="display: none;">'+''+'</td><td>'+$('#TipoTelefono').val()+'</td><td>'+$('#Numero').val()+'</td><td><a onclick="eliminarTelefonosDeTabla($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		$("#TipoTelefono").val('');
		$("#Numero").val('');
		$(".close").click()
    }
	else
	{
		$(document).on('ready',inicio);

		function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario telefonos.
			$("#Numero").mask("(999) 999-9999");	
			$("#btnAgregarTelefono").on('click',agregarTelefono);
		}
		alertify.alert('Se requiere ingresar la información de teléfonos para continuar.');
	}
}

function pasarComprobacionesAgregarTelefono(){ // Función que valida la información para agregar teléfonos.
	if (($('#TipoTelefono').val() != '' && $('#Numero').val() != ''))
	{
		return true;
	}	
	
	return false;
}

function eliminarTelefonosDeTabla(eliminar){ // Función que elimina las filas de la tabla de telefonos que se encuentra en la plantilla telefonos.html
	alertify.confirm("Esto eliminará el teléfono, ¿Desea continuar?", function (e) {
	    if (e) {
			eliminar.parent().parent().remove();
			var rowEliminar = eliminar.closest("tr");	
			Dajaxice.ConexosAgropecuarios.eliminar_Telefono(Dajax.process, {'idTelefono':rowEliminar.children('td')[0].innerText});
			alertify.success("El teléfono fue eliminado correctamente");
	    }
	});	
	return false;	
}

function buscarTelefonosConIdPersona(idPersona){ // Función que busca la lista de teléfonos relacionados con una persona pasando el idpersona.
	Dajaxice.ConexosAgropecuarios.obtener_Telefonos_Persona(cargarTablaTelefonos, {'idPersona':idPersona});
	return false;
}

function cargarTablaTelefonos(dato){ // Función que carga los teléfonos obtenidos de la función buscarTelefonosConIdPersona en la tabla telefonos_tabla que se encuentra en la plantilla telefonos.html
	var contenido = $('.telefonos_tabla tbody');
	contenido.html('');
	
	if(dato.telefonos)
	{
		$.each(dato.telefonos, function(i,elemento)
		{
			$('<tr><td style="display: none;">'+elemento.IdTelefono+'</td><td>'+elemento.TipoTelefono+'</td><td>'+elemento.Numero+'</td><td><a onclick="eliminarTelefonosDeTabla($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function obtencionDatosTablaTelefonos(){ // Función que obtiene la información de la tabla telefonos y la agrega a un arreglo.
	var arrayTelefonos = [];

	$(".telefonos_tabla tr").each(function() {
	    var arrayFilas = [];
	    var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {
	    	fila.each(function()
	    	{
	    		arrayFilas.push($(this).text()); 
	    	});
	        arrayTelefonos.push(arrayFilas);
	    }
	});
	
	return arrayTelefonos;
}