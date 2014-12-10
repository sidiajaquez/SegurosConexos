$(document).on('ready',inicio);

function inicio(){ //Inicio de las funciones
	activarMenu();
	$('#EsSocio').prop('checked', false);
	$("#FechaNacimiento").val(fechaActual());
	
	$("#FechaNacimiento").datepicker({
		firstDay: 1
	});
	
	$("#Guardar").click(guardarPersonaMoral);
	$("#Cancelar").on('click',recargarPagina);	

	$("#btnAgregarSocio").click(limpiarBusquedaSocios);
	$("#btnBuscarPersona").on('click',buscarPersonaMoral);
	$("#BuscarSocio").click(buscarPersonaSocio);	
	generarColumnasTablaBusquedaPersona();	
	tablaBusquedaSociosMoral();
}

function buscarPersonaMoral(){ // Función que llama a buscarPersona de buscadorPersona.js pasandole un indicador de persona moral 'M'.
	buscarPersona('M');
	return false;
}

function generarColumnasTablaBusquedaPersona(){ // Función que genera las columnas de la tabla busquedaPersona cuando el buscador es llamdado de la plantilla moral.html
	var contenido = $('.busquedaPersona thead');
	contenido.html('');	
	$("<tr><th>"+"#"+"</th><th>"+"Razón Social"+"</th><th>"+"Rfc"+"</th></tr>").appendTo(contenido);
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function tablaBusquedaSociosMoral(){ //Funcion que permite interactuar con la ventana modal de busqueda de personas
	$('.busquedaSocios tbody').on('mouseover', 'tr', function(event) { //toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.busquedaSocios tbody').on('mouseout', 'tr', function(event) { //evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});

	$('.busquedaSocios tbody').on('click', 'tr', function(event) { //permite agregar a la tabla de personas principal el registro que se seleccione
		var contenido = $('.sociosPersonaMoral tbody');
		var persona = new Object();
		$(this).children('td').each(function(indice){
			switch(indice){
				case 0:
					persona.id = $(this).text();
					break;
				case 1:
					persona.nombre = $(this).text();
					break;
				case 2:
					persona.apellidoPaterno = $(this).text();
					break;
				case 3:
					persona.apellidoMaterno = $(this).text();
					break;
				case 4:
					persona.rfc = $(this).text();
					break;					
			}
		});
		if (comprobarPersonaDuplicada(persona.id)){
			alertify.alert('La persona ya se encuentra como socio');
		}else{
			$('<tr><td style="display: none;">'+ '' +'</td><td>'+persona.id+'</td><td>'+persona.nombre+"</td><td>"+persona.apellidoPaterno+"</td><td>"+persona.apellidoMaterno+"</td><td>"+persona.rfc+'</td><td><a onclick="eliminarSociosMoralDeTabla($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
			$(".close").click();
		}
	});	
}

function comprobarPersonaDuplicada(idPersona){ // Funcion que comprueba que la persona que se esta agregando no se encuentre repetida, regresa true si ya esta
	var personaRepetida = false;
	$('.sociosPersonaMoral tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 1:
					if ($(this).text() == idPersona){
						personaRepetida = true;
					}
					break;
			}
		});
	});
	return personaRepetida;
}

function guardarPersonaMoral(){ //Función que guarda una persona moral enviando el formulario deserializado a ajax.py en el metodo guardar_persona_moral
	if (pasarComprobaciones())
	{
		var idSocios = [,];
		var direcciones = [];
		
		var indicadorEsSocio = 0;
		
		if($('#EsSocio').is(':checked'))
		{
			indicadorEsSocio = 1;
		}	
		
		if ($("#varIdPersona").val() == '')
		{			
			direcciones = obtieneDatosTabla('.direccionesPeridSocioMoralsonaMoral');
			Dajaxice.ConexosAgropecuarios.guardar_persona_moral(Dajax.process,{'formulario':$('#formulario_persona_moral').serialize(true),'datosSociosMoral':validarArrayVacio(obtencionDatosTablaSociosMoral()),'direcciones':validarArrayVacio(direcciones),'telefonos':validarArrayVacio(obtencionDatosTablaTelefonos()), 'indicadorEsSocio':indicadorEsSocio});
			limpiarFormulario();
		}
		else
		{
			alertify.confirm("¿Desea modificar la persona?", function (e) 
			{
			    if (e) 
			    {
			    	direcciones = obtieneDatosTabla('.direccionesPersonaMoral');
			    	Dajaxice.ConexosAgropecuarios.guardar_persona_moral(Dajax.process,{'formulario':$('#formulario_persona_moral').serialize(true),'datosSociosMoral':validarArrayVacio(obtencionDatosTablaSociosMoral()),'direcciones':validarArrayVacio(direcciones),'telefonos':validarArrayVacio(obtencionDatosTablaTelefonos()), 'indicadorEsSocio':indicadorEsSocio});
			    	alertify.success("Datos Actualizados Correctamente");
			    	$("#PrimerNombre").focus();
			    }
			});
		}		
	}
	else
	{
		alertify.alert('Se requiere ingresar información.');
	}
		
	return false;
}

function obtencionDatosTablaSociosMoral(){ // Función que obtiene un arreglo con la información de la tabla socios moral.
	var arraySociosMoral = [];

	$(".sociosPersonaMoral tr").each(function() {
	    var arrayFilas = [];
	    var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {
	    	fila.each(function()
	    	{
	    		arrayFilas.push($(this).text()); 
	    	});
	    	arraySociosMoral.push(arrayFilas);
	    }
	});
	
	return arraySociosMoral;
}

function limpiarFormulario(){ //Funcion que borra todas las cajas de texto y restaura la fecha a fecha inicial
	var contenido = $('.telefonos_tabla tbody');
	contenido.html('');
	var contenidoDirecciones = $('.direccionesPersonaMoral tbody');
	contenidoDirecciones.html('');
	var contenidoPersonaMoral = $('.sociosPersonaMoral tbody');
	contenidoPersonaMoral.html('');
	$("#varIdPersona").val('');
	document.getElementById("formulario_persona_moral").reset();	
	$('#EsSocio').prop('checked', false);
}

function fechaActual(){ //Obtiene la fecha actual en formato dd/mm/yyyy
	var currentTime = new Date();
	var day = ("0" + currentTime.getDate()).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return (day+'/'+month+'/'+year);
}

function pasarComprobaciones(){ //Comprobaciones del formulario para verificar que no se reciba campos obligatorios en blanco
	validarFormulario();
	if ($('#Rfc').val() == "" || $('#RazonSocial').val() == "" || $('#FechaNacimiento').val() == "")
	{
		return false;
	}
	
	return true;
}

function validarFormulario(){ //se usa el jquery validate para validar los campos mencionados en la funcion
	$('#formulario_persona_moral').validate({
		errorElement: "span",
		rules: {
			Rfc: {
				minlength: 13,
				maxlength: 13,
				required: true
			},
			RazonSocial: {
				required: true
			},
			Email: {
				minlength: 2,
				email: true
			}
		},
		highlight: function(element) {
			$(element).closest('.control-group')
			.removeClass('success').addClass('error');
		},
		success: function(element) {
			element
			.text('OK!').addClass('help-inline')
			.closest('.control-group')
			.removeClass('error').addClass('success');
		}
	});
}

function buscarPersonaSocio(){ //Entra en el click de buscar persona de la ventana modal, utiliza ajax.py para buscar la informacion necesaria de la caja de texto txtBuscar, el callback lo recibe en la funcion personaCallBack
	datosBuscar = $('#txtBuscarSocio').val();
	Dajaxice.ConexosAgropecuarios.buscar_persona_socio(cargarSocios, {'datosBuscar':datosBuscar.toUpperCase()});
	return false;
}

function cargarSocios(data){ //Obtiene la informacion de la busqueda de la persona que recibe del metodo buscar_persona de ajax.py, los datos de la busqueda se agregan a la tabla busquedaPersona de la ventana modal
	var contenido = $('.busquedaSocios tbody');
	contenido.html('');
	if(data.personas){
		$.each(data.personas, function(i,elemento){
			$('<tr><td>'+elemento.IdPersona+'</td><td>'+elemento.Nombre+"</td><td>"+elemento.ApellidoPaterno+"</td><td>"+elemento.ApellidoMaterno+"</td><td>"+elemento.Rfc+"</td></tr>").appendTo(contenido);
		});
	}else{
		alertify.alert('No se encontro información');
	}
}

function limpiarBusquedaSocios(){ //Se llama la funcion cuando se da click en el boton de agregar socio para que borre el contenido de la tabla que vacia el resultado de la busqueda de personas
	$('#txtBuscarSocio').val('');
	$('#buscarSocioModal').on('shown',function(){
		$('#txtBuscarSocio').focus();
	});		
	$('.busquedaSocios tbody').html('');
}

function cargarPersonaMoralEnFormulario(persona){ // Función que obtiene a la persona encontrada y la carga en los controles del formulario.
	$("#Rfc").val(persona.Rfc);
	$("#RazonSocial").val(persona.RazonSocial);	
	$("#FechaNacimiento").val(persona.FechaNacimiento);	
	$("#Email").val(persona.Email);
	$("#varIdPersona").val(persona.IdPersona);
	
	var boolSocio = false;
	if (persona.EsSocio == 1)
	{
		boolSocio = true;
	}
			
	$('#EsSocio').prop('checked', boolSocio);
}

function buscarSocioMoral(idPersona){ // Función que busca la lista de direcciones relacionados con una persona pasando el idpersona.
	Dajaxice.ConexosAgropecuarios.obtener_socios_personamoral_idpersona(cargarTablaSocioMoral, {'idPersona':idPersona});	
	return false;
}

function cargarTablaSocioMoral(data){ // Función que carga las direcciones obtenidos de la función buscarDireccionesConIdPersona en la tabla direccionesPersonaMoral.
	var contenido = $('.sociosPersonaMoral tbody');
	contenido.html('');
	
	if(data.personasSocioMoral)
	{
		$.each(data.personasSocioMoral, function(i,persona)
		{				
			$('<tr><td style="display: none;">'+ persona.IdSocioMoral +'</td><td>'+persona.IdPersona+'</td><td>'+ persona.PrimerNombre + ' ' + persona.SegundoNombre +
					"</td><td>"+persona.ApellidoPaterno+"</td><td>"+persona.ApellidoMaterno+"</td><td>"+persona.Rfc+
					'</td><td><a onclick="eliminarSociosMoralDeTabla($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function eliminarSociosMoralDeTabla(eliminar){ // Función que elimina las filas de la tabla de SociosMorales que se encuentra en la plantilla Moral.html
	alertify.confirm("Esto eliminará el socio de la persona moral, ¿Desea continuar?", function (e) {
	    if (e) {
			eliminar.parent().parent().remove();
			var rowEliminar = eliminar.closest("tr");	
			Dajaxice.ConexosAgropecuarios.eliminar_socioMoral(Dajax.process, {'idSocioMoral':rowEliminar.children('td')[0].innerText});
			alertify.success("El socio fue eliminado correctamente");
	    }
	});	
	return false;		
}

function mensajePersonaMoral(idPersona){ // Función que recibe el id de la persona. 
	alertify.alert('La Persona se Guardado con el IdPersona: '+ idPersona);
}