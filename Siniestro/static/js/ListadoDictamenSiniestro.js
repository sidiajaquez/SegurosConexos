$(document).on('ready',inicio)

function inicio(){	// Función que inicia las variables y los eventos de los controles del listado de solicitudes.
	activarMenu();
	buscarActasSiniestro();
	$("#txtBuscarActaSiniestro").focus();
}

function activarMenu(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(40)').addClass('active');
}

var buscarActasSiniestro = function(){ //Funcion que carga las actas de siniestro
	Dajaxice.Siniestro.CargarActasSiniestro(cargarActasSiniestro);
}

var cargarActasSiniestro = function(data){ //Callback de la funcion cargarActasSiniestro
	if(data.ActasSiniestro.length>0)
	{
		var items = [];
		
		data.ActasSiniestro.forEach(function (campo, valor){
			items.push({IdActaSiniestro:campo[0],ActaSiniestro:"Acta: "+campo[1],FolioAviso:"Aviso: "+campo[2],FolioInspeccion:"Inspeccion: "+campo[3],
				FolioConstancia:"Constancia: "+campo[4],FechaSiniestro:"Fecha Siniestro: "+ campo[5],Asegurado:"Asegurado: "+campo[7],IdConstancia:campo[6]});
		});
	
		options = {
		        item: "<li><div style='display: none;'><span class='IdActaSiniestro'></span></div><div style='display: none;'><span class='IdConstancia'></span></div>" +
		        		"<div class='row'>" +
		        		"<span class='ActaSiniestro tituloPrincipal span2'></span>" +
		        		"<span class='FolioInspeccion span2'></span>" +
		        		"<span class='FolioAviso span2'></span>" +
		        		"<span class='FechaSiniestro span3'></span>" +
		        		"</div>" +
		        		"<div class='row'><span class='FolioConstancia Subtitulo span4'></span>" +
		        		"<span class='Asegurado span5'></span>" +
		        		"<span class='offset1'><a href='#' title='Generar Dictamen' onclick='generarDictamen($(this));'><i class='icon-briefcase'></i></a></span>" +
		        		"</div>" +
		        		"</li>",
		        valueNames: [ 'IdActaSiniestro','ActaSiniestro','FolioAviso','FolioInspeccion','FolioConstancia','FechaSiniestro','Asegurado','IdConstancia' ],
		        plugins: [
		            [ 'fuzzySearch' ]
		        ]
		};		
		
	    var featureList = new List('lovely-things-list', options, items);

	    $('.search-fuzzy').keyup(function() {
	        featureList.fuzzySearch($(this).val());
	    });		
	}
	else
	{
		alertify.alert('No se encontraron actas de siniestro para dictaminar');
	}		
}

var generarDictamen = function(idActaSiniestro){ //Funcion que toma el IdActaSiniestro para generar el template del dictamen
	actaSeleccionada = idActaSiniestro.closest("li");
	id_ActaSiniestro = actaSeleccionada.children()[0].innerText;
	location.href = '/DictamenSiniestro/' + id_ActaSiniestro;
}