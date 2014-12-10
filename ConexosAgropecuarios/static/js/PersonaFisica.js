$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario persona.
	activarMenu();
	
	$("#FechaNacimiento").val(fechaActual());
	
	$("#FechaNacimiento").datepicker({
		firstDay: 1
	});
	
	$('#EsSocio').prop('checked', false);
	
	$("#Numero").mask("(999) 999-9999");	
	$('#PrimerNombre').change(rfc);
	$('#ApellidoPaterno').change(rfc);
	$('#ApellidoMaterno').change(rfc);
	$('#FechaNacimiento').change(rfc);	
	$("#Guardar").click(guardar_persona_fisica);
	$("#Cancelar").click(recargarPagina);
	$("#btnBuscarPersona").on('click',buscarPersonaFisica);
	
	generarColumnasTablaBusquedaPersona();
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function buscarPersonaFisica(){ // Función que llama a buscarPersona de buscadorPersona.js pasandole un indicador de persona fisica 'F'.
	buscarPersona('F');
	return false;
}

function generarColumnasTablaBusquedaPersona(){ // Función que genera las columnas de la tabla busquedaPersona cuando el buscador es llamdado de la plantilla fisica.html
	var contenido = $('.busquedaPersona thead');
	contenido.html('');	
	$("<tr><th>"+"#"+"</th><th>"+"Nombre"+"</th><th>"+"Apellido Paterno"+"</th><th>"+"Apellido Materno"+"</th><th>"+"Rfc"+"</th></tr>").appendTo(contenido);
}

function fechaActual(){ // Función que genera y devuelve la fecha de hoy.
	var currentTime = new Date();
	var day = ("0" + currentTime.getDate()).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return (day+'/'+month+'/'+year);
}

function manejadorMensajesFisica(){ // Función que se encarga de manejar los mensajes que vienen desde dajax
	alertify.alert('Se requiere ingresar información.');
	return false;
}

function guardar_persona_fisica(){	// Función que guarda la información de la persona física pasando comprobaciones. 
	if (pasarComprobaciones())
	{
		var indicadorEsSocio = 0;
		
		if($('#EsSocio').is(':checked'))
		{
			indicadorEsSocio = 1;
		}
		
		direcciones = obtieneDatosTabla('.direccionesPersonaMoral');
		
		if ($("#varIdPersona").val() == '')
		{
			Dajaxice.ConexosAgropecuarios.guardar_persona_fisica(Dajax.process,{'formulario':$('#formulario_persona_fisica').serialize(true), 'telefonos':validarArrayVacio(obtencionDatosTablaTelefonos()),'indicadorEsSocio':indicadorEsSocio, 'direcciones':validarArrayVacio(direcciones)});
			limpiarFormularioPersonaFisica();
		}
		else
		{
			alertify.confirm("¿Desea modificar la persona?", function (e) 
			{
			    if (e) 
			    {	
					Dajaxice.ConexosAgropecuarios.guardar_persona_fisica(Dajax.process,{'formulario':$('#formulario_persona_fisica').serialize(true), 'telefonos':validarArrayVacio(obtencionDatosTablaTelefonos()),'indicadorEsSocio':indicadorEsSocio, 'direcciones':validarArrayVacio(direcciones)});
					alertify.success("Datos Actualizados Correctamente");
					$("#RazonSocial").focus();
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

function limpiarFormularioPersonaFisica() { // Función que permite limpiar los controles del formulario de persona física.
	var contenido = $('.telefonos_tabla tbody');
	contenido.html('');
	var contenidoDirecciones = $('.direccionesPersonaMoral tbody');
	contenidoDirecciones.html('');
	$("#varIdPersona").val('');
	document.getElementById("formulario_persona_fisica").reset();	
	$('#EsSocio').prop('checked', false);
}

function cargarPersonaFisicaEnFormulario(persona){ // Función que obtiene a la persona encontrada y la carga en los controles del formulario.
	$("#Rfc").val(persona.Rfc);
	$("#Curp").val(persona.Curp);
	$("#PrimerNombre").val(persona.PrimerNombre);
	$("#SegundoNombre").val(persona.SegundoNombre);
	$("#ApellidoPaterno").val(persona.ApellidoPaterno);
	$("#ApellidoMaterno").val(persona.ApellidoMaterno);		
	$("#FechaNacimiento").val(persona.FechaNacimiento);
	$("#Sexo").val(persona.Sexo);
	$("#Email").val(persona.Email);
	$("#EstadoCivil").val(persona.EstadoCivil);
	$("#varIdPersona").val(persona.IdPersona);
	
	var boolSocio = false;
	if (persona.EsSocio == 1)
	{
		boolSocio = true;
	}
			
	$('#EsSocio').prop('checked', boolSocio);
}

function validarControlesFormulario(){ // Función que valida que la información ingresada en el formulario tenga el formato correcto.
	$('#formulario_persona_fisica').validate({
		errorElement: "span",
		rules: {
			Rfc: {
				minlength: 13,
				maxlength: 13,
				required: true
			},
			Curp: {
				minlength: 18,
				maxlength: 18,
				required: true
			},
			PrimerNombre: {
				minlength: 2,
				required: true
			},
			FechaNacimiento: {
				required: true
			},
			ApellidoPaterno: {
				minlength: 2,
				required: true
			},
			ApellidoMaterno: {
				minlength: 2,
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

function pasarComprobaciones() // Función que llama a validarControlesFormulario y verifica si los texts requeridos del formulario no se encuentren en blanco.
{
	validarControlesFormulario();	
	
	if ($("#Rfc").val() == '' || $("#Curp").val() == '' || $("#PrimerNombre").val() == '' || $("#ApellidoPaterno").val() == '' || $("#FechaNacimiento").val() == '')
	{
		return false;
	}
	
	return true;
}

function rfc(){ // Función que genera el rfc apartir de la información ingresada en el formulario.
	var nombre = $.trim($("#PrimerNombre").val().toUpperCase());
	var apaterno = $.trim($("#ApellidoPaterno").val().toUpperCase());
	var amaterno = $.trim($("#ApellidoMaterno").val().toUpperCase());
	var fecha = $.trim($("#FechaNacimiento").val()).split("/");
	var dia = fecha[0];
	var mes = fecha[1];
	var anio = fecha[2];
	
	apaterno = $.trim(apaterno);
	var aux=apaterno.substring(1, apaterno.length);
	
	var i;
		
	apaterno=quitarart(apaterno);	
	amaterno=quitarart(amaterno);
	var bandera = false;
	
	rfc = apaterno.substring(0,1);
	
	for(i=0; i < aux.length; i++)
	{
		if (vocal (aux.charAt(i)))
		{
			rfc += aux.charAt(i);
			bandera=false;
			break;
		}
		else
		{
			bandera=true;
		}
	}
	
	if (bandera){
		rfc += "X";
	}
	
	if (amaterno.length > 0)
	{
		rfc += amaterno.substring(0,1);
	}
	else
	{
		rfc += "X";
	}	
	
	rfc += ignoranomc(nombre);
	
	if (rfc == "PUTO" || rfc == "PUTA" || rfc == "CULO" || rfc == "CULA" || rfc == "QULO" || rfc == "QULA" || rfc == "MAME" || rfc == "MAMO")
	{
		rfc =rfc.substring(0,1) + "X" + rfc.substring(2,3);
	}
	
	rfc += String(anio).substring(2,4);
	rfc += mes;
	rfc += dia;
	
	$("#Rfc").val(rfc);
}

function quitarart(apellido){ // Quita articulos de los apellidos paternos y maternos.
	apellido = apellido.replace(/DEL /gi, "");
	apellido = apellido.replace(/LAS /gi, "");
	apellido = apellido.replace(/DE /gi, "");
	apellido = apellido.replace(/LA /gi, "");
	apellido = apellido.replace(/Y /gi, "");
	apellido = apellido.replace(/A /gi, "");
	apellido = apellido.replace(/MC /gi, "");
	apellido = apellido.replace(/LOS /gi, "");
	apellido = apellido.replace(/VON /gi, "");
	apellido = apellido.replace(/VAN /gi, "");
	return apellido;		
}

function ignoranomc(nombre){ // Regresa la primera vocal del primer nombre ignorando nombres comunes como José y María.	
	var nombres=nombre.split(" ");
	if (nombres[0].length > 1)
	{
		if(nombres[0] == "JOSE" || UTF8.decode(nombres[0]) == UTF8.decode("JOSÉ") || nombres[0] == "MARIA" || nombres[0] == UTF8.decode("MARÍA") || 
			nombres[0] == "MA." || nombres[0] == "MA")
		{			
			return nombres[1].charAt(0);
		}
		else
		{
			return nombres[0].charAt(0);
		}
	}
	else
	{
		return nombre.charAt(0);
	}
}

UTF8 ={ 
		encode: function (s){
			for(var c, i = -1, l = (s = s.split("")).length, o = String.fromCharCode; ++i < l;
			s[i] = (c = s[i].charCodeAt(0)) >= 127 ? o(0xc0 | (c >>> 6)) + o(0x80 | (c & 0x3f)) : s[i]);
			return s.join("");
		},
		decode: function(s){
			for(var a, b, i = -1, l = (s = s.split("")).length, o = String.fromCharCode, c = "charCodeAt"; ++i < l;
				((a = s[i][c](0)) & 0x80) &&
				(s[i] = (a & 0xfc) == 0xc0 && ((b = s[i + 1][c](0)) & 0xc0) == 0x80 ?
				o (((a & 0x03) << 6) + (b & 0x3f)) : o(128), s[++i] = ""));
				return s.join("");				
		}
}

function vocal(letra){	// Función que recibe una letra y valida si es vocal.
	if (letra == 'A' || letra == 'E' || letra == 'I' || letra == 'O' || letra == 'U')
	{
		return true;
	}
	else
	{
		return false;
	}
}

function mensajePersonaFisica(idPersona){ //Funcion que recibe el id de la persona. 
	alertify.alert('La Persona se Guardado con el IdPersona: '+ idPersona);
}