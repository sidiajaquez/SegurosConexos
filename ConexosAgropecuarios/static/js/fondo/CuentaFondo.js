$(document).on('ready',inicio);                 

function inicio(){ //Inicio de las funciones
	$("#btnAgregarCuentaFondoModal").click(agregarCuentaFondo);
	$("#btnMdlAgregarCuentasFondoModal").click(borrarInformacionModalCuentasFondo);
	
	$(".modal").on('shown', function() {
	    $("#TipoCuenta").focus();
	});
	
}

function borrarInformacionModalCuentasFondo(){ // Función que limpia los textos del formulario.
	$('#TipoCuenta').val('');
	$('#IdBanco').val('');
	$('#NumeroCuenta').val('');
	$('#Clave').val('');
}

function agregarCuentaFondo(){ // Función que agrega una cuenta bancaria al fondo a la tabla en el formulario de DatosFondo de la plantilla datosFondo.html
	if (pasarComprobacionesAgregarCuentaBancariaFondo())
    {
		var contenido = $('.cuentasBancariasFondoTabla tbody');
		var selectBanco = document.getElementById("IdBanco");
		$('<tr><td style="display: none;">'+''+'</td><td>'+$('#TipoCuenta').val()+'</td><td>'+ selectBanco.options[selectBanco.selectedIndex].text +'</td><td>'+$('#NumeroCuenta').val()+'</td><td>'+$('#Clave').val()+'</td><td style="display: none;">'+ $('#IdBanco').val() +'</td><td><a onclick="eliminarCuentaBancariaFondo($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		$("#TipoCuenta").val('');
		$("#IdBanco").val('');
		$("#NumeroCuenta").val('');
		$("#Clave").val('');
		$(".close").click();
    }
	else
	{
		alertify.alert('Se requiere ingresar información a la cuenta bancaria para continuar');
	}
}

function pasarComprobacionesAgregarCuentaBancariaFondo(){ // Función que nos permite pasar las comprobaciones que nos indica si la información ingresada es la requerida.
	
	if ($("#TipoCuenta").val() == '' || $("#IdBanco").val() == '' || $("#NumeroCuenta").val() == '' || $("#Clave").val() == '')
	{
		return false;
	}
	
	return true;
}

function obtencionDatosTablaCuentaFondo(){ // Función que obtiene la información de la tabla cuentasBancariasFondoTabla y la agrega a un arreglo.
	var arrayCuentaFondo = [];

	$(".cuentasBancariasFondoTabla tr").each(function() {
	    var arrayFilas = [];
	    var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {
	    	fila.each(function()
	    	{
	    		arrayFilas.push($(this).text()); 
	    	});
	    	arrayCuentaFondo.push(arrayFilas);
	    }
	});
	
	return arrayCuentaFondo;
}

function buscarCuentasBancariasFondo(idDatosFondo){ // Función que busca las cuentas bancarias del fondo.
	Dajaxice.ConexosAgropecuarios.obtener_cuentasbancarias_datosfondo(cargarTablaCuentasBancariasFondo, {'idDatosFondo':idDatosFondo});	
}

function cargarTablaCuentasBancariasFondo(dato){ // Función que nos permite cargar en la tabla de cuentasBancariasFondoTabla de la plantilla DatosFondo.html.
	var contenido = $('.cuentasBancariasFondoTabla tbody');
	contenido.html('');
	
	if(dato.cuentas)
	{
		$.each(dato.cuentas, function(i,elemento)
		{
			
			linkEliminarCuenta = '';
			if (!(elemento.ContratoReaseguroUtilizado)){
				linkEliminarCuenta = '<a onclick="eliminarCuentaBancariaFondo($(this));" href="#"><i class="icon-remove"></i></a>';
			}			
			
			$('<tr><td style="display: none;">'+elemento.IdCuentaFondo+'</td><td>'+elemento.TipoCuenta+'</td><td>'+elemento.Descripcion+'</td><td>'+elemento.NumeroCuenta+'</td><td>'+elemento.Clave+'</td><td style="display: none;">'+ '' +'</td><td>'+linkEliminarCuenta+'</td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function eliminarCuentaBancariaFondo(eliminar){ // Función que elimina las filas de la tabla de cuentas bancarias que se encuentra en la plantilla datosFondo.html
	alertify.confirm("Esto eliminará la cuenta bancaria, ¿Desea continuar?", function (e) {
	    if (e) {
			eliminar.parent().parent().remove();
			var rowEliminar = eliminar.closest("tr");	
			Dajaxice.ConexosAgropecuarios.eliminar_cuentabancaria_datosFondo(Dajax.process, {'idCuentaFondo':rowEliminar.children('td')[0].innerText});
			alertify.success("La cuenta bancaria fue eliminada correctamente");
	    }
	});	
	return false;
}