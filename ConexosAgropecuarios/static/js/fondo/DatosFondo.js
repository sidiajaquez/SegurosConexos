$(document).on('ready',inicio);                 

function inicio(){ //Inicio de las funciones
	activarMenu();
	buscarEstados();
	tablaBusquedaFondos();
	
	$("#chkSeleccionarTodosMunicipios").on("click",seleccionarTodosMunicipios);
	
	$("#Telefono").mask("(999) 999-9999");
	
	$("#btnGuardarDatosFondo").click(guardar_datos_fondo);
	$("#btnCancelarDatosFondo").click(limpiar_formulario);
	
	$("#FechaEscritura").val(fechaActual());
	$("#FechaRegistro").val(fechaActual());
	$("#FechaRppc").val(fechaActual());
	$("#btnAgregarMunicipioDatosFondo").on("click",agregarMuncipioDatosFondo);
	
	$("#FechaEscritura").datepicker({
		firstDay: 1
	});	
	$("#FechaRegistro").datepicker({
		firstDay: 1
	});	
	$("#FechaRppc").datepicker({
		firstDay: 1
	});
	
	buscarDatosFondo();
	$("#btnBuscarInformacionFondo").on('click',buscarInformacionFondo);
	$("#btnAgregarInformacionFondo").on('click',limpiarModalBuscarInformacionFondo);
	
	$(".modal").on('shown', function() {
	    $("#txtMunicipioDatosFondo").focus();
	});
	
	//Configuracion de los chosen
	$(".chosen-select-deselect").chosen({allow_single_deselect:true,no_results_text:'No se encontro'});
	$(".chosen-select").chosen();
	$(".chosen-select-deselect").chosen().change(function(evt,params){
		$("#chkSeleccionarTodosMunicipios").prop('disabled',false);
		$("#chkSeleccionarTodosMunicipios").prop('checked',false);
		$("#cmbMunicipios").html("");
		if (!params){
			$("#chkSeleccionarTodosMunicipios").prop('disabled',true);
			//Limpiar caja de texto cuando no exista nada
			$(".chosen-select").val('').trigger('chosen:updated');
		}else{
			cargarCmbMunicipios(params.selected-1);
		}
	});
}

function tablaBusquedaFondos(){ //Función que permite interactuar con la ventana modal de busqueda de fondos o personas morales.
	$('.busquedaFondos tbody').on('mouseover', 'tr', function(event) { //toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});
	
	$('.busquedaFondos tbody').on('mouseout', 'tr', function(event) { //evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});
	
	$('.busquedaFondos tbody').on('click', 'tr', function(event) { // permite agregar los datos de la persona moral al formulario de los datos del fondo		
		idPersona = $(this).children('td')[0].innerText;
		buscarPersonaConIdPersona(idPersona);
		$(".close").click();
	});		
}

function buscarPersonaConIdPersona(idPersona){ // Función que busca a una persona mediante el idpersona.
	Dajaxice.BuscadorPersonas.obtener_Persona_IdPersona(cargarFormularioInformacionFondo, {'idPersona':idPersona});
	buscarTelefonosConIdPersona(idPersona);
	buscarDireccionesConIdPersona(idPersona);
	return false;
}

function buscarDireccionesConIdPersona(idPersona){ // Función que busca la lista de direcciones relacionados con una persona pasando el idpersona, se obtiene la direccion del trabajo
	Dajaxice.Direcciones.buscar_direcciones_idsepomex(cargarFormularioDirecciones, {'idPersona':idPersona});	
	return false;
}

function cargarFormularioDirecciones(datos){ // Función que carga las direcciones obtenidos de la función buscarDireccionesConIdPersona en el formulario datos del fondo
	if(datos.direcciones)
	{
		$("#Domicilio").val('');
		$.each(datos.direcciones, function(i,direccion)
		{
			$("#Domicilio").val(direccion.Calle+direccion.NumeroExterior+direccion.NumeroInterior);
			if(direccion.TipoDireccion = 2)
			{
				$("#Domicilio").val(direccion.Calle+direccion.NumeroExterior+direccion.NumeroInterior);
				return false;
			}
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}	
}

function cargarFormularioInformacionFondo(datos){ // Función que manda a cargar la información encontrada en buscarPersonaConIdPersona, y se muestra en las cajas de texto de datos del fondo
	if(datos.personas)
	{
		var persona = datos.personas[0];
		$("#NombreFondo").val(persona.RazonSocial);
		$("#Email").val(persona.Email);
		$("#Rfc").val(persona.Rfc);
		$("#IdPersonaDatosFondo").val(persona.IdPersona);
	}
	else
	{
		alertify.alert('No se encontro información del fondo');
	}	
	
}

function buscarTelefonosConIdPersona(idPersona){ // Función que busca la lista de teléfonos relacionados con una persona pasando el idpersona.
	Dajaxice.ConexosAgropecuarios.obtener_Telefonos_Persona(cargarFormularioTelefonos, {'idPersona':idPersona});
	return false;
}

function cargarFormularioTelefonos(datos){ // Función que carga el telegono de trabajo en el formulario de datos del fondo, si no lo encuentra carga cualquier otro
	if(datos.telefonos)
	{
		$("#Telefono").val('');
		$.each(datos.telefonos, function(i,elemento)
		{
			$("#Telefono").val(elemento.Numero);
			if (elemento.TipoTelefono=="TRABAJO"){
				$("#Telefono").val(elemento.Numero);
				return false;
			}
		});
	}
	else
	{
		alertify.alert('No se encontraron Teléfonos');
	}	
}

function buscarInformacionFondo(){ // Busca la personas morales para agregarlas como datos del fondo
	datosBuscar = $('#txtBuscarFondo').val();	
	tipoPersona = 'M';
	Dajaxice.BuscadorPersonas.buscar_persona(informacionFondoCallBack, {'datosBuscar':datosBuscar.toUpperCase(), 'tipoPersona':tipoPersona});
	return false;
}

function informacionFondoCallBack(data){ // Obtiene la informacion de la busqueda de la informacion del fondo que recibe del método buscar_persona de ajax.py, los datos de la busqueda se agregan a la tabla busquedaFondos de la ventana modal.
	var contenido = $('.busquedaFondos tbody');
	contenido.html('');	
	
	if(data.personas)
	{
		$.each(data.personas, function(i,elemento)
		{
			$('<tr><td>'+elemento.IdPersona+'</td><td>'+elemento.RazonSocial+"</td><td>"+elemento.Rfc+"</td></tr>").appendTo(contenido);			
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function limpiarModalBuscarInformacionFondo(){ //Se limpia la ventana modal de buscar informacion fondo al dar click en el boton btnAgregarInformacionFondo
	$("#txtBuscarFondo").val('');
	var contenido = $('.busquedaFondos tbody');
	contenido.html('');
	$("#agregarInformacionFondo").on('shown', function() {
	    $("#txtBuscarFondo").focus();
	});	
}

function cargarCmbMunicipios(idEstado){ //Carga los municipios en el cmbMunicipo dependiendo del estado
	Dajaxice.ConexosAgropecuarios.cargar_Combo_Municipios(callbackMunicipios,{'valor':idEstado});
}

var callbackMunicipios = function(data){
	data.Municipios.forEach(function (municipio, valor){
		$('#cmbMunicipios').append("<option value='"+municipio.IdMunicipio+"'>"+municipio.DescripcionMunicipio+"</option>");
	});
	$(".chosen-select").trigger('chosen:updated');
}

function buscarEstados(){ //Funcion que busca los estados para agregarlos al combo
	Dajaxice.ConexosAgropecuarios.cargar_Combo_Estados(Dajax.process);	
}

function fechaActual(){ // Función que genera y devuelve la fecha de hoy.
	var currentTime = new Date();
	var day = ("0" + currentTime.getDate()).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return (day+'/'+month+'/'+year);
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function guardar_datos_fondo(){	// Función que guarda la información de los datos generales del fondo.
	if (pasarComprobacionesDatosFondo())
	{
		Dajaxice.ConexosAgropecuarios.guardar_datos_fondo(Dajax.process,{'formularioFondo':$('#formulario_datos_fondo').serialize(true), 'municipiosDatosFondo': validarArrayVacio(obtencionDatosTablaMunicipioDatosFondo()), 'cuentasFondo': validarArrayVacio(obtencionDatosTablaCuentaFondo()), 'contratosFondo': validarArrayVacio(obtencionDatosTablaContratoFondo()), 'miembrosConsejoFondo': validarArrayVacio(obtencionDatosTablaMiembrosFondo()), 'personasApoyoFondo': validarArrayVacio(obtencionDatosTablaPersonalApoyoFondo())});  
	}
	return false;
}

function manejadorMensajes(estatus){ //funcion que se encarga de manejar los mensajes que vienen desde dajax
	switch (estatus){
		case 1:
			alertify.success("Datos Guardados");			
			break;
		case 2:
			alertify.alert("Datos Actualizados Correctamente");
			break;
	}
}

function pasarComprobacionesDatosFondo() // Función que llama a validarControlesFormulario y verifica si los texts requeridos del formulario no se encuentren en blanco.
{
	validarControlesFormulario();	
	
	if ($("#NumeroEscritura").val() == '' || $("#NumeroNotario").val() == '' ||
		$("#CiudadNotario").val() == '' || $("#NombreNotario").val() == '' || $("#NumeroRegistroShcp").val() == '' || 
		$("#OficioRegistro").val() == '' || $("#LugarRegistro").val() == '' || $("#NumeroLibro").val() == '' || 
		$("#Foja").val() == '')
	{
		alertify.alert('Se requiere ingresar información.');
		return false;
	}
	
	if (isNaN($("#NumeroEscritura").val()) ||  isNaN($("#NumeroNotario").val()))
	{
		alertify.alert('Se requiere ingresar solo números en Número escritura y Número notario para continuar.');
		return false;
	}
	
	return true;
}

function limpiar_formulario(){ // Función que se encarga de limpiar los texts del formulario.
	location.reload();	
}

function buscarDatosFondo(){ // Función que busca los datos generales del fondo.
	Dajaxice.ConexosAgropecuarios.obtener_datos_fondo(cargarFormularioDatosFondo);	
}

function cargarMunicipiosDatosFondo(dato){ // Función que nos permite cargar en la tabla de municipios de la plantilla datosFondo.html los municipios que 
	var contenido = $('.municipios_datosFondo_tabla tbody');
	contenido.html('');
	
	if(dato.municipios)
	{
		$.each(dato.municipios, function(i,elemento)
		{
			$('<tr><td style="display: none;">'+elemento.IdMunicipio+'</td><td style="display: none;">'+elemento.IdAreaInfluencia+'</td><td>'+elemento.DescripcionEstado+'</td><td>'+elemento.DescripcionMunicipio+'</td><td><a onclick="eliminarMunicipioDatosFondo($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function cargarFormularioDatosFondo(dato){ // Función que manda a cargar en datosFondo.html la información de los datos del fondo.
	
	if(dato.datosfondo.length > 0)
	{
		var datoFondo = dato.datosfondo[0];
		$("#NumeroFondo").val(datoFondo.NumeroFondo);
		$("#NombreFondo").val(datoFondo.NombreFondo);
		$("#Domicilio").val(datoFondo.Domicilio);
		$("#Telefono").val(datoFondo.Telefono);
		$("#Email").val(datoFondo.Email);
		$("#varIdFondo").val(datoFondo.IdDatosFondo);
		$("#IdPersonaDatosFondo").val(datoFondo.Persona_id);
		$("#NumeroEscritura").val(datoFondo.NumeroEscritura);
		$("#NumeroNotario").val(datoFondo.NumeroNotario);    
		$("#CiudadUbicacionNotario").val(datoFondo.CiudadUbicacionNotario);
		$("#NombreNotario").val(datoFondo.NombreNotario);
		$("#NumeroRegistroShcp").val(datoFondo.NumeroRegistroShcp);
		$("#OficioRegistro").val(datoFondo.OficioRegistro);
		$("#Rfc").val(datoFondo.Rfc);
		$("#LugarRegistro").val(datoFondo.LugarRegistro);
		$("#NumeroLibro").val(datoFondo.NumeroLibro);
		$("#Foja").val(datoFondo.Foja);
		$("#FechaEscritura").val(datoFondo.FechaEscritura);
		$("#FechaRegistro").val(datoFondo.FechaRegistro);
		$("#FechaRppc").val(datoFondo.FechaRppc);
		
		Dajaxice.ConexosAgropecuarios.obtenerMunicipiosDatosFondo(cargarMunicipiosDatosFondo);
		buscarCuentasBancariasFondo(datoFondo.IdDatosFondo);
		buscarContratosFondo(datoFondo.IdDatosFondo);
		buscarMiembrosConsejoFondo();
		buscarPersonalApoyoFondo();
	}
}

function validarControlesFormulario(){ // Función que valida que la información ingresada en el formulario tenga el formato correcto.
	$('#formulario_datos_fondo').validate({
		errorElement: "span",
		rules: {
			NumeroEscritura: {
				digits:true,
				required: true
			},
			NumeroNotario: {
				digits:true,
				required: true
			},
			CiudadUbicacionNotario: {
				required: true
			},
			NombreNotario: {
				required: true
			},
			OficioRegistro: {
				required: true
			},
			LugarRegistro: {
				required: true
			},
			Foja: {
				required: true
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

var seleccionarTodosMunicipios = function(){ //Selecciona todos los municipios
	if ($("#chkSeleccionarTodosMunicipios").is(":checked"))
		$(".chosen-select option").attr('selected', true);
	else
		$(".chosen-select option").attr('selected', false);
	$(".chosen-select").trigger('chosen:updated');
}

function agregarMuncipioDatosFondo(){ // Funcion que agrega a la zona de influencia los municipios que se seleccionan desde el cmbMunicipios
	var contenido = $('.municipios_datosFondo_tabla tbody');
	idEstado = $("#cmbEstados option:selected").val()-1;
	descripcionEstado = $("#cmbEstados :nth-child("+idEstado+")").text();
	idMunicipio = $("#cmbMunicipios").val();
	if (idMunicipio){
		idMunicipio.forEach(function(id){
			registroDuplicado = comprobarMunicipioDuplicado(id);
			descripcionMunicipio =  $("#cmbMunicipios option[value="+id+"]").text();
			if (registroDuplicado){
				alertify.alert('El municipio '+descripcionMunicipio+' ya se encuentra en la zona de influencia');
			}else{
				$('<tr><td style="display: none;">'+id+'</td><td style="display: none;"></td><td>'+descripcionEstado+'</td><td>'+descripcionMunicipio+'</td><td><a onclick="eliminarMunicipioDatosFondo($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
			}
		});
	}else{
		alertify.alert('No se ha elegido Municipio');
	}
}

function comprobarMunicipioDuplicado(idMunicipio){ //Funcion que regresa true si el municipio no se encuentra agregado en la tabla de zona de influencia del fondo
	registroRepetido = false;
	$('.municipios_datosFondo_tabla tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 0:
					if ($(this).text() == idMunicipio){
						registroRepetido = true;
					}
					break;
			}
		});
	});
	return registroRepetido;	
}

function eliminarMunicipioDatosFondo(eliminar){ // Función que elimina las filas de la tabla de municipios_datosFondo_tabla que se encuentra en la plantilla datosFondo.html
	alertify.confirm("Esto eliminará el municipio, ¿Desea continuar?", function (e) {
	    if (e) {
			eliminar.parent().parent().remove();
			var rowEliminar = eliminar.closest("tr");	
			Dajaxice.ConexosAgropecuarios.eliminar_municipio_datosFondo(Dajax.process, {'idMunicipio':rowEliminar.children('td')[0].innerText});
			alertify.success("El municipio fue eliminado correctamente");
	    }
	});	
	return false;
}

function obtencionDatosTablaMunicipioDatosFondo(){ // Función que obtiene la información de la tabla municipios_datos_fondo y la agrega a una arreglo.
	var arrayMunicipios = [];

	$(".municipios_datosFondo_tabla tr").each(function() {
	    var arrayFilas = [];
	    var fila = $(this).find('td');
	    if (fila.length > 0) 
	    {
	    	fila.each(function()
	    	{
	    		arrayFilas.push($(this).text()); 
	    	});
	    	arrayMunicipios.push(arrayFilas);
	    }
	});
	
	return arrayMunicipios;
}

