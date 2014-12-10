var checked = false; //Variable Global ** Bandera que se encarga de hacer el check una vez para las direcciones de sepomex

$(document).on('ready',inicio);

function inicio(){ //Inicio de las funciones
	$("#btnBuscarSepomex").on('click',buscarSepomex);
	$("#btnAgregarDireccion").on('click',limpiarModalDireccion);
	$("#btnAceptarDireccion").on('click',agregarDireccionTabla);
	tablaBusquedaSepomex();
}

function agregarDireccionTabla(){ // Función que agrega la información obtenida del buscador de direcciones en la tabla que se encuentra en direcciones.html
	if (validarDireccion()){
		var contenido = $('.direccionesPersonaMoral tbody');
		DireccionSocio = validarDireccion();
		registroDuplicado = comprobarDireccionDuplicada(DireccionSocio.TipoDireccion,DireccionSocio.IdSepomex); 
		if ((registroDuplicado.tipoDireccionRepetida) || (registroDuplicado.idSepomexRepetido)){
			if (registroDuplicado.tipoDireccionRepetida){
				alertify.alert('El tipo de dirección se encuentra repetido');
			}
			if (registroDuplicado.idSepomexRepetido){
				alertify.alert('La dirección de Sepomex se encuentra repetida');
			}
			checked = false;
		}else{
			$('<tr><td style="display: none;">'+''+'</td><td>'+DireccionSocio.Calle+'</td><td>'+DireccionSocio.Cp+'</td><td>'+DireccionSocio.Colonia+'</td><td>'+DireccionSocio.Ciudad+'</td><td>'+DireccionSocio.Municipio+'</td><td>'+DireccionSocio.Estado+'</td><td>'+DireccionSocio.DescripcionTipoDireccion+'</td><td style="display:none">'+DireccionSocio.Detalle+'</td><td style="display:none">'+DireccionSocio.IdSepomex+'</td><td style="display:none">'+DireccionSocio.TipoDireccion+'</td><td style="display:none">'+DireccionSocio.NoExterior+'</td><td style="display:none">'+DireccionSocio.NoInterior+'</td><td><a onclick="eliminarDireccionesDeTabla($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
			//Se limpia toda la ventana modal para que no se quede el html generado
			borrarInformacionModalDireccion();
			$(".close").click();
		}		
	}else{
		alertify.alert('Falta especificar el tipo de dirección y/o dirección Sepomex');
		$('#TipoDireccion').focus();
	}
}

function comprobarDireccionDuplicada(idTipoDireccion,idSepomex){ // Funcion que comprueba que la persona que se esta agregando no se encuentre repetida, regresa true si ya esta
	var registroRepetido = new Object();
	registroRepetido.tipoDireccionRepetida = false;
	registroRepetido.idSepomexRepetido = false;
	$('.direccionesPersonaMoral tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 9:
					if ($(this).text() == idSepomex){
						registroRepetido.idSepomexRepetido = true;
					}
					break;
				case 10:
					if ($(this).text() == idTipoDireccion){
						registroRepetido.tipoDireccionRepetida = true;
					}
					break;				
			}
		});
	});
	return registroRepetido;
}


function buscarSepomex(){ //Entra en el click de buscar direcciones de la ventana modal, utiliza ajax.py para buscar la informacion necesaria de la caja de texto txtBuscarSepomex, el callback lo recibe en la funcion sepomexCallBack
	datosBuscar = $('#txtBuscarSepomex').val();
	Dajaxice.Direcciones.buscar_sepomex(sepomexCallBack,{'datosBuscar':datosBuscar});
	return false;
}

function sepomexCallBack(data){ //Obtiene la informacion de la busqueda de la direccion de sepomex que recibe del metodo buscar_sepomex de ajax.py, los datos de la busqueda se agregan a la tabla busquedaSepomex de la ventana modal
	var contenido = $('.busquedaSepomex tbody');
	contenido.html('');
	if(data.sepomex){
		$.each(data.sepomex, function(i,elemento){
			$('<tr><td><input type="checkbox" disabled></td><td>'+elemento.IdSepomex+'</td><td>'+elemento.Cp+'</td><td>'+elemento.Asentamiento+'</td><td>'+elemento.Ciudad+'</td><td>'+elemento.Municipio+'</td><td>'+elemento.Estado+'</td></tr>').appendTo(contenido);
		});
	}else{
		alertify.alert('No se encontro información');
	}
}

function tablaBusquedaSepomex(){ //Funcion que permite interactuar con la ventana modal de busqueda sepomex
	
	$('.busquedaSepomex tbody').on('mouseover', 'tr', function(event) { //toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.busquedaSepomex tbody').on('mouseout', 'tr', function(event) { //evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});	

	$('.busquedaSepomex tbody').on('click', 'tr', function(event) { //evento click que selecciona el row y marca el check de la tabla
		if (checked){
			if($(this).children().children().is(':checked')){
				$(this).children().children().prop('checked',false);
				checked = false;
				$('#SepomexId').val('');
				$('#SepomexCp').val('');
				$('#SepomexColonia').val('');
				$('#SepomexCiudad').val('');
				$('#SepomexMunicipio').val('');
				$('#SepomexEstado').val('');
			}
		}else{
			$(this).css({"background-color":"#0099FF"});
			$(this).children().children().prop('checked',true);
			checked = true;
			// se asignan los valores a los campos ocultos
			$(this).children('td').each(function(indice){
				switch(indice){
					case 1:
						$('#SepomexId').val($(this).text());
						break;
					case 2:
						$('#SepomexCp').val($(this).text());
						break;
					case 3:
						$('#SepomexColonia').val($(this).text());
						break;	
					case 4:
						$('#SepomexCiudad').val($(this).text());
						break;	
					case 5:
						$('#SepomexMunicipio').val($(this).text());
						break;	
					case 6:
						$('#SepomexEstado').val($(this).text());
						break;							
				}
			});			
		}
	});		
}

function limpiarModalDireccion(){ //Se llama la funcion cuando se da click en el boton de agregar direccion para que borre el contenido de la tabla que vacia el resultado de la busqueda de direcciones, ademas de los campos que muestra la ventana modal
	$('#direcciones').on('shown',function(){
		$('#TipoDireccion').focus();
	});
	checked = false; //Bandera que se encarga de hacer el check una vez para las direcciones de sepomex
	borrarInformacionModalDireccion();
}

function borrarInformacionModalDireccion(){
	$('#TipoDireccion').val('');
	$('#Calle').val('');
	$('#Detalle').val('');
	$('#txtBuscarSepomex').val('');
	$('#NumeroExterior').val('');
	$('#NumeroInterior').val('');
	$('.busquedaSepomex tbody').html('');	
}

function validarDireccion(){ // Valida el formulario que se encuentra en la plantilla direcciones.html
	if ($('#TipoDireccion').val()=="" || $('#SepomexId').val()==""){
		return false;
	}
	var DireccionSocio = new Object();
	DireccionSocio.TipoDireccion = $('#TipoDireccion').val();
	DireccionSocio.DescripcionTipoDireccion = $('#TipoDireccion option:selected').text();
	if ($('#NumeroExterior').val()!=""){
		DireccionSocio.NoExterior = $('#NumeroExterior').val();
	}else{
		DireccionSocio.NoExterior = '';
	}
	if ($('#NumeroInterior').val()!=""){
		DireccionSocio.NoInterior = $('#NumeroInterior').val();
	}else{
		DireccionSocio.NoInterior ='';
	}
	if ($('#Calle').val()==""){
		DireccionSocio.Calle = 'NO ESPECIFICADO';
	}else{
		DireccionSocio.Calle = $('#Calle').val().toUpperCase();
	}
	
	DireccionSocio.Cp = $('#SepomexCp').val();
	DireccionSocio.Colonia = $('#SepomexColonia').val().toUpperCase();
	DireccionSocio.Ciudad = $('#SepomexCiudad').val().toUpperCase();
	DireccionSocio.Municipio = $('#SepomexMunicipio').val().toUpperCase();
	DireccionSocio.Estado = $('#SepomexEstado').val().toUpperCase();
	DireccionSocio.Detalle = $('#Detalle').val().toUpperCase();
	DireccionSocio.IdSepomex = $('#SepomexId').val().toUpperCase();
	
	return DireccionSocio;
}

function buscarDireccionesConIdPersona(idPersona){ // Función que busca la lista de direcciones relacionados con una persona pasando el idpersona.
	Dajaxice.Direcciones.buscar_direcciones_idsepomex(cargarTablaDirecciones, {'idPersona':idPersona});	
	return false;
}

function cargarTablaDirecciones(data){ // Función que carga las direcciones obtenidos de la función buscarDireccionesConIdPersona en la tabla direccionesPersonaMoral.
	var contenido = $('.direccionesPersonaMoral tbody');
	contenido.html('');
	
	if(data.direcciones)
	{
		$.each(data.direcciones, function(i,direccion)
		{
			var tipoDireccion = 'DOMICILIO';
			
			if(direccion.TipoDireccion == "2")
			{
				tipoDireccion = 'TRABAJO';
			}
				
			$('<tr><td style="display: none;">'+direccion.IdDireccion+'</td><td>'+direccion.Calle + ' ' + direccion.NumeroExterior+direccion.NumeroInterior+'</td><td>'+direccion.Cp+'</td><td>'+direccion.Colonia+'</td><td>'+direccion.Ciudad+'</td><td>'+direccion.Municipio+'</td><td>'+direccion.Estado+'</td><td>'+tipoDireccion+'</td><td style="display:none">'+ direccion.Detalle+'</td><td style="display:none">'+direccion.IdSepomex+'</td><td style="display:none">'+ direccion.TipoDireccion +'</td><td style="display:none">'+ direccion.NumeroExterior+'</td><td style="display:none">'+ direccion.NumeroInterior+'</td><td><a onclick="eliminarDireccionesDeTabla($(this));" href="#"><i class="icon-remove"></i></a></td></tr>').appendTo(contenido);
		});
	}
	else
	{
		alertify.alert('No se encontro información');
	}
}

function eliminarDireccionesDeTabla(eliminar){ // Función que elimina las filas de la tabla de Direcciones que se encuentra en la plantilla moral.html y fisica.html 
	alertify.confirm("Esto eliminará la dirección, ¿Desea continuar?", function (e) {
	    if (e) {
			eliminar.parent().parent().remove();
			var rowEliminar = eliminar.closest("tr");	
			Dajaxice.Direcciones.eliminar_direccion(Dajax.process, {'idDireccion':rowEliminar.children('td')[0].innerText});
			alertify.success("La dirección fue eliminada correctamente");
	    }
	});	
	return false;	
}