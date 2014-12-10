$(document).on('ready',inicio);

function inicio(){ //Función que inicia las variables y los eventos de los controles del listado de solicitudes
	activarMenu();
	$('#btnPagarConstancia').on('click',pagarConstancia);
	$('#btnCancelar').on('click',listadoPagoConstancias);
	$("#btnImprimir").on('click',imprimirRecibo);
	$("#btnCartaNoSiniestro").on('click',cartaNoSiniestro);
	rehabilitarConstancia();
}

var cartaNoSiniestro = function(){ //Funcion para imprimir en las constancias rehabilitadas la carta de no siniestro
	window.open('/CartaNoSiniestro/'+$("#varIdConstancia").val());
}

var rehabilitarConstancia = function(){ //Funcion para preguntar si se desea rehabilitar la constancia en dado caso que venga del listado rehabilitar constancias canceladas
	if ($("#varRehabilitarConstancia").val() == 'True'){
		alertify.set({ labels: {
		    ok     : "Si",
		    cancel : "No"
		}});
		alertify.confirm("¿Rehabilitar Constancia?", function (e) {
		    if (e) {
		    	Dajaxice.Cobranza.rehabilitar_constancia(Dajax.process,{'idConstancia':$('#varIdConstancia').val(),'idSolicitud':$('#varIdSolicitud').val()});
		    	alertify.success("Constancia rehabilitada");
		    }else{
		    	location.href = '/ListadoRehabilitarConstanciasCanceladas/';
		    }
		});		
	}
}

var mensajeFolioRehabilitacion = function(folioEndosoRehabilitacion){ //Funcion que recibe el numero de folio del endoso de la funcion Dajaxice.Cobranza.rehabilitar_constancia para mostrarla en un alert
	alertify.alert('Endoso generado con el Folio: '+ folioEndosoRehabilitacion);
}

var activarMenu = function(){ // Función que agrega la clase active al menu principal para saber en que parte se esta trabajando del sistema
	$('.menu_principal li:first-child').removeClass('active');
	$('.menu_principal li:eq(26)').addClass('active');	
}

var generarCartaConstancia = function (){ //Funcion que manda a generar el pdf de la carta de la constancia
	window.open('/CartaConstancia/'+$("#varIdConstancia").val());
}

var pagarConstancia = function() { //Funcion que genera el pago de la constancia
	if ($('#FormaPago').val()!=''){
		alertify.set({ labels: {
		    ok     : "Si",
		    cancel : "No"
		}});		
		alertify.confirm("¿Pagar Constancia?", function (e) {
		    if (e) {
				Dajaxice.Cobranza.guardar_pago_constancia(Dajax.process,{'idConstancia':$('#varIdConstancia').val(),'formaPago':$('#FormaPago').val()});
				//alertify.success('Constancia pagada');
				$('#btnCancelar').text('Volver al Listado');
				$('.tblFormaPago tbody').children('tr').children('td')[1].innerText = $('#FormaPago').val();
				$('#btnPagarConstancia').attr('disabled',true);
				$('#btnImprimir').attr('disabled',false);
				$('#btnCartaConstancia').attr('disabled',false);
		    }
		});
	}else{
		alertify.alert('Falta especificar la forma de pago');
	}
	return false;	
}

var imprimirRecibo = function() { // Función que llama a la vista previa de la impresion representando la tecla ctrl + P.
	window.print();
}

var folioRecibo = function (folio){ //Funcion que obtiene el folio para agregarlo al formato de pago
	$('.tblFolio tbody').children('tr').children('td')[0].innerText = folio;
}

var listadoPagoConstancias = function() { //Si se cancela se regresa solamente al listado de las constancias
	if ($("#varRehabilitarConstancia").val() == 'True' || $("#varIdEstatusConstancia").val() == 3){
		location.href = '/ListadoRehabilitarConstanciasCanceladas/';
	}else{
		location.href = '/ListadoCobroConstancias/';
	}
}