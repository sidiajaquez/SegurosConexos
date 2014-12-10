$(function () {
	$.datepicker.regional['es'] = {
			closeText: 'Cerrar',
			prevText: ' nextText: Sig>',
			currentText: 'Hoy',
			monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
			'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
			monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
			'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
			dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
			dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mié;', 'Juv', 'Vie', 'Sáb'],
			dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
			weekHeader: 'Sm',
			dateFormat: 'dd/mm/yy',
			firstDay: 1,
			isRTL: false,
			showMonthAfterYear: false,
			yearSuffix: ''
		};	
	
	$.datepicker.setDefaults($.datepicker.regional["es"]);
});

function obtieneDatosTabla(tabla){ //Función para obtener los datos de una tabla en un arreglo
	var renglonData = [];
	var renglon = 0;
	var columna = 0;
	$(tabla.concat(' tbody')).children('tr').each(function(indice){
		renglonData [renglon] = [];
		$(this).children('td').each(function(indice2){
			renglonData[renglon][columna++] = $(this).text();
		});
		renglon++;
		columna = 0;
	});
	return renglonData;	
}

function validarArrayVacio(array){
	if (array.length == 0)
	{
		return '';
	}
	return array.join(';');
}

function recargarPagina(){ // Función que se encarga de recargar la pagina
	location.reload();	
}

function fechaActual(){ // Función que genera 
	var currentTime = new Date();
	var day = ("0" + currentTime.getDate()).slice(-2);
	var month = ("0" + (currentTime.getMonth()+1)).slice(-2);
	var year = currentTime.getFullYear();
	
	return (day+'/'+month+'/'+year);
}

var formatCurrency = function(total) // Función que nos permite darle formato a una cantidad.
{
    var neg = false;
    
    if(total < 0) 
    {
        neg = true;
        total = Math.abs(total);
    }
    return parseFloat(total, 10).toFixed(4).replace(/(\d)(?=(\d{3})+\.)/g, "$1,").toString();
}

var replaceAll = function(text, busca, reemplaza) // Función que nos permite remplazar los caracteres de un string.
{
	while (text.toString().indexOf(busca) != -1)	
	text = text.toString().replace(busca,reemplaza);
	
	return text;	
}