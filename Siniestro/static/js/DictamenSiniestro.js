$(document).on('ready',inicio);

function inicio(){ // Función que inicia las variables y los eventos de los controles
	$.ajaxSetup({
		beforeSend: function(xhr, settings){
			if (settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});
	
	$('#btnGuardarDictamenSiniestro').on('click', guardarDictamenSiniestro);
	
	//Configuracion de los chosen
	$(".chosen-select-deselect").chosen({allow_single_deselect:true,no_results_text:'No se encontro'});
	$(".chosen-select-deselect").chosen().change(function(evt,params){
		if (params){
			//alert(params.selected);
		}
	});
	//Configuracion de los radio
	$("input[name=ProcedenteImprocedente]").click(function () {    
		if ($(this).val() == 'Procedente'){
			$("#cmbCausaNegativa").prop('disabled',true).trigger("chosen:updated");
			$("#cmbCausaNegativa").val('').trigger("chosen:updated");
		}else{
			$("#cmbCausaNegativa").prop('disabled',false).trigger("chosen:updated");
		}
	});
}

var guardarDictamenSiniestro = function(){
	var j = {nombre:"prueba"};
	$.post('GuardarDictamenSiniestro/',{data:JSON.stringify(j)}, callback_prueba);
}

var callback_prueba = function(data){
	alert(data.nada);
}

Dropzone.options.frmDictamenSiniestro = {
	maxFilesize:1, //1 mb de tamaño maximo permitido
	paramName: "file", //Nombre de la variable que almacena las imagenes utilizado en la vista
	maxFiles:4, //maximos archivos permitidos
	autoProcessQueue:false, //deshabilita el auto upload de las imagenes para subirlas al momento de guardar el dictamen
	acceptedFiles:"image/*", //Tipos de archivos aceptados
	parallelUploads: 4, //Numero de archivos a subir
	init:function(){
		myDropzone = this;

		var submitButton = document.querySelector("#btnGuardarDictamenSiniestro");
		
		submitButton.addEventListener("click",function(){
			myDropzone.processQueue(); //Subir archivos al hacer clic en submit-all
		});
		
		this.on("success", function(file, responseText){
			file.previewTemplate.children.removeImage.disabled=true; //bloquear los botones de quitar imagen de cada una
		});
	
		this.on("addedfile", function(file){ //despues de agregar una imagen se adjunta el boton quitar imagen
			var removeButton = Dropzone.createElement("<button id='removeImage'>Quitar Imagen</button>");
			removeButton.addEventListener("click",function(e){
				e.preventDefault();
				e.stopPropagation();
				myDropzone.removeFile(file);
			});
			file.previewElement.appendChild(removeButton);
		});
	}
};