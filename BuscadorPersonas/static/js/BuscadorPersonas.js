$(document).on('ready',inicio);

function inicio(){	// Función que inicia las variables y los eventos de los controles del modal buscador personas.
	$("#btnBuscarPersonaModal").on('click',limpiarBuscadorPersonaModal);
	tablaBusquedaPersona();
}

var tipoPersona;

function buscarPersona(tipoPersonaRecibida){ // Entra en el click de buscar persona de la ventana modal, utiliza ajax.py para buscar la informacion necesaria de la caja de texto txtBuscar, el callback lo recibe en la función personaCallBack.
	datosBuscar = $('#txtBuscarPersona').val();	
	tipoPersona = tipoPersonaRecibida;
	Dajaxice.BuscadorPersonas.buscar_persona(personaCallBack, {'datosBuscar':datosBuscar.toUpperCase(), 'tipoPersona':tipoPersona});
	return false;
} 

function personaCallBack(data){ // Obtiene la informacion de la busqueda de la persona que recibe del método buscar_persona de ajax.py, los datos de la busqueda se agregan a la tabla busquedaPersona de la ventana modal.
	var contenido = $('.busquedaPersona tbody');
	contenido.html('');	
	
	if(data.personas)
	{
		$.each(data.personas, function(i,elemento)
		{
			if(tipoPersona == 'F')
			{				
				$('<tr><td>'+elemento.IdPersona+'</td><td>'+elemento.Nombre+"</td><td>"+elemento.ApellidoPaterno+"</td><td>"+elemento.ApellidoMaterno+"</td><td>"+elemento.Rfc+"</td></tr>").appendTo(contenido);
			}
			else
			{
				$('<tr><td>'+elemento.IdPersona+'</td><td>'+elemento.RazonSocial+"</td><td>"+elemento.Rfc+"</td></tr>").appendTo(contenido);
			}			
		});
	}
	else
	{
		alert('No se encontro información');
	}
}

function limpiarBuscadorPersonaModal(){ // Función que cierra el formulario modal buscadorPersona.
	$("#txtBuscarPersona").val('');
	var contenido = $('.busquedaPersona tbody');
	contenido.html('');	
}

function tablaBusquedaPersona(){ // Función que permite interactuar con la ventana modal de busqueda de personas.
	$(".modal").on('shown', function() {
	    $("#txtBuscarPersona").focus();
	});
	
	$('.busquedaPersona tbody').on('mouseover', 'tr', function(event) { //Toma el evento mouseover en funcion live para que el tr seleccionado cambie de color al igual que el cursor
		$(this).parent().parent().removeClass("table-striped");
		$(this).css({"background-color":"#adff2f","cursor":"pointer"});
	});

	$('.busquedaPersona tbody').on('mouseout', 'tr', function(event) { // evento mouseout que elimina los estilos (background de todo el tr) y agrega el estilo sebra a la tabla
		$(this).parent().parent().addClass("table-striped");
		$(this).removeAttr("style");
	});

	var idPersona;
	
	$('.busquedaPersona tbody').on('click', 'tr', function(event) { // permite agregar a la tabla de personas principal el registro que se seleccione.		
		idPersona = $(this).children('td')[0].innerText;
		buscarPersonaConIdPersona(idPersona);
		$(".close").click();
	});	
}

function buscarPersonaConIdPersona(idPersona){ // Función que busca a una persona mediante el idpersona.
	Dajaxice.BuscadorPersonas.obtener_Persona_IdPersona(cargarFormularioPersona, {'idPersona':idPersona});
	buscarTelefonosConIdPersona(idPersona);
	buscarDireccionesConIdPersona(idPersona);
	return false;
}

function cargarFormularioPersona(dato){ // Función que manda a cargar en fisica.html o moral.html la información encontrada en buscarPersonaConIdPersona.
	
	if(dato.personas)
	{
		var persona = dato.personas[0];
		
		if (persona.TipoPersona == 'F')
		{
			cargarPersonaFisicaEnFormulario(persona);
		}
		else
		{
			cargarPersonaMoralEnFormulario(persona);
			buscarSocioMoral(persona.IdPersona);
		}
	}
	else
	{
		alert('No se encontro información');
	}
}
