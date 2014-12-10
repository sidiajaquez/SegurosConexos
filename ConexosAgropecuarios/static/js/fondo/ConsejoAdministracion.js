$(document).on('ready',inicio);                 

function inicio(){ //Inicio de las funciones
	$("#FechaEleccion").datepicker({
		firstDay: 1
	});
	
	$("#btnBuscarPersonaFisicaFondoMoral").click(buscarPersonaFisicaFondo);
	$("#btnCerrarMdlBuscarPersonaConsejoFondo").on('click',cerrarModalBuscarPersonaMiembroConsejo);	
	$("#btnAgregarMiembroConsejoModal").click(agregarMiembroAlConsejoAdministrador);		
	$("#btnMdlConsejoAdministracionFondoModal").click(limpiarModalConsejoAdministracionFondo);		
	$("#btnMdlBuscarPersonaConsejoModal").click(limpiarBuscadorPersonaConsejo);
	
	document.getElementById("txtNombrePersonaFisicaFondo").readOnly = true;

	tablaBusquedaPersonaFondo();
}

function limpiarBuscadorPersonaConsejo(){ // Función que nos permite limpiar el buscador de la persona que sera integrante del consejo.
	$("#txtBuscarPersonaFisicaConsejoFondoModal").val('');
	var contenido = $('.tblPersonaMiembroConsejoFondo tbody');
	contenido.html('');	
}

function agregarMiembroAlConsejoAdministrador(){ // Función que agrega un miembro del consejo de administrativo.
	if (pasarComprobacionesAgregarMiembroConsejoAdministracion())
    {
		var contenido = $('.tblConsejoAdministracionFondo tbody');
		registroDuplicado = comprobarDireccionDuplicada($('#varIdPersona').val(),$('#Cargo').val());
		if ((registroDuplicado.personaRepetida) || (registroDuplicado.puestoRepetido)){
			if (registroDuplicado.personaRepetida){
				alertify.alert('La persona ya se encuentra en el Consejo de Administración');
			}
			if (registroDuplicado.puestoRepetido){
				alertify.alert('El cargo ya se encuentra en el Consejo de Administración');
			}
		}else{
			$('<tr><td style="display: none;">'+''+'</td><td>'+$('#Cargo').val()+'</td><td>'+$('#txtNombrePersonaFisicaFondo').val()+'</td><td></td><td>'+$('#FechaEleccion').val()+'</td><td>'+$('#Duracion').val()+'</td><td style="display: none;">'+$('#varIdPersona').val()+'</td><td><a onclick="eliminarMiembroConsejoAdministracionFondo($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
			$(".close").click();
		}
    }
}

function comprobarDireccionDuplicada(idPersona,cargoConsejo){ // Funcion que comprueba que la persona que se esta agregando no se encuentre repetida, regresa true si ya esta
	var registroRepetido = new Object();
	registroRepetido.personaRepetida = false;
	registroRepetido.puestoRepetido = false;
	$('.tblConsejoAdministracionFondo tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 1:
					if (($(this).text() == cargoConsejo) && ($(this).text()!="VOCAL")){
						registroRepetido.puestoRepetido = true;
					}
				break;			
				case 6:
					if ($(this).text() == idPersona){
						registroRepetido.personaRepetida = true;
					}
					break;			
			}
		});
	});
	return registroRepetido;
}


function pasarComprobacionesAgregarMiembroConsejoAdministracion(){ // Función que valida la información para agregar miembros al consejo de administración.
	
	if ($('#txtNombrePersonaFisicaFondo').val() == '' || $('#Cargo').val() == '' || $('#FechaEleccion').val() == ''
		|| $('#Duracion').val() == '')
	{
		alertify.alert('Se requiere ingresar la información de miembro consejo para continuar.');
		return false;
	}	
	
	if (isNaN($("#Duracion").val()))
	{
		alertify.alert('Se requiere ingresar solo números en duración para continuar.');
		return false;
	}
	
	return true;
}

function eliminarMiembroConsejoAdministracionFondo(eliminar){ // Función que elimina la fila a un miembro del consejo de administración.
	alertify.confirm("Esto eliminará el miembro del consejo de administración, ¿Desea continuar?", function (e) {
	    if (e) {
			eliminar.parent().parent().remove();
			var rowEliminar = eliminar.closest("tr");	
			Dajaxice.ConexosAgropecuarios.eliminar_consejoAdministracion_fondo(Dajax.process, {'idConsejoAdministracion':rowEliminar.children('td')[0].innerText});
			alertify.success("La persona fue eliminada correctamente");
	    }
	});	
	return false;
}

function limpiarModalConsejoAdministracionFondo(){ // Función que limpia los controles del modal consejo de administración.
	$("#txtNombrePersonaFisicaFondo").val('');
	$("#Cargo").val('');
	$("#FechaEleccion").val(fechaActual());
	$("#Duracion").val('');
	$("#Numero").val('');
}

function cerrarModalBuscarPersonaMiembroConsejo(){ // Función que cierra el modal para buscar personas para agregarlas como miembros de consejo.
	$('#mdlBuscarPersonaConsejoFondo').modal('hide')
}

function buscarPersonaFisicaFondo(){ // Función que busca a la persona fisica del fondo.
		datosBuscar = $('#txtBuscarPersonaFisicaConsejoFondoModal').val();
		Dajaxice.BuscadorPersonas.buscar_persona(cargarPersonaMiembroConsjeo, {'datosBuscar':datosBuscar.toUpperCase(), 'tipoPersona':'F'});
		return false;
}

function cargarPersonaMiembroConsjeo(data){ // Obtiene la información de la busqueda de la persona que recibe del método buscar_persona de ajax.py, los datos de la busqueda se agregan a la tabla busquedaPersona de la ventana modal.
	var contenido = $('.tblPersonaMiembroConsejoFondo tbody');
	contenido.html('');	
	
	if(data.personas)
	{
		$.each(data.personas, function(i,elemento)
		{		
			var nombreCompleto = elemento.Nombre +" "+ elemento.ApellidoPaterno +" "+ elemento.ApellidoMaterno;
			$('<tr><td>'+elemento.IdPersona+'</td><td>' + nombreCompleto +"</td><td>"+elemento.Rfc+"</td></tr>").appendTo(contenido);		
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function tablaBusquedaPersonaFondo(){ // Función que permite interactuar con la ventana modal de busqueda de personas.
	$(".modal").on('shown', function() {
	    $("#txtBuscarPersonaFisicaConsejoFondoModal").focus();
	});
	
	$('.tblPersonaMiembroConsejoFondo tbody').on('mouseover', 'tr', function(event) { // Toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tblPersonaMiembroConsejoFondo tbody').on('mouseout', 'tr', function(event) { // Evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});

	var idPersona;
	
	$('.tblPersonaMiembroConsejoFondo tbody').on('click', 'tr', function(event) { // Permite agregar a la tabla de personas principal el registro que se seleccione.		
		idPersona = $(this).children('td')[0].innerText;
		$('#txtNombrePersonaFisicaFondo').val($(this).children('td')[1].innerText);
		$('#varIdPersona').val(idPersona)
		cerrarModalBuscarPersonaMiembroConsejo();	
	});	
}

function obtencionDatosTablaMiembrosFondo(){ // Función que obtiene la información de la tabla miembrosFondo y la agrega a un arreglo.
	var arrayMiembrosFondo = [];

	$(".tblConsejoAdministracionFondo tr").each(function() {
	    var arrayFilas = [];
	    var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {
	    	fila.each(function()
	    	{
	    		arrayFilas.push($(this).text()); 
	    	});
	    	arrayMiembrosFondo.push(arrayFilas);
	    }
	});
	
	return arrayMiembrosFondo;
}

function buscarMiembrosConsejoFondo(){ // Función que busca los miembros de administracion del fondo.
	Dajaxice.ConexosAgropecuarios.obtener_consejoAdministracion_fondo(cargarTablaMiembrosConsejoFondo);	
}

function cargarTablaMiembrosConsejoFondo(dato){ // Función que carga los miembros del consejo de administración.
	var contenido = $('.tblConsejoAdministracionFondo tbody');
	contenido.html('');
	
	if(dato.miembrosConsejo)
	{
		$.each(dato.miembrosConsejo, function(i,elemento)
		{
			$('<tr><td style="display: none;">'+elemento.IdConsejoAdministracion+'</td><td>'+elemento.Cargo+'</td><td>'+elemento.Nombre+'</td><td></td><td>'+elemento.FechaEleccion+'</td><td>'+elemento.Duracion+'</td><td style="display: none;">'+elemento.IdPersona+'</td><td><a onclick="eliminarMiembroConsejoAdministracionFondo($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		});
	}
}