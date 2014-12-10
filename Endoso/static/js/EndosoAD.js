$(document).on('ready',inicio);

function inicio(){ // Función que inicia las variables y los eventos de los controles
	$("#FechaBien").val(fechaActual());
	$("#FechaBien").datepicker({
		firstDay: 1
	});
	$("#btnAgregarBienModal").on("click",limpiarModalAgregarBien);
	$("#btnAceptarBienEditable").on("click",modificarBien);
	$("#ValorUnitario").mask("000,000,000,000,000.00", {reverse:true});
	$("#Cantidad").mask("000,000,000,000,000", {reverse:true});
	$("#btnAgregarBien").on("click",agregarBienTabla);
	$("#btnVolverListadoEndoso").on("click",volverListadoEndoso);
	$("#btnGuardarEndoso").on("click",guardarEndoso);
	$("#btnImprimirEndoso").on("click",imprimirEndoso);
	modalDescripcionBienes();
	activarMenu();
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema.
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(15)').addClass('active');
}

var guardarEndoso = function(){ //Function para guardar el Endoso
	if(pasarComprobaciones()){
		descripcionContenidos = obtieneDatosTabla (".tblDescripcionDetalladaBien");
		var datosEndoso = new Object();
		datosEndoso.idConstancia = $("#varIdConstancia").val();
		datosEndoso.idSolicitudEndoso = $("#varIdSolicitudEndoso").val();
		datosEndoso.SumaAseguradaAnterior = replaceAll($("#SumaAseguradaAnterior").val(),",","");
		datosEndoso.SumaAseguradaActual = replaceAll($("#SumaAseguradaTotal").val(),",","");
		datosEndoso.SumaAseguradaEndoso = replaceAll($("#SumaAseguradaTotal").val(),",","");
		datosEndoso.TipoEndoso = $("#varIdTipoEndoso").val();
		Dajaxice.Endoso.guardar_endoso_ad(Dajax.process,{'contenidos':validarArrayVacio(descripcionContenidos),'datosEndoso':datosEndoso});
	}else{
		if ($("#varIdTipoEndoso").val() == "AUMENTO"){
			alertify.alert("Se requiere tener Aumento en la Suma Asegurada Total");
		}else{
			alertify.alert("Se requiere tener Disminución en la Suma Asegurada Total");
		}
	}
	return false;
}

var mensajeSolicitud = function(numeroEndoso){ //Funcion que recibe el folio del endoso de la funcion Dajaxice.Endoso.guardar_endoso_ad para mostrarla en un alert
	if (numeroEndoso){
		alertify.set({ labels: {
		    ok     : "Si",
		    cancel : "No"
		}});
		$("#varIdControlEndoso").val(numeroEndoso[1]);
		$("#btnImprimirEndoso").attr('disabled',false);
		$("#btnGuardarEndoso").attr('disabled',true);
		$("#btnAgregarBienModal").attr('disabled',true);
		$(".btn-group").css("display", "none");
		$(".icon-remove").css("display", "none");
		alertify.confirm('Número de Endoso: '+ numeroEndoso[0] + ' ¿Desea imprimirlo?', function (e) {
		    if (e) {
		    	imprimirEndoso();
		    }
		});
	}else{
		alertify.alert('Error al guardar contacte al administrador del sistema');
	}
	return false;
}

var imprimirEndoso = function(){ //Se redirecciona al formato en pdf para imprimir el endoso de aumento/disminucion
	window.open('/EndosoADImpresion/'+$("#varIdControlEndoso").val());
	return false;
}

var pasarComprobaciones = function(){ //Comprobar el formulario de Endoso para guardar la informacion
	sumaAseguradaAnterior = replaceAll($("#SumaAseguradaAnterior").val(),",","");
	sumaAseguradaTotal = replaceAll($("#SumaAseguradaTotal").val(),",","");
	//Se hace la comprobacion del formulario para un endoso de aumento
	if ($("#varIdTipoEndoso").val() == "AUMENTO"){
		if (sumaAseguradaAnterior >= sumaAseguradaTotal){
			return false;
		}
	}else{ //Se hace la comprobacion del formulario para un endoso de disminucion
		if (sumaAseguradaTotal <= sumaAseguradaAnterior){
			return false;
		}		
	}
	return true;
}

var volverListadoEndoso = function(){ //Funcion para direccionar al listado de los endosos
	if ($("#varIdTipoEndoso").val() == "AUMENTO"){ 
		location.href= '/ListadoAumentoEndoso/';
	}else{
		location.href= '/ListadoDisminucionEndoso/';
	}
	return false;	
}

var agregarBienTabla = function(){ //Funcion que agrega la descripcion del Bien en la tabla de los bienes
	var contenido = $('.tblDescripcionDetalladaBien tbody');
	
	if (validarModalDescripcionBienes()){
		cantidad = replaceAll($("#Cantidad").val(),",","");
		valorUnitario = replaceAll($("#ValorUnitario").val(),",","");
		sumaAsegurada = cantidad * valorUnitario;		
		$("#SumaAseguradaBienTemporal").val(sumaAsegurada.toFixed(2));
		$("#SumaAseguradaBienTemporal").mask("000,000,000,000,000.00", {reverse:true});
		$("<tr><td style='display:none;'></td><td>"+$("#NombreEquipo").val().toUpperCase()+"</td><td>"+$("#Marca").val().toUpperCase()+"</td><td>"+$("#Modelo").val().toUpperCase()+"</td><td>"+$("#Serie").val().toUpperCase()+"</td><td>"+$("#DocumentacionEvaluacion").val()+"</td><td>"+$("#FechaBien").val()+"</td><td style='display:none;'>"+cantidad+"</td><td style='display:none;'>"+valorUnitario+"</td><td>"+$("#Cantidad").val()+"</td><td>"+$("#ValorUnitario").val()+"</td><td>"+$("#SumaAseguradaBienTemporal").val()+"</td><td><a onclick='quitarBienAumento($(this),2);'><i class='icon-remove'></i></a></td></tr>").appendTo(contenido);
		recalcularSumaAsegurada();
		$(".close").click();
	}
}

var validarModalDescripcionBienes = function(){ //permite validar la ventana modal para agregar la descripcion detallada de los bienes o contenidos
	if ($("#NombreEquipo").val() == '' || $("#DocumentacionEvaluacion").val() == '' || $("#Cantidad").val() == '' || $("#ValorUnitario").val() == ''){
		alertify.alert("Faltan datos por especificar");
		return false;
	}
	return true;
}

var quitarBienAumento = function(quitarRegistro,opcion){ //Quita el bien de la tabla descripcion detallada de los bienes para un endoso de aumento
	var rowData = quitarRegistro.closest("tr");
	sumaAseguradaQuitar = replaceAll(rowData.children('td')[11].innerText,",","");
	sumaAseguradaTotal = replaceAll($("#SumaAseguradaTotal").val(),",","");
	sumaAseguradaAnterior = replaceAll($("#SumaAseguradaAnterior").val(),",","");
	if ((parseFloat(sumaAseguradaTotal) - parseFloat(sumaAseguradaQuitar)) > parseFloat(sumaAseguradaAnterior)){
		opcionQuitarBien(quitarRegistro,opcion);
	}else{
		alertify.confirm("Si elimina este bien necesitara aumentar la suma asegurada,  ¿Desea continuar?", function (e) {
		    if (e) {
		    	opcionQuitarBien(quitarRegistro,opcion);
		    }
		});			
	}
	return false;	
}

var quitarBienDisminucion = function(quitarRegistro,opcion){ //Quita el bien de la tabla descripcion detallada de los bienes para un endoso de disminucion
	var rowData = quitarRegistro.closest("tr");
	sumaAseguradaQuitar = replaceAll(rowData.children('td')[11].innerText,",","");
	sumaAseguradaTotal = replaceAll($("#SumaAseguradaTotal").val(),",","");
	sumaAseguradaAnterior = replaceAll($("#SumaAseguradaAnterior").val(),",","");
	if ((parseFloat(sumaAseguradaTotal) - parseFloat(sumaAseguradaQuitar)) >0 ){
		opcionQuitarBien(quitarRegistro,opcion);
	}else{
		alertify.alert("No puede eliminar este bien, la Suma Asegurada debe ser mayor a 0");
	}
	return false;	
}

var opcionQuitarBien = function(quitarRegistro,opcion){ //Funcion para quitar el bien dependiendo si viene de un registro modificado o nuevo
	if (opcion == 1){
		quitarRegistro.parent().parent().parent().parent().parent().remove();
	}else{
		quitarRegistro.parent().parent().remove();
	}
	recalcularSumaAsegurada();
}

var limpiarModalAgregarBien = function(){ //Funcion que Limpia los campos de texto de la ventana modal
	$("#NombreEquipo").val('');
	$("#Marca").val('');
	$("#Modelo").val('');
	$("#Serie").val('');
	$("#DocumentacionEvaluacion").val('');
	$("#Cantidad").val('');
	$("#ValorUnitario").val('');
	$("#FechaBien").val(fechaActual());
	$("#btnAceptarBienEditable").css("display","none");
	$("#btnAgregarBien").css("display","inline");
	//se habilitan las cajas de texto de la ventana modal
	habilitarControlesModal(false);	
}

var modalDescripcionBienes = function(){ //Manejo del Focus en la ventana modal para agregar la descripcion detallada de los bienes asegurados
	$("#mdlDescripcionBien").on('shown', function() {
		$("#Cantidad").focus();
	    $("#NombreEquipo").focus();
	});
}

var editarBienModal = function(editarRegistro){ //Funcion que permite editar los datos de la tabla de la descripcion de los bienes en la ventana modal
	var bienEditable = new bienAsegurable(editarRegistro);
	$("#idBien").val(bienEditable.idBien);
	$("#NombreEquipo").val(bienEditable.nombreEquipo);
	$("#Marca").val(bienEditable.marca);
	$("#Modelo").val(bienEditable.modelo);
	$("#Serie").val(bienEditable.noSerie);
	$("#DocumentacionEvaluacion").val(bienEditable.documentacion);
	$("#FechaBien").val(bienEditable.fechaBien);
	$("#Cantidad").val(bienEditable.cantidad);
	$("#ValorUnitario").val(bienEditable.valorUnitario);
	$("#btnAgregarBien").css("display","none");
	$("#btnAceptarBienEditable").css("display","inline");
	//se desabilitan las cajas de texto, solamente se dejan activadas la cantidad y el valor unitario
	habilitarControlesModal(true);
}

var bienAsegurable = function (data){ //Clase para definir los atributos del bien asegurable
	var rowData = data.closest("tr");
	this.idBien = rowData.children('td')[0].innerText;
	this.nombreEquipo = rowData.children('td')[1].innerText;
	this.marca = rowData.children('td')[2].innerText;
	this.modelo = rowData.children('td')[3].innerText;
	this.noSerie = rowData.children('td')[4].innerText;
	this.documentacion = rowData.children('td')[5].innerText;
	this.fechaBien = rowData.children('td')[6].innerText;
	this.cantidad = rowData.children('td')[9].innerText;
	this.valorUnitario = rowData.children('td')[10].innerText;
}

var habilitarControlesModal = function(enabled){ //Funcion para habilitar y deshabilitar los controles de la ventana modal para agregar bienes
	$("#NombreEquipo").prop("disabled",enabled);
	$("#Marca").prop("disabled",enabled);
	$("#Modelo").prop("disabled",enabled);
	$("#Serie").prop("disabled",enabled);
	$("#DocumentacionEvaluacion").prop("disabled",enabled);
	$("#FechaBien").prop("disabled",enabled);	
}

var modificarBien = function () { //Funcion para aceptar la modificacion del bien una vez que se modifiquen sus valores
	$('.tblDescripcionDetalladaBien tbody').children('tr').each(function(indice){
		$(this).children('td').each(function(indice2){
			switch(indice2){
				case 0:
					if ($(this).text() == $("#idBien").val()){ //Se edita el renglon de la tabla
						//Guarda en un arreglo los valores anteriores de la tabla para comprobar si se realiza el endoso de aumento
						var valoresAnterioresTabla = new Array();
						valoresAnterioresTabla[0] = $(this).parent().children('td')[7].innerText;
						valoresAnterioresTabla[1] = $(this).parent().children('td')[8].innerText;
						valoresAnterioresTabla[2] = $(this).parent().children('td')[9].innerText;
						valoresAnterioresTabla[3] = $(this).parent().children('td')[10].innerText;
						valoresAnterioresTabla[4] = $(this).parent().children('td')[11].innerText;
						valoresAnterioresTabla[5] = $("#SumaAseguradaTotal").val();
						
						$(this).parent().children('td')[1].innerText = $("#NombreEquipo").val().toUpperCase();
						$(this).parent().children('td')[2].innerText = $("#Marca").val().toUpperCase();
						$(this).parent().children('td')[3].innerText = $("#Modelo").val().toUpperCase();
						$(this).parent().children('td')[4].innerText = $("#Serie").val().toUpperCase();
						$(this).parent().children('td')[5].innerText = $("#DocumentacionEvaluacion").val();
						$(this).parent().children('td')[6].innerText = $("#FechaBien").val();
						cantidad = replaceAll($("#Cantidad").val(),",","");
						valorUnitario = replaceAll($("#ValorUnitario").val(),",","");
						sumaAsegurada = cantidad * valorUnitario;							
						$("#SumaAseguradaBienTemporal").val(sumaAsegurada.toFixed(2));
						$("#SumaAseguradaBienTemporal").mask("000,000,000,000,000.00", {reverse:true});						
						$(this).parent().children('td')[7].innerText = cantidad;
						$(this).parent().children('td')[8].innerText = valorUnitario;
						$(this).parent().children('td')[9].innerText = $("#Cantidad").val();
						$(this).parent().children('td')[10].innerText = $("#ValorUnitario").val();
						$(this).parent().children('td')[11].innerText = $("#SumaAseguradaBienTemporal").val();
						recalcularSumaAsegurada();
						sumaAseguradaTotal = replaceAll($("#SumaAseguradaTotal").val(),",","");
						sumaAseguradaAnterior = replaceAll($("#SumaAseguradaAnterior").val(),",","");
						
						//Condicion para endoso aumento
						if ($("#varIdTipoEndoso").val() == "AUMENTO"){
							if(parseFloat(sumaAseguradaTotal) > parseFloat(sumaAseguradaAnterior)){
								$(".close").click();
							}else{
								alertify.alert("La suma asegurada debe ser mayor a la suma asegurada anterior: " + $("#SumaAseguradaAnterior").val());
								//Se regresan los valores como estaban anteriormente
								regresarValoresContenidoBienes($(this),valoresAnterioresTabla);
							}
						}else{ //Endoso de Disminucion
							if (parseFloat(sumaAseguradaTotal) > 0){
								if(parseFloat(sumaAseguradaTotal) < parseFloat(sumaAseguradaAnterior)){
									$(".close").click();
								}else{
									alertify.alert("La suma asegurada debe ser menor a la suma asegurada anterior: " + $("#SumaAseguradaAnterior").val());
									//Se regresan los valores como estaban anteriormente
									regresarValoresContenidoBienes($(this),valoresAnterioresTabla);										
								}
							}else{
								alertify.alert("La suma asegurada debe sermayor a cero");
								//Se regresan los valores como estaban anteriormente
								regresarValoresContenidoBienes($(this),valoresAnterioresTabla);
							}
						}					
					}
					break;
			}
		});
	});
}

var regresarValoresContenidoBienes = function(Bien,valoresAnteriores){ //Funcion que regresa los valores de la tabla de la descripcion de los bienes
	Bien.parent().children('td')[7].innerText = valoresAnteriores[0];
	Bien.parent().children('td')[8].innerText = valoresAnteriores[1];
	Bien.parent().children('td')[9].innerText = valoresAnteriores[2];
	Bien.parent().children('td')[10].innerText = valoresAnteriores[3];
	Bien.parent().children('td')[11].innerText = valoresAnteriores[4];
	$("#SumaAseguradaTotal").val(valoresAnteriores[5]);	
}

var recalcularSumaAsegurada = function (){ //Funcion que recalcula la cantidad de suma asegurada
	sumaAseguradaAcumulada = 0;
	$('.tblDescripcionDetalladaBien tbody').children('tr').each(function(i){
		$(this).children('td').each(function(i2){
			switch(i2){
				case 11:
					sumaAseguradaBien = replaceAll($(this).text(),",","");
					sumaAseguradaAcumulada = parseFloat(sumaAseguradaAcumulada) + parseFloat(sumaAseguradaBien);
			}
		});
	});						
	$("#SumaAseguradaTotal").val(sumaAseguradaAcumulada.toFixed(2));
	$("#SumaAseguradaTotal").mask("000,000,000,000,000.00", {reverse:true});	
}

function replaceAll( text, busca, reemplaza ){ //Reemplaza todos los caracteres que se encuentren en una cadena de texto
	while (text.toString().indexOf(busca) != -1)
		text = text.toString().replace(busca,reemplaza);
	return text;
}