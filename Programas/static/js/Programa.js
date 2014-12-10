$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del formulario teléfonos.
	activarMenu();
	buscarAreaInfluenciaFondo();
	buscarTipoSeguros();	
	modalBusquedaHabilitador();
	$("#IdTipoSeguro").change(cargarCmbSubTipoSeguro);	
	$("#Ejercicio").val(añoActual());
	$("#btnBuscarHabilitador").click(buscarHabilitadorPrograma);
	$("#btnGuardarPrograma").click(guardarPrograma);
	$("#btnCancelarPrograma").on("click", limpiar_formulario_programa);
	$("#btnListadoProgramas").on("click", regresarListadoProgramas);
	$("#btnBuscarPersonaSolicitante").on("click", limpiarModalHabilitadorPrograma)	
	document.getElementById("PersonaHabilitador").readOnly = true;	
	
	var idPrograma = $("#varIdPrograma").val();

	if (idPrograma != "")
	{
		$("#btnVistaPrevia").click(vistaPrevia);
		buscarPrograma(idPrograma);
		if($("#varUtilizado").val()=='True'){
			deshabilitarControles();
		}
	}
	else
	{
		$("#btnVistaPrevia").attr('disabled', 'true');
	}
	
	//obtener el tipo de moneda segun el contrato y toma en cuenta el evento change cuando no exista informacion (programa nuevo)
	$('#IdContratoFondo').change(contratoFondo);	
}

var deshabilitarControles = function(){ //Si el programa ya cuenta con cotizador se deshabilitan los controles
	$("#IdContratoFondo").prop("disabled",true);
	$("#btnBuscarPersonaSolicitante").prop("disabled",true);
	$("#IdTipoSeguro").prop("disabled",true);
	$("#IdSubTipoSeguro").prop("disabled",true);
	$("#IdTipoMoneda").prop("disabled",true);
	$("#Ejercicio").prop("disabled",true);
	$("#Observaciones").prop("disabled",true);
}

var contratoFondo = function(){ //Funcion para obtener los datos del contrato del fondo para el tipo de moneda
	if ($("#IdContratoFondo").val()>0){
		Dajaxice.ConexosAgropecuarios.obtenerDatosContratoFondo(cargarMonedaContratoFondo, {'idContratoFondo':$('#IdContratoFondo').val()});
	}else{
		$("#IdTipoMoneda").text('');
	}
}

var cargarMonedaContratoFondo = function(datos){ //Se cargan los tipos de moneda segun el catalogo de monedas y el tipo de moneda que tenga el contrato de retro
	//borrar el select
	$('#IdTipoMoneda').find('option').remove();
	//cargar el o los tipos de monedas permitidas para la programacion segun el contrato de retro
	$.each(datos.DescripcionMoneda, function(i,elemento){
		$('#IdTipoMoneda').append($('<option />').attr('value',elemento.IdMoneda).text(elemento.DescripcionMoneda));
	});
}

var deshabilitarBotonGuardar = function() { // Función que nos permite deshabilitar el boton de guardar.
	$("#btnGuardarPrograma").unbind("click");
	$("#btnGuardarPrograma").attr("disabled","disabled");
}

function limpiarModalHabilitadorPrograma(){ // Función que cierra el formulario modal para la busqueda del habilitador.
	$("#txtBuscarHabilitador").val('');
	var contenido = $('.tblBusquedaHabilitador tbody');
	contenido.html('');	
}

function vistaPrevia(){ // Función que permite mostrar el programa seleccionado de la table listado_programa_tabla pasando el id del programa a la plantilla programa.html
	location.href = '/ReportePrograma/?' + $("#varIdPrograma").val();
}

function limpiar_formulario_programa(){ // Función que se encarga de limpiar el formulario de la plantilla Programa.html
	
	if ($("#varIdPrograma").val() == '')
	{
		document.getElementById("formulario_programas_aseguramiento").reset();
		$("#varIdPrograma").val('');
		$("#varUtilizado").val('');
		$("#varIdHabilitador").val('');
		$("#rB").html('');
		$("#rC").html('');		
	}
	else
	{
		regresarListadoProgramas();
	}
}

function regresarListadoProgramas() { // Función que permite regresar al listado de los programas.
	location.href = '/Programas/';
}

function modalBusquedaHabilitador(){ //Función que permite interactuar con la ventana modal de busqueda del habilitador del programa.
	$("#mdlBuscarHabilitadorPersonaMoral").on('shown', function() {
	    $("#txtBuscarHabilitador").focus();
	});

	$('.tblBusquedaHabilitador tbody').on('mouseover', 'tr', function(event) { //Toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.tblBusquedaHabilitador tbody').on('mouseout', 'tr', function(event) { // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	
	
	$('.tblBusquedaHabilitador tbody').on('click', 'tr', function(event) { // permite agregar los datos del programa en los input text correspondientes.	
		$('#varIdHabilitador').val($(this).children('td')[0].innerText);
		$('#PersonaHabilitador').val($(this).children('td')[1].innerText);
		$(".close").click();
	});			
}

function mensajePrograma(folioPrograma){ //Funcion que recibe el numero de folio del programa de la funcion Dajaxice.Programa.guardar_programa para mostrarla en un alert
	alertify.alert('Programa Guardado con el Folio: '+ folioPrograma);
}

function buscarHabilitadorPrograma(){ // Función que busca a una persona para agregarla como habilitador del programa.	
	var tipoPersona = 'M';
	Dajaxice.BuscadorPersonas.obtenerPersonaPorTipo(cargarTablaBusquedaHabilitador, {'datosBuscar':$("#txtBuscarHabilitador").val().toUpperCase(),'tipoPersona':tipoPersona});
	return false;
}

function cargarTablaBusquedaHabilitador(data){ // Función que carga la información en el formulario de los posibles habilitadores encontradas.
	var contenido = $('.tblBusquedaHabilitador tbody');
	contenido.html('');
	
	if(data.personas)
	{
		$.each(data.personas, function(i,elemento)
		{	
			nombreCompleto = arreglarNombreMoralFisica(elemento);
			
			$('<tr><td>'+elemento.IdPersona+'</td><td>'+nombreCompleto+'</td><td>'+elemento.Rfc+'</td><td style="display: none;">'+elemento.Direccion+'</td><td style="display: none;">' + elemento.Telefono + '</td><td style="display: none;">'+elemento.CP+'</td><td style="display: none;">'+elemento.Municipio+'</td><td style="display: none;">'+elemento.Estado+'</td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro ninguna persona moral.');
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

function buscarAreaInfluenciaFondo(){ // Función que busca municipios los cuales pertenecen al área de influencia del fondo de aseguramiento, llamando a la función obtener_areas_influencia_fondo y cargando la informacion en la funcion cargarAreaInfluencia.
	Dajaxice.Programas.obtener_areas_infuencia_fondo(cargarAreaInfluenciaCheckEdit);
	return false;
}

function cargarAreaInfluenciaCheckEdit(data){ // Función que permite generar los checkedit's en base al área de influencia al cual pertenece el fondo de aseguramiento.
	$("#rC").html('');
			
	if(data.areasInfluencia)
	{			
		$.each(data.areasInfluencia, function(i,area)
		{
			check = '<li><input type="checkbox" size="20" value= '+ area.IdAreaInfluencia + '>'+ ' ' + area.Descripcion+'</li>';
			$("#rC").append(check);
		});
	}
	iCheckActivate('#rC');
}

function buscarPrograma(idPrograma){ // Función que busca la información del programa seleccionado.
	Dajaxice.Programas.buscar_programa(cargarInformacionPrograma, {'idPrograma': idPrograma});
	return false;
}

function cargarCobertura(dato){ // Función que permite cargar las coberturas del programa a editar.
	
	if(dato.coberturasprograma)
	{
		$.each(dato.coberturasprograma, function(i,elemento)
		{
			$("#rB input[type=checkbox]").each(function()
			{
		        if ($(this).val() == elemento.IdCobertura)
				{
		        	$(this).prop( "checked", true );
				}
		    });
		});
	}
	iCheckActivate('#rB');
}

function cargarAreaInfluencia(data){ // Función que permite cargar la área de influencia del programa seleccionado para editar.
	
	if(data.areaInfluenciaPrograma)
	{
		$.each(data.areaInfluenciaPrograma, function(i,area)
		{
			$("#rC input[type=checkbox]").each(function()
			{
		        if ($(this).val() == area.IdAreaInfluencia)
				{
		        	$(this).prop( "checked", true );
				}
		    });
		});
	}
	iCheckActivate('#rC');
}

var iCheckActivate = function(id){ //Funcion para activar iCheck en los formularios
	$(id.concat(' input')).iCheck({
	    checkboxClass: 'icheckbox_square-aero',
	    radioClass: 'iradio_square-aero'
	});	
}

function cargarInformacionPrograma(data){ // Función que carga la encontrada del programa en el formulario de la plantilla programa.html
	programaACargar = data.programaEncontrado[0];
	$("#varIdPrograma").val(programaACargar.IdPrograma);
	$('#IdTipoSeguro').val(programaACargar.IdTipoSeguro);
	$('#varIdHabilitador').val(programaACargar.IdPersona);
	$('#PersonaHabilitador').val(programaACargar.RazonSocial);
	$("#IdSubTipoSeguro").val(programaACargar.IdSubSeguro);
	$("#Ejercicio").val(programaACargar.Ejercicio);	
	$("#Observaciones").val(programaACargar.Observaciones);
	$("#IdContratoFondo").val(programaACargar.IdContratoFondo);
	$("#varUtilizado").val(programaACargar.Utilizado);
	$("#IdTipoMoneda").val(programaACargar.IdTipoMoneda);
	Dajaxice.Programas.cargar_Combo_Coberturas(cargarCheckEdit,{'idTipoSeguro':$("#IdTipoSeguro").val()});
	window.setTimeout('buscarCoberturaPrograma()', 500);
	window.setTimeout('buscarAreasInfluencia()', 500);
}

var buscarCoberturaPrograma = function() { // Función que nos permite cargar las coberturas de los programas de la base de datos mediante la función buscar_cobertura_programa que se encuentra en el ajax.
	Dajaxice.Programas.buscar_cobertura_programa(cargarCobertura, {'idPrograma': $("#varIdPrograma").val()});
	return false;
}

var buscarAreasInfluencia = function() { // función que nos permite cargar las areas de influencia del programa de la base de datos mediante la función obtener_area_influencia_con_idprograma que se encuentra en el ajax.
	Dajaxice.Programas.obtener_area_influencia_con_idprograma(cargarAreaInfluencia, {'idPrograma': $("#varIdPrograma").val()});	
	return false;
}

function buscarTipoSeguros(){ // Función que busca el listado de tipos de seguros.
	Dajaxice.Programas.cargar_Combo_TipoSeguro(Dajax.process);
	return false;
}

function cargarCmbSubTipoSeguro(){ // Función que busca el listado de sub tipos de seguros.
	var selectTipoSeguro = document.getElementById("IdTipoSeguro");
	
	if (selectTipoSeguro.options[selectTipoSeguro.selectedIndex].text == "---------")
	{
		$("#IdSubTipoSeguro").empty();
		$("#rB").html('');
	}
	else
	{
		Dajaxice.Programas.cargar_Combo_SubTipoSeguro(Dajax.process,{'idTipoSeguro':$("#IdTipoSeguro").val()});
		Dajaxice.Programas.cargar_Combo_Coberturas(cargarCheckEdit,{'idTipoSeguro':$("#IdTipoSeguro").val()});
		return false;
	}
}

function cargarCheckEdit(dato){ // Función que permite generar check en tiempo de ejecución dependiendo que tipo seguro se elija.
	$("#rB").html('');
			
	if(dato.coberturas)
	{			
		$.each(dato.coberturas, function(i,cobertura)
		{
			check = '<li><input type="checkbox" size="20" value= '+ cobertura.IdCobertura + ' />'+ ' ' + cobertura.Descripcion+'</li>';
			$("#rB").append(check);
		});
	}
	iCheckActivate('#rB');
}

function guardarPrograma(){ // Función que envia el formulario_Programa para guardarlo en la base de datos.
	
	if (pasarComprobacionesPrograma())
	{
		if ($("#varIdPrograma").val() == '')
		{
			Dajaxice.Programas.guardar_programas(Dajax.process,{'formulario':$('#formulario_programas_aseguramiento').serialize(true), 'coberturas':obtenerCheckBoxSeleccionados(), 'folio':generarFolioPrograma(), 'areaInfluencia':obtenerCheckBoxAreaInfluenciaSeleccionados()});
			limpiar_formulario_programa();
		}
		else
		{
			alertify.confirm("¿Desea modificar el programa?", function (e) 
			{
			    if (e) 
			    {
			    	Dajaxice.Programas.guardar_programas(Dajax.process,{'formulario':$('#formulario_programas_aseguramiento').serialize(true), 'coberturas':obtenerCheckBoxSeleccionados(), 'folio':generarFolioPrograma(), 'areaInfluencia':obtenerCheckBoxAreaInfluenciaSeleccionados()});
					$("#IdContratoFondo").focus();
			    }
			});
		}
	}
			
	return false;
}

function generarFolioPrograma(){ // Función que genera el folio del programa.
	
	var tipoSeguro = document.getElementById("IdTipoSeguro");
	var primerLetraTipoSeguro = tipoSeguro.options[tipoSeguro.selectedIndex].text.substr(0,1);
	var subTipoSeguro = document.getElementById("IdSubTipoSeguro");
	var primerLetraSubTipoSeguro = subTipoSeguro.options[subTipoSeguro.selectedIndex].text.substr(0,1);
	var folio = primerLetraTipoSeguro + primerLetraSubTipoSeguro + "-";
	
	return folio;
}

function obtenerCheckBoxSeleccionados(){ // Función que obtiene el valor de los check seleccionados almacenandolo en un array.
	var arrayCheckBox = [];

	 $("#rB input:checked").each(function(){ 
		 	arrayCheckBox.push($(this).val());    
	    });
	
	return arrayCheckBox;
}

function obtenerCheckBoxAreaInfluenciaSeleccionados(){ // Función que obtiene el valor de los check de area de influencia seleccionados almacenandolo en un array.
	var arrayCheckBox = [];

	 $("#rC input:checked").each(function(){ 
		 	arrayCheckBox.push($(this).val());    
	    });
	
	return arrayCheckBox;
}

function pasarComprobacionesPrograma(){ // Función que permite verificar que la información ingresada en el formulario sea la correcta.
	
	if ($("#IdContratoFondo").val() == "")
	{
		alertify.alert('Se requiere seleccionar un contrato para continuar.');
		return false;
	}
	
	if ($("#PersonaHabilitador").val() == "")
	{
		alertify.alert('Se requiere seleccionar un habilitador del programa para continuar.');
		return false;
	}
	
	if ($("#IdTipoSeguro").val() == "#")
	{
		alertify.alert('Se requiere seleccionar tipo de seguro para continuar.');
		return false;
	}
	
	if ($("#IdSubTipoSeguro").val() == "")
	{
		alertify.alert('Se requiere seleccionar sub tipo de seguro para continuar.');
		return false;
	}
	
	var tipoMoneda = document.getElementById("IdTipoMoneda");
	var checarMoneda = tipoMoneda.options[tipoMoneda.selectedIndex].text;
		
	if (checarMoneda == "---------")
	{
		alertify.alert('Se requiere seleccionar moneda para continuar para continuar.');
		return false;
	}
		
	if ($("#Ejercicio").val() == "")
	{
		alertify.alert('Se requiere ingresar el año en el cual esta habilitado el programa para continuar.');
		return false;
	}		
	
	if ($("#Ejercicio").val().length > 4 || $("#Ejercicio").val().length < 4)
	{
		alertify.alert('El ejercicio debe ser de 4 digitos para continuar.');
		return false;
	}
	
	if (isNaN($("#Ejercicio").val()))
	{
		alertify.alert('Se requiere ingresar solo números en ejercicio para continuar.');
		return false;
	}
	
	return true;
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(1)').addClass('active');
}

function añoActual(){ // Función que devuelve el año actual.
	var ano = (new Date).getFullYear();
	
	return (ano);
}

function manejadorMensajes(estatus){ // funcion que se encarga de manejar los mensajes que vienen desde dajax
	switch (estatus){
		case 1:
			alertify.success("Datos Guardados");		
			break;
		case 2:
			alertify.alert("Datos Actualizados Correctamente");
			break;		
	}
	return false;
}

function validarControlesFormulario(){ // Función que valida que la información ingresada en el formulario tenga el formato correcto.
	$('#formulario_programas_aseguramiento').validate({
		errorElement: "span",
		rules: {
			IdContrato: {
				required: true
			},
			Habilitador: {
				required: true
			},
			IdTipoSeguro: {
				required: true
			},
			IdSubTipoSeguro: {
				required: true
			},
			IdTipoMoneda: {
				required: true
			},
			Ejercicio: {
				minlength: 4,
				maxlength: 4,
				required: true
			},
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