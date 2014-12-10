$(document).on('ready',inicio);                 

function inicio(){ //Inicio de las funciones
	
	$("#btnCerrarMdlBuscarPersonaApoyoFondo").on('click',cerrarModalBuscarPersonaApoyoFondo);
	$("#btnBuscarPersonaApoyoFondoMoral").click(buscarPersonaApoyoFondo); 
	$("#btnAgregarPersonaloApoyoModal").click(agregarPersonalApoyoFondo);
	$("#btnMdlAgregarPersonalApoyo").click(borrarInformacionModalPersonalApoyo);
	$("#btnMdlBuscarPersonaApoyoModal").click(limpiarBuscadorPersonalApoyo);
	document.getElementById("txtNombrePersonaApoyoFondo").readOnly = true;

	tablaBusquedaPersonaApoyoFondo();
}

function limpiarBuscadorPersonalApoyo(){ // Función que nos permite limpiar el buscador del personal de apoyo del fondo.
	$("#txtBuscarPersonaFisicaApoyoModal").val('');
	var contenido = $('.tblPersonaMiembroApoyoFondo tbody');
	contenido.html('');	
}

function agregarPersonalApoyoFondo(){ // Función que agrega una persona de apoyo para el fondo.
	if (pasarComprobacionesAgregarPersonalApoyoFondo())
    {
		var contenido = $('.tblPersonaApoyoModal tbody');
		registroDuplicado = comprobarDuplicado($('#CargoPersonaApoyo').val());
		if (registroDuplicado.puestoRepetido){
			alertify.alert('Ya se cuenta con un Gerente para el Fondo');
		}else{
			$('<tr><td style="display: none;">'+''+'</td><td>'+$('#txtNombrePersonaApoyoFondo').val()+'</td><td>'+$('#CargoPersonaApoyo').val()+'</td><td style="display: none;">'+$('#varIdPersonaApoyo').val()+'</td><td><a onclick="eliminarPersonalApoyoFondo($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
			$(".close").click();
		}
    }
	else
	{
		alertify.alert('Se requiere ingresar la información para el personal de apoyo del Fondo');
	}
}

function comprobarDuplicado(cargoPersonaApoyo){ // Funcion que valida si el puesto de Gerente ya se encuentra repetido en el personal de apoyo del fondo
	var registroRepetido = new Object();
	registroRepetido.puestoRepetido = false;
	$('.tblPersonaApoyoModal tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 2:
					if (($(this).text() == cargoPersonaApoyo) && ($(this).text()=="GERENTE")){
						registroRepetido.puestoRepetido = true;
					}
				break;			
			}
		});
	});
	return registroRepetido;	
}

function borrarInformacionModalPersonalApoyo(){ // Función que limpia los textos del formulario.
	$('#txtNombrePersonaApoyoFondo').val('');
	$('#CargoPersonaApoyo').val('');
}

function eliminarPersonalApoyoFondo(eliminar){ // Función que elimina las filas de la tabla de personal de apoyo que se encuentra en la plantilla datosFondo.html
	alertify.confirm("Esto eliminará a la persona de apoyo del Fondo, ¿Desea continuar?", function (e) {
	    if (e) {
			eliminar.parent().parent().remove();
			var rowEliminar = eliminar.closest("tr");	
			Dajaxice.ConexosAgropecuarios.eliminar_personalApoyo_fondo(Dajax.process, {'idPersonalApoyo':rowEliminar.children('td')[0].innerText});
			alertify.success("La persona fue eliminada correctamente");
	    }
	});	
	return false;	
}

function pasarComprobacionesAgregarPersonalApoyoFondo(){ // Función que valida la información para agregar al personal de apoyo del fondo.
	if ($('#txtNombrePersonaApoyoFondo').val() != '' && $('#CargoPersonaApoyo').val() != '')
	{
		return true;
	}	
	
	return false;
}

function cerrarModalBuscarPersonaApoyoFondo(){ // Función que cierra el modal para buscar personal de apoyo del fondo.
	$('#mdlBuscarPersonaApoyoFondo').modal('hide');
}

function buscarPersonaApoyoFondo(){ // Función que manda a llamar al método buscar_personas para filtrar lo que se encuentra en el txt.
	datosBuscar = $('#txtBuscarPersonaFisicaApoyoModal').val();
	Dajaxice.BuscadorPersonas.buscar_todas_personas(cargarPersonaApoyoFondo, {'datosBuscar':datosBuscar.toUpperCase(),'esSocio':'0'});
	return false;
}

function cargarPersonaApoyoFondo(data){ // Obtiene la información de la busqueda de la persona que recibe del método buscar_persona de ajax.py, los datos de la busqueda se agregan a la tabla busquedaPersona de la ventana modal.
var contenido = $('.tblPersonaMiembroApoyoFondo tbody');
contenido.html('');	

	if(data.personas)
	{
		$.each(data.personas, function(i,elemento)
		{
			nombreCompleto = arreglarNombreMoralFisica(elemento);
			$('<tr><td>'+elemento.IdPersona+'</td><td>' + nombreCompleto +"</td><td>"+elemento.Rfc+"</td></tr>").appendTo(contenido);		
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function tablaBusquedaPersonaApoyoFondo(){ // Función que permite interactuar con la ventana modal de busqueda de personas.
	$(".modal").on('shown', function() {
	    $("#txtBuscarPersonaFisicaApoyoModal").focus();
	});
	
	$('.tblPersonaMiembroApoyoFondo tbody').on('mouseover', 'tr', function(event) { // Toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tblPersonaMiembroApoyoFondo tbody').on('mouseout', 'tr', function(event) { // Evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});

	var idPersona;
	
	$('.tblPersonaMiembroApoyoFondo tbody').on('click', 'tr', function(event) { // Permite agregar a la tabla de personas principal el registro que se seleccione.		
		idPersona = $(this).children('td')[0].innerText;
		$('#txtNombrePersonaApoyoFondo').val($(this).children('td')[1].innerText);
		$('#varIdPersonaApoyo').val(idPersona)
		cerrarModalBuscarPersonaApoyoFondo();		
	});	
}

function obtencionDatosTablaPersonalApoyoFondo(){ // Función que obtiene la información de la tabla personalApoyo y la agrega a un arreglo.
	var arrayPersonalApoyo = [];

	$(".tblPersonaApoyoModal tr").each(function() {
	    var arrayFilas = [];
	    var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {
	    	fila.each(function()
	    	{
	    		arrayFilas.push($(this).text()); 
	    	});
	    	arrayPersonalApoyo.push(arrayFilas);
	    }
	});
	
	return arrayPersonalApoyo;
}

function buscarPersonalApoyoFondo(){ // Función que busca al personal de apoyo del fondo.
	Dajaxice.ConexosAgropecuarios.obtener_personalApoyo_fondo(cargarTablaPersonalApoyoFondo);	
}

function cargarTablaPersonalApoyoFondo(dato){ // Función que carga el personal de apoyo.
	var contenido = $('.tblPersonaApoyoModal tbody');
	contenido.html('');
	
	if(dato.personasApoyo)
	{
		$.each(dato.personasApoyo, function(i,elemento)
		{
			nombreCompleto = arreglarNombreMoralFisica(elemento);
			$('<tr><td style="display: none;">'+elemento.IdPersonalApoyo+'</td><td>'+nombreCompleto+'</td><td>'+elemento.CargoPersonaApoyo+'</td><td style="display: none;">'+elemento.Persona_id+'</td><td><a onclick="eliminarPersonalApoyoFondo($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		});
	}
}

function arreglarNombreMoralFisica(nombreCompletoMoralFisica){ // Funcion que concatena en una variable el nombre dependiendo si es fisica o moral
	var nombreCompleto='';
	// Se hacen validaciones de null para que no se adjunte la palabra null en la variable nombreCompleto
	if (nombreCompletoMoralFisica.PrimerNombre != null){
		nombreCompleto = nombreCompletoMoralFisica.PrimerNombre;
	}
	if (nombreCompletoMoralFisica.SegundoNombre != null){
		nombreCompleto = nombreCompleto + ' ' + nombreCompletoMoralFisica.SegundoNombre;
	}
	if (nombreCompletoMoralFisica.RazonSocial != null){
		nombreCompleto = nombreCompleto + ' ' + nombreCompletoMoralFisica.RazonSocial;
	}
	if (nombreCompletoMoralFisica.ApellidoPaterno != null){
		nombreCompleto = nombreCompleto + ' ' + nombreCompletoMoralFisica.ApellidoPaterno;
	}
	if (nombreCompletoMoralFisica.ApellidoMaterno != null){
		nombreCompleto = nombreCompleto + ' ' + nombreCompletoMoralFisica.ApellidoMaterno;
	}
	return nombreCompleto;
}