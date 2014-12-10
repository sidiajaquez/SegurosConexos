#encoding:utf-8
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from ConexosAgropecuarios.forms import PersonaMoralForm, PersonaFisicaForm, RegistroFondoForm
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from ConexosAgropecuarios.models import Persona, Telefono, SocioMoral, DatosFondo, RegistroFondo, Municipio, CuentaFondo, Bancos, ContratoFondo, Reaseguradora, MiembroConsejoAdministracion, PersonalApoyo, Estado, AreaInfluencia, ContratoReaseguro, Moneda
from Cobranza.models import PagoConstancia
from Direcciones.models import Direccion
from Programas.models import Programa
import datetime
from django.db.models import Q

@dajaxice_register
def obtenerDatosContratoFondo(request, idContratoFondo): #metodo para obtener el tipo de moneda segun el contrato de retrosecion que tenga el fondo (para la programacion)
    datosContratoFondo = ContratoFondo.objects.filter(IdContratoFondo = idContratoFondo) 
    datos = list()

    for contrato in datosContratoFondo:
        if contrato.IdMoneda == 3:
            monedas = Moneda.objects.using('catalogos').filter(IdMoneda__in=[1,2])
            for moneda in monedas:
                datos.append({'IdMoneda':moneda.IdMoneda,'DescripcionMoneda':moneda.Descripcion})
        else:
            moneda = Moneda.objects.using('catalogos').get(IdMoneda=contrato.IdMoneda)
            datos.append({'IdMoneda':moneda.IdMoneda,'DescripcionMoneda':moneda.Descripcion})
    
    return simplejson.dumps({'DescripcionMoneda':datos})


@dajaxice_register
def guardar_persona_fisica(request, formulario, telefonos, indicadorEsSocio, direcciones):# Metodo que recibe el formulario de persona fisica obtenido de fisica.html y lo deserializa para obtener la información de sus controles y lo valida con PersonaFisciaForm, si la información es valida guarda los datos y limpia los controles del formulario mediante una función de js.
    dajax = Dajax()
    
    if telefonos == '':
        list_Telefonos = ''
    else:        
        array_convertido_string = simplejson.dumps(telefonos, separators=('|',','))
        list_Telefonos = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')  
    
    if direcciones == '':
        listaDirecciones = ''
    else:
        arrayConvertidoStringDirecciones = simplejson.dumps(direcciones, separators=('|',','))
        listaDirecciones = arrayConvertidoStringDirecciones.replace('[', '').replace(']', '').replace('"', '').split(';')
                      
    formulario_deserializado = deserialize_form(formulario) 
    
    if formulario_deserializado.get('varIdPersona') == '':              
        
        if not Persona.objects.filter(Curp = formulario_deserializado.get('Curp')).exists():
            
            fechaIngreso = datetime.datetime.now()
    
            if indicadorEsSocio == 0:
                fechaIngreso = None
        
            datos = {'Rfc':formulario_deserializado.get('Rfc'),'Curp':formulario_deserializado.get('Curp'),'PrimerNombre':formulario_deserializado.get('PrimerNombre'),
                     'SegundoNombre':formulario_deserializado.get('SegundoNombre'),'ApellidoPaterno':formulario_deserializado.get('ApellidoPaterno'),
                     'ApellidoMaterno':formulario_deserializado.get('ApellidoMaterno'),'FechaNacimiento':datetime.datetime.strptime(formulario_deserializado.get('FechaNacimiento'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                     'Email':formulario_deserializado.get('Email'), 'EstadoCivil':formulario_deserializado.get('EstadoCivil'), 'Sexo':formulario_deserializado.get('Sexo')}
            formulario = PersonaFisicaForm(datos)
            
            if formulario.is_valid():
                persona_fisica = Persona(Rfc = formulario_deserializado.get('Rfc').upper(), Curp = formulario_deserializado.get('Curp').upper(), PrimerNombre = formulario_deserializado.get('PrimerNombre').upper(),
                                       SegundoNombre = formulario_deserializado.get('SegundoNombre').upper(), ApellidoPaterno = formulario_deserializado.get('ApellidoPaterno').upper(), 
                                       ApellidoMaterno = formulario_deserializado.get('ApellidoMaterno').upper(),  FechaNacimiento = datetime.datetime.strptime(formulario_deserializado.get('FechaNacimiento'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                                        Email = formulario_deserializado.get('Email').upper(), EstadoCivil = formulario_deserializado.get('EstadoCivil').upper(), Sexo = formulario_deserializado.get('Sexo').upper(), EsSocio = indicadorEsSocio, FechaIngreso = fechaIngreso, TipoPersona = 'F')
                persona_fisica.save()   
                
                if listaDirecciones != '':
                    for direccion in listaDirecciones:
                        guardar_direcciones(direccion, persona_fisica.IdPersona)
                
                if list_Telefonos != '':
                    for registro in list_Telefonos:
                        guardar_Telefonos(registro, persona_fisica.IdPersona)          
                        
                dajax.add_data(persona_fisica.IdPersona, 'mensajePersonaFisica')
            else:
                dajax.alert('Formulario invalido')
                dajax.script('limpiar_Formulario();')
        else:           
            dajax.alert('El registro ya se encuentra')
    else:
        actualizar_Datos_Persona_Fisica(formulario_deserializado, list_Telefonos, indicadorEsSocio, listaDirecciones)
         
    return dajax.json()

@dajaxice_register
def guardar_Telefonos(telefonoRecibido, idPersona): # Función que recibe una entidad con la información de teléfono y un id de persona para almacenarlos en la base de datos.
    dajax = Dajax()
    
    list_registro = telefonoRecibido.split(',')
    telefono = Telefono(TipoTelefono = list_registro[1], IdPersona_id = idPersona, Numero = list_registro[2])
    telefono.save()
        
    return dajax.json()

def guardar_direcciones(direccion, idPesona): # Función que recibe una entidad con la información de dirección y una variable que contiene el id de persona para almacenarlos en la base de datos.
    dajax = Dajax()
    
    listaDireccion = direccion.split(',')
    direccionMoral = Direccion(Persona_id = idPesona, TipoDireccion = listaDireccion[10], Detalle = codificarUTF8(listaDireccion[8]), Calle = codificarUTF8(listaDireccion[1]), NumeroExterior = listaDireccion[11],
                                NumeroInterior = listaDireccion[12], IdSepomex = listaDireccion[9])
    direccionMoral.save()
    return dajax.json()

def codificarUTF8(strDato): #Metodo para cambiar los caracteres especiales que vienen de javascript y ponerlos con acentos
    Utf = strDato.replace("\u00d1","Ñ")
    Utf = Utf.replace("\u00c1", "Á")
    Utf = Utf.replace("\u00c9", "É")
    Utf = Utf.replace("\u00cd", "Í")
    Utf = Utf.replace("\u00d3", "Ó")
    Utf = Utf.replace("\u00da", "Ú")
    
    return Utf
    
                  
def guardar_socioMoral(socioMoralRecibido, idPesona): # Función que recibe una entidad con la información de socios morales y el id persona de una moral para almacenarlos en la base de datos.
    dajax = Dajax()
    
    listaRegistro = socioMoralRecibido.split(',')
    socioMoral = SocioMoral(Persona_id = idPesona, SocioMoral = listaRegistro[1])
    socioMoral.save()
    
    return dajax.json()

@dajaxice_register
def actualizar_Datos_Persona_Fisica(formulario_deserializado, list_Telefonos, indicadorEsSocio, direcciones): #Función que permite actualizar los datos de una persona física, recibiendolos en  el formulario persona fisica de la plantilla fisica.html.
    dajax = Dajax()   
           
    fechaIngreso = datetime.datetime.now()
    
    if indicadorEsSocio == 0:
        fechaIngreso =  None        
           
    Persona.objects.filter(IdPersona=formulario_deserializado.get('varIdPersona')).update(Rfc = formulario_deserializado.get('Rfc').upper(), Curp = formulario_deserializado.get('Curp').upper(), PrimerNombre = formulario_deserializado.get('PrimerNombre').upper(),
                               SegundoNombre = formulario_deserializado.get('SegundoNombre').upper(), ApellidoPaterno = formulario_deserializado.get('ApellidoPaterno').upper(), 
                               ApellidoMaterno = formulario_deserializado.get('ApellidoMaterno').upper(),  FechaNacimiento = datetime.datetime.strptime(formulario_deserializado.get('FechaNacimiento'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                               Email = formulario_deserializado.get('Email').upper(), EstadoCivil = formulario_deserializado.get('EstadoCivil').upper(), Sexo = formulario_deserializado.get('Sexo').upper(), EsSocio = indicadorEsSocio, FechaIngreso = fechaIngreso)            
    
    if list_Telefonos != '':
        for registro in list_Telefonos:
            list_registro = registro.split(',')
            if list_registro[0] == '':
                guardar_Telefonos(registro, formulario_deserializado.get('varIdPersona'))   
    
    if direcciones != '':
        for direccion in direcciones:
            lista_Direccion = direccion.split(',')        
            if lista_Direccion[0] == '':
                guardar_direcciones(direccion, formulario_deserializado.get('varIdPersona'))       
 
    return dajax.json()
 
@dajaxice_register
def guardar_persona_moral(request, formulario, datosSociosMoral, direcciones, telefonos, indicadorEsSocio): #Método que recibe el formulario de moral.html, lo deserializa y lo valida contra el forms.py PersonaMoralForm que a su vez lo valida contra el modelo Persona, si es valido guarda los datos y ejecuta una funcion de js que limpia el formulario 
    dajax = Dajax()      

    if telefonos == '':
        list_Telefonos = ''
    else:        
        array_convertido_string = simplejson.dumps(telefonos, separators=('|',','))
        list_Telefonos = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')  
    
    if direcciones == '':
        listaDirecciones = ''
    else:
        arrayConvertidoStringDirecciones = simplejson.dumps(direcciones, separators=('|',','))
        listaDirecciones = arrayConvertidoStringDirecciones.replace('[', '').replace(']', '').replace('"', '').split(';')
        
    if datosSociosMoral == '':
        listaSociosMoral = ''
    else:
        arrayConvertidoStringSociosMoral = simplejson.dumps(datosSociosMoral, separators=('|',','))
        listaSociosMoral = arrayConvertidoStringSociosMoral.replace('[', '').replace(']', '').replace('"', '').split(';')
        
    formulario_deserializado = deserialize_form(formulario)
       
   
    datos = {'Rfc':formulario_deserializado.get('Rfc'),'RazonSocial':formulario_deserializado.get('RazonSocial'),'FechaNacimiento':datetime.datetime.strptime(formulario_deserializado.get('FechaNacimiento'),'%d/%m/%Y').strftime('%Y-%m-%d'),'Email':formulario_deserializado.get('Email')}
    formulario = PersonaMoralForm(datos)
    
    if formulario.is_valid():
        if formulario_deserializado.get('varIdPersona') == '':
            if not Persona.objects.filter(Rfc = formulario_deserializado.get('Rfc')).exists():    
                persona_moral = Persona (Rfc = formulario_deserializado.get('Rfc').upper(), RazonSocial = formulario_deserializado.get('RazonSocial').upper(), FechaNacimiento = datetime.datetime.strptime(formulario_deserializado.get('FechaNacimiento'),'%d/%m/%Y').strftime('%Y-%m-%d'), Email = formulario_deserializado.get('Email').upper(), TipoPersona= 'M', EsSocio= indicadorEsSocio)
                persona_moral.save()
                
                if listaSociosMoral != '':      
                    for registro in listaSociosMoral:
                        guardar_socioMoral(registro, persona_moral.IdPersona)
                
                if listaDirecciones != '':                                         
                    for direccion in listaDirecciones:
                        guardar_direcciones(direccion, persona_moral.IdPersona)
        
                if list_Telefonos != '':
                    for registro in list_Telefonos:
                        guardar_Telefonos(registro, persona_moral.IdPersona)         
                
                dajax.add_data(persona_moral.IdPersona, 'mensajePersonaMoral')  
            else:
                dajax.alert('El registro ya se encuentra')
            
        else:
            actualizar_Datos_Persona_Moral(formulario_deserializado, list_Telefonos, indicadorEsSocio, listaDirecciones, listaSociosMoral)  
    else:
        dajax.alert('Error: Faltan datos o la informacion es incorrecta')    
        
    return dajax.json()

@dajaxice_register
def actualizar_Datos_Persona_Moral(formulario_deserializado, list_Telefonos, indicadorEsSocio, direcciones, datosSociosMoral): #Función que permite actualizar los datos de una persona moral, recibiendolos en  el formulario persona moral de la plantilla moral.html.
    dajax = Dajax()    
           
    fechaIngreso = datetime.datetime.now()
    
    if indicadorEsSocio == 0:
        fechaIngreso = None        
           
    Persona.objects.filter(IdPersona=formulario_deserializado.get('varIdPersona')).update(Rfc = formulario_deserializado.get('Rfc').upper(), RazonSocial = formulario_deserializado.get('RazonSocial').upper(), FechaNacimiento = datetime.datetime.strptime(formulario_deserializado.get('FechaNacimiento'),'%d/%m/%Y').strftime('%Y-%m-%d'), Email = formulario_deserializado.get('Email').upper(), TipoPersona= 'M', EsSocio= indicadorEsSocio, FechaIngreso= fechaIngreso)            
    
    if datosSociosMoral != '':
        for datosSocio in datosSociosMoral:      
            list_socioMoral = datosSocio.split(',')
            if list_socioMoral[0] == '':  
                guardar_socioMoral(datosSocio, formulario_deserializado.get('varIdPersona'))
    
    if list_Telefonos != '':
        for registro in list_Telefonos:
            list_registro = registro.split(',')
            if list_registro[0] == '':
                guardar_Telefonos(registro, formulario_deserializado.get('varIdPersona'))
    
    if direcciones != '':
        for direccion in direcciones:
            lista_Direccion = direccion.split(',')
            if lista_Direccion[0] == '':
                guardar_direcciones(direccion, formulario_deserializado.get('varIdPersona'))         

    return dajax.json()

@dajaxice_register
def buscar_persona_socio(req,datosBuscar): #Recibe los datos de la funcion js buscarPersona y regresa los datos en json por medio de la variable personas
    dajax = Dajax()
    try:
        datos = list()
        personas = Persona.objects.filter((Q(Rfc__contains=datosBuscar) | Q(PrimerNombre__contains=datosBuscar) | Q(SegundoNombre__contains=datosBuscar) | Q(ApellidoPaterno__contains=datosBuscar) | Q(ApellidoMaterno__contains=datosBuscar)),Q(TipoPersona='F'))
            
        for persona in personas:
            datos.append({'IdPersona':persona.IdPersona,'Nombre':persona.PrimerNombre + " " + persona.SegundoNombre,'ApellidoPaterno':persona.ApellidoPaterno,'ApellidoMaterno':persona.ApellidoMaterno,'Rfc':persona.Rfc})
    except:
        return dajax.json()
    
    return simplejson.dumps({'personas':datos})

@dajaxice_register
def obtener_Telefonos_Persona(req, idPersona): #Función que busca los teléfonos de una persona pasando el idpersona.
    dajax = Dajax()
    try:
        telefonos = Telefono.objects.filter(IdPersona = idPersona)
        datos = list()
        for telefono in telefonos:
            datos.append({'IdTelefono':telefono.IdTelefono,'TipoTelefono':telefono.TipoTelefono,'Numero':telefono.Numero})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'telefonos':datos})

@dajaxice_register
def eliminar_Telefono(request, idTelefono): #Función que recibe el idTelefono con el cual se buscara el registro en la base de datos y se eliminara.
    dajax = Dajax()
    Telefono.objects.filter(IdTelefono = idTelefono).delete()
    
    return dajax.json()    

@dajaxice_register
def obtener_socios_personamoral_idpersona(req, idPersona): #Función que busca los socios de las personas morales.
    dajax = Dajax()
    try:
        socioMorales = SocioMoral.objects.filter(Persona_id = idPersona)
        datos = list()
        for socioMoral in socioMorales:  
            personasSociosMorales = Persona.objects.filter(IdPersona = socioMoral.SocioMoral)  # Se busca los datos de la persona que es socio de la persona moral.
            personaSocioMoral = personasSociosMorales[0] 
            fecha = personaSocioMoral.FechaNacimiento.strftime("%d/%m/%Y")
            datos.append({'IdSocioMoral': socioMoral.IdSocioMoral, 'IdPersona':personaSocioMoral.IdPersona,'PrimerNombre':personaSocioMoral.PrimerNombre,
            'SegundoNombre':personaSocioMoral.SegundoNombre,'ApellidoPaterno':personaSocioMoral.ApellidoPaterno,
            'ApellidoMaterno':personaSocioMoral.ApellidoMaterno,'Rfc':personaSocioMoral.Rfc,'Curp':personaSocioMoral.Curp,'Sexo':personaSocioMoral.Sexo,
            'Email':personaSocioMoral.Email,'EstadoCivil':personaSocioMoral.EstadoCivil,'FechaNacimiento': str(fecha), 'EsSocio':personaSocioMoral.EsSocio,
            'TipoPersona':personaSocioMoral.TipoPersona,'RazonSocial':personaSocioMoral.RazonSocial})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'personasSocioMoral':datos})   
    
@dajaxice_register
def eliminar_socioMoral(request, idSocioMoral): #Función que recibe el idSocioMoral con el cual se buscará el registro en la base de datos y se eliminara.
    dajax = Dajax()
    SocioMoral.objects.filter(IdSocioMoral = idSocioMoral).delete()
    
    return dajax.json()   

@dajaxice_register
def guardar_datos_fondo(request, formularioFondo, municipiosDatosFondo, cuentasFondo, contratosFondo, miembrosConsejoFondo, personasApoyoFondo):# Método que recibe el formulario de los datos generales obtenido de datosFondo.html y lo deserializa para obtener la información de sus controles y lo valida con DatosFondoForm, si la información es valida guarda los datos y limpia los controles del formulario mediante una función de js.
    dajax = Dajax()
    formulario_deserializado = deserialize_form(formularioFondo) 
    
    if municipiosDatosFondo == '':
        list_Municipios = ''
    else:        
        array_convertido_string = simplejson.dumps(municipiosDatosFondo, separators=('|',','))
        list_Municipios = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')  
        
    if cuentasFondo == '':
        list_CuentasFondo = ''
    else:        
        array_convertido_string = simplejson.dumps(cuentasFondo, separators=('|',','))
        list_CuentasFondo = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
        
    if contratosFondo == '':
        list_ContratosFondos = ''
    else:        
        array_convertido_string = simplejson.dumps(contratosFondo, separators=('|',','))
        list_ContratosFondos = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
        
    if miembrosConsejoFondo == '':
        list_MiembrosFondo = ''
    else:        
        array_convertido_string = simplejson.dumps(miembrosConsejoFondo, separators=('|',','))
        list_MiembrosFondo = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')    
        
    if personasApoyoFondo == '':
        list_PersonasApoyo = ''
    else:        
        array_convertido_string = simplejson.dumps(personasApoyoFondo, separators=('|',','))
        list_PersonasApoyo = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
     
    if formulario_deserializado.get('varIdFondo') == '':
      
        validar_registro_fondo = {'NumeroEscritura':formulario_deserializado.get('NumeroEscritura'),'FechaEscritura':datetime.datetime.strptime(formulario_deserializado.get('FechaEscritura'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                 'NumeroNotario':formulario_deserializado.get('NumeroNotario'),'CiudadUbicacionNotario':formulario_deserializado.get('CiudadUbicacionNotario'),
                 'NombreNotario':formulario_deserializado.get('NombreNotario'),'NumeroRegistroShcp':formulario_deserializado.get('NumeroRegistroShcp'),
                 'OficioRegistro':formulario_deserializado.get('OficioRegistro'),'FechaRegistro':datetime.datetime.strptime(formulario_deserializado.get('FechaRegistro'),'%d/%m/%Y').strftime('%Y-%m-%d'),     
                 'FechaRppc':datetime.datetime.strptime(formulario_deserializado.get('FechaRppc'),'%d/%m/%Y').strftime('%Y-%m-%d'),'LugarRegistro':formulario_deserializado.get('LugarRegistro'),
                 'NumeroLibro':formulario_deserializado.get('NumeroLibro'),'Foja':formulario_deserializado.get('Foja'),}
        formularioRegistroFondo = RegistroFondoForm(validar_registro_fondo)
        
        if formularioRegistroFondo.is_valid():
                   
            datos_fondo = DatosFondo(Persona_id = formulario_deserializado.get('IdPersonaDatosFondo'),NumeroFondo=formulario_deserializado.get('NumeroFondo'))
            datos_fondo.save()        
            
            registro_fondo = RegistroFondo(DatosFondo_id = datos_fondo.IdDatosFondo, NumeroEscritura = formulario_deserializado.get('NumeroEscritura'),
                                            FechaEscritura = datetime.datetime.strptime(formulario_deserializado.get('FechaEscritura'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                                            NumeroNotario = formulario_deserializado.get('NumeroNotario'),CiudadUbicacionNotario = formulario_deserializado.get('CiudadUbicacionNotario').upper(),
                                            NombreNotario = formulario_deserializado.get('NombreNotario').upper(), NumeroRegistroShcp = formulario_deserializado.get('NumeroRegistroShcp'),
                                            OficioRegistro = formulario_deserializado.get('OficioRegistro').upper(),
                                            FechaRegistro = datetime.datetime.strptime(formulario_deserializado.get('FechaRegistro'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                                            FechaRppc = datetime.datetime.strptime(formulario_deserializado.get('FechaRppc'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                                            LugarRegistro = formulario_deserializado.get('LugarRegistro').upper(),NumeroLibro = formulario_deserializado.get('NumeroLibro'),
                                            Foja = formulario_deserializado.get('Foja').upper())
        
            registro_fondo.save()
            
            if list_Municipios != '':
                for municipio in list_Municipios:
                    guardar_municipios_datosFondo(municipio)
                    
            if list_CuentasFondo != '':
                for cuenta in list_CuentasFondo:
                    guardar_cuentas_datosFondo(cuenta, datos_fondo.IdDatosFondo)  
                    
            if list_ContratosFondos != '':
                for contrato in list_ContratosFondos:
                    guardar_contrato_fondo(contrato, datos_fondo.IdDatosFondo)
                    
            if list_MiembrosFondo != '':
                for miembroConsejo in list_MiembrosFondo:
                    guardar_miembrosConsejo_datosFondo(miembroConsejo, datos_fondo.IdDatosFondo)                    
                    
            if list_PersonasApoyo != '':
                for personaApoyo in list_PersonasApoyo:
                    guardar_personaApoyo_datosFondo(personaApoyo, datos_fondo.IdDatosFondo)
        
            dajax.script('manejadorMensajes(1);')          
        else:
            dajax.alert('Formulario invalido')
    
    else:
        actualizar_datos_fondo(formulario_deserializado, list_Municipios, list_CuentasFondo, list_ContratosFondos, list_MiembrosFondo, list_PersonasApoyo)
        dajax.script('manejadorMensajes(2);')
                 
    return dajax.json()

def guardar_personaApoyo_datosFondo(personaApoyo, idDatosFondo): # Función que recibe una entidad con la información de la persona de apoyo del fondo.
    dajax = Dajax()
    
    listaPersonaApoyo = personaApoyo.split(',')
    personaApoyoAGuardar = PersonalApoyo(DatosFondo_id = idDatosFondo, Persona_id = listaPersonaApoyo[3], CargoPersonaApoyo = listaPersonaApoyo[2])
    personaApoyoAGuardar.save()
    
    return dajax.json()

@dajaxice_register
def eliminar_personalApoyo_fondo(request, idPersonalApoyo): #Función que recibe el idPersonalApoyo con el cual se buscará el registro en la base de datos y se eliminara.
    dajax = Dajax()
    PersonalApoyo.objects.filter(IdPersonalApoyo = idPersonalApoyo).delete()
    
    return dajax.json()

def guardar_miembrosConsejo_datosFondo(miembro, idDatosFondo): # Función que recibe una entidad con la información del miembro de consejo de administración.
    dajax = Dajax()
    
    listaMiembro = miembro.split(',')
    fechaEleccion = datetime.datetime.strptime(listaMiembro[4],'%d/%m/%Y').strftime('%Y-%m-%d')
    consejoAGuardar = MiembroConsejoAdministracion(Cargo = listaMiembro[1], FechaEleccion = fechaEleccion, Duracion = listaMiembro[5], DatosFondo_id = idDatosFondo, Persona_id = listaMiembro[6])
    consejoAGuardar.save()
    
    return dajax.json()

@dajaxice_register
def obtener_personalApoyo_fondo(req): #Función que busca el personal de apoyo del fondo pasando el idDatosFondo.
    dajax = Dajax()
    try:            
        personalApoyo = PersonalApoyo.objects.all()
        datos = list()
        for personaApoyo in personalApoyo:
            nombrePersona = Persona.objects.filter(IdPersona = personaApoyo.Persona_id)[0]
            datos.append({'IdPersonalApoyo':personaApoyo.IdPersonalApoyo,'CargoPersonaApoyo':personaApoyo.CargoPersonaApoyo,'Persona_id':personaApoyo.Persona_id,'PrimerNombre':nombrePersona.PrimerNombre,'SegundoNombre':nombrePersona.SegundoNombre,'ApellidoPaterno':nombrePersona.ApellidoPaterno,'ApellidoMaterno':nombrePersona.ApellidoMaterno,'RazonSocial':nombrePersona.RazonSocial})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'personasApoyo':datos})

@dajaxice_register
def obtener_consejoAdministracion_fondo(req): #Función que busca a los integrantes del consejo de administración del fondo.
    dajax = Dajax()
    try:
        personalConsejoAdministracion = MiembroConsejoAdministracion.objects.all()
        datos = list()
        
        for personalConsejo in personalConsejoAdministracion:
            nombrePersona = Persona.objects.filter(IdPersona = personalConsejo.Persona_id)[0]
            datos.append({'IdConsejoAdministracion':personalConsejo.IdConsejoAdministracion,'IdPersona':personalConsejo.Persona_id,'Cargo':personalConsejo.Cargo,'Duracion':personalConsejo.Duracion,'FechaEleccion':personalConsejo.FechaEleccion.strftime("%d/%m/%Y"),'Nombre':nombrePersona.PrimerNombre+' '+nombrePersona.SegundoNombre+' '+nombrePersona.ApellidoPaterno+' '+nombrePersona.ApellidoMaterno})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'miembrosConsejo':datos})

@dajaxice_register
def eliminar_consejoAdministracion_fondo(request, idConsejoAdministracion): #Función que recibe el IdConsejoAdministracion con el cual se buscará el registro en la base de datos y se eliminara.
    dajax = Dajax()
    MiembroConsejoAdministracion.objects.filter(IdConsejoAdministracion = idConsejoAdministracion).delete()
    
    return dajax.json()

def guardar_cuentas_datosFondo(cuenta, idDatosFondo): # Función que recibe una entidad con la información de la cuenta bancaria y una variable que contiene el id de los datos del fondo para almacenarlos en la base de datos.
    dajax = Dajax()
    
    listaCuenta = cuenta.split(',')
    cuentaAGuardar = CuentaFondo(TipoCuenta = codificarUTF8(listaCuenta[1]), IdBanco = listaCuenta[5], NumeroCuenta = listaCuenta[3], Clave = listaCuenta[4], DatosFondo_id = idDatosFondo)
    cuentaAGuardar.save()
    
    return dajax.json()


def guardar_municipios_datosFondo(municipio): # Función que recibe una entidad con la información de dirección y una variable que contiene el id de persona para almacenarlos en la base de datos.
    dajax = Dajax()
    
    listaMunicipio = municipio.split(',')
    municipioAGuardar = AreaInfluencia(Municipio_id = listaMunicipio[0])
    municipioAGuardar.save()
    
    return dajax.json()

def actualizar_datos_fondo(formularioFondo, municipios, cuentas, contratos, miembros, personasApoyo):#Función que permite actualizar los datos generales del fondo.
    dajax = Dajax()
    
    DatosFondo.objects.filter(IdDatosFondo=formularioFondo.get('varIdFondo')).update(Persona = formularioFondo.get('IdPersonaDatosFondo'),NumeroFondo=formularioFondo.get('NumeroFondo'))  
    
    RegistroFondo.objects.filter(DatosFondo_id=formularioFondo.get('varIdFondo')).update(NumeroEscritura = formularioFondo.get('NumeroEscritura'), 
        FechaEscritura = datetime.datetime.strptime(formularioFondo.get('FechaEscritura'),'%d/%m/%Y').strftime('%Y-%m-%d'),
        NumeroNotario = formularioFondo.get('NumeroNotario'),CiudadUbicacionNotario = formularioFondo.get('CiudadUbicacionNotario').upper(),
        NombreNotario= formularioFondo.get('NombreNotario').upper(),NumeroRegistroShcp = formularioFondo.get('NumeroRegistroShcp'),
        OficioRegistro= formularioFondo.get('OficioRegistro').upper(),
        FechaRegistro = datetime.datetime.strptime(formularioFondo.get('FechaRegistro'),'%d/%m/%Y').strftime('%Y-%m-%d'),
        FechaRppc = datetime.datetime.strptime(formularioFondo.get('FechaRppc'),'%d/%m/%Y').strftime('%Y-%m-%d'),
        LugarRegistro= formularioFondo.get('LugarRegistro').upper(),NumeroLibro= formularioFondo.get('NumeroLibro'),
        Foja= formularioFondo.get('Foja').upper())   
    
    #AreaInfluencia.objects.all().delete()
    if municipios != '':
        for municipio in municipios:
            lista_municipio = municipio.split(',')
            if lista_municipio[1] == '':
                guardar_municipios_datosFondo(municipio)
    
    if cuentas != '':
        for cuenta in cuentas:
            lista_cuenta = cuenta.split(',')
            if lista_cuenta[0] == '':   
                guardar_cuentas_datosFondo(cuenta, formularioFondo.get('varIdFondo'))
                
    if contratos != '':
        for contrato in contratos:
            lista_contrato = contrato.split(',')
            if lista_contrato[0] == '':
                guardar_contrato_fondo(contrato, formularioFondo.get('varIdFondo'))
                
    if personasApoyo != '':
        for personaApoyo in personasApoyo:
            lista_PersonaApoyo = personaApoyo.split(',')
            if lista_PersonaApoyo[0] == '':
                guardar_personaApoyo_datosFondo(personaApoyo, formularioFondo.get('varIdFondo'))
                
    if miembros != '':
        for miembro in miembros:
            lista_miembro = miembro.split(',')
            if lista_miembro[0] == '':
                guardar_miembrosConsejo_datosFondo(miembro, formularioFondo.get('varIdFondo'))
    
    return dajax.json()
    

@dajaxice_register
def obtener_datos_fondo(req): #Función que busca la información de los datos generales del fondo.
    dajax = Dajax()
    try:
        datos = list()
        datosFondo = DatosFondo.objects.all()
        for datoFondo in datosFondo:  
            registroFondo = RegistroFondo.objects.filter(DatosFondo_id = datoFondo.IdDatosFondo)[0]        
            
            fechaEscritura = registroFondo.FechaEscritura.strftime("%d/%m/%Y")
            fechaRegistro = registroFondo.FechaRegistro.strftime("%d/%m/%Y")
            fecha = registroFondo.FechaRppc.strftime("%d/%m/%Y")
            
            informacionGeneralFondo = Persona.objects.filter(IdPersona = datoFondo.Persona_id)[0]
            #direccionDatosFondo = Direccion.objects.filter(Persona = datoFondo.Persona_id, TipoDireccion = 2)[0]               
            direccionDatosFondo = Direccion.objects.filter(Persona = datoFondo.Persona_id)
            Calle = ''
            for direccionFondo in direccionDatosFondo:
                Calle = direccionFondo.Calle
                if direccionFondo.TipoDireccion == 2:
                    Calle = direccionFondo.Calle
                    break
            
            #telefonoDatosFondo = Telefono.objects.filter(IdPersona = datoFondo.Persona_id, TipoTelefono = 'TRABAJO')[0]
            telefonoDatosFondo = Telefono.objects.filter(IdPersona = datoFondo.Persona_id)
            TelefonoF = ''
            for telefonoFondo in telefonoDatosFondo:
                TelefonoF = telefonoFondo.Numero
                if telefonoFondo.TipoTelefono == 'TRABAJO':
                    TelefonoF = telefonoFondo.Numero
                    break
            
           
            datos.append({'IdDatosFondo': datoFondo.IdDatosFondo,'Persona_id':datoFondo.Persona_id,'NombreFondo': informacionGeneralFondo.RazonSocial,'Email': informacionGeneralFondo.Email,
                          'Domicilio': Calle,'NumeroFondo':datoFondo.NumeroFondo,'Telefono':TelefonoF,'NumeroEscritura':registroFondo.NumeroEscritura,'NumeroNotario':registroFondo.NumeroNotario, 
                          'CiudadUbicacionNotario':registroFondo.CiudadUbicacionNotario,'NombreNotario':registroFondo.NombreNotario, 'NumeroRegistroShcp':registroFondo.NumeroRegistroShcp, 
                          'OficioRegistro':registroFondo.OficioRegistro,'Rfc':informacionGeneralFondo.Rfc, 'LugarRegistro':registroFondo.LugarRegistro, 'NumeroLibro':registroFondo.NumeroLibro, 
                          'Foja':registroFondo.Foja,'FechaEscritura':fechaEscritura, 'FechaRegistro':fechaRegistro, 'FechaRppc':fecha})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'datosfondo':datos}) 

@dajaxice_register
def obtenerMunicipiosDatosFondo(req): #Función que busca los municipios que conforman la zona de influencia de los datos del fondo.
    dajax = Dajax()
    try:
        #municipios = AreaInfluencia.objects.all().select_related().order_by('Municipio')
        municipios = AreaInfluencia.objects.all().order_by('Municipio_id')
        datos = list()
        
        for municipio in municipios:
            descripcionMunicipio = Municipio.objects.using('catalogos').get(IdMunicipio = municipio.Municipio_id)
            #descripcionEstado = Municipio.objects.select_related().filter(Estado_id=municipio.Municipio.Estado)[0]
            descripcionEstado = Municipio.objects.using('catalogos').select_related().filter(Estado_id=descripcionMunicipio.Estado_id)[0]
            datos.append({'IdMunicipio':municipio.Municipio_id,'DescripcionMunicipio':descripcionMunicipio.Descripcion,'DescripcionEstado':descripcionEstado.Estado.Descripcion,
                          'IdAreaInfluencia':municipio.IdAreaInfluencia})
          
    except:
        return dajax.json()
    
    return simplejson.dumps({'municipios':datos})

@dajaxice_register
def eliminar_municipio_datosFondo(request, idMunicipio): #Función que recibe el idMunicipio con el cual se buscará el registro en la base de datos y se eliminara.
    dajax = Dajax()
    AreaInfluencia.objects.filter(Municipio_id = idMunicipio).delete()
    
    return dajax.json()  

@dajaxice_register
def obtener_cuentasbancarias_datosfondo(req, idDatosFondo): #Función que busca las cuentas bancarias del fondo pasando el idDatosFondo.
    dajax = Dajax()
    try:            
        cuentasBancarias = CuentaFondo.objects.filter(DatosFondo = idDatosFondo)
        datos = list()
        #verificamos que exista malgun movimiento en el cobro de las constancias que afecten a los numeros de cuenta para poder bloquearlas
        contratoReaseguroUtilizado = False
        movimientoCobros = PagoConstancia.objects.all()
        if movimientoCobros:
            contratoReaseguroUtilizado = True
        
        for cuenta in cuentasBancarias:            
            banco = Bancos.objects.using('catalogos').filter(IdBanco = cuenta.IdBanco)[0]
            datos.append({'IdCuentaFondo':cuenta.IdCuentaFondo,'TipoCuenta':cuenta.TipoCuenta,'Descripcion':banco.Descripcion,'NumeroCuenta':cuenta.NumeroCuenta,
                          'Clave':cuenta.Clave,'ContratoReaseguroUtilizado':contratoReaseguroUtilizado})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'cuentas':datos})

@dajaxice_register
def eliminar_cuentabancaria_datosFondo(request, idCuentaFondo): #Función que recibe el idCuentaFondo con el cual se buscará el registro en la base de datos y se eliminara.
    dajax = Dajax()
    CuentaFondo.objects.filter(IdCuentaFondo = idCuentaFondo).delete()
    
    return dajax.json()

@dajaxice_register
def guardar_contrato_fondo(contrato, idDatosFondo): # Función que recibe una entidad con la información de contrato  y una variable que contiene el id del fondo para almacenarlos en la base de datos.
    dajax = Dajax()
    
    listaContrato = contrato.split(',')
    
    fechaContrato = datetime.datetime.strptime(listaContrato[3],'%d/%m/%Y').strftime('%Y-%m-%d')
    contratoAGuardar = ContratoFondo(VigenciaContrato = listaContrato[1], Ejercicio = listaContrato[2], FechaContrato = fechaContrato, NumeroContrato = listaContrato[4].upper(), IdReaseguradora = listaContrato[6], DatosFondo_id = idDatosFondo, IdContratoReaseguro = listaContrato[7], IdMoneda = listaContrato[8])
    contratoAGuardar.save()
    
    return dajax.json()

@dajaxice_register
def obtener_contratos_fondo(req, idDatosFondo): #Función que busca las cuentas bancarias del fondo pasando el idDatosFondo.
    dajax = Dajax()
    try:        
        contratoDatosFondo = ContratoFondo.objects.filter(DatosFondo = idDatosFondo)            
        datos = list()
        for contrato in contratoDatosFondo:
            contratoUtilizado = False
            #Se buscan utiliza una variable para controlar que no se borren los contratos de reaseguro del fondo si estos ya cuentan con alguna cotizacion de por medio
            programa = Programa.objects.filter(IdContratoFondo = contrato.IdContratoFondo)
            if programa:
                contratoUtilizado = True
            
            reaseguradora = Reaseguradora.objects.using('catalogos').filter(IdReaseguradora = contrato.IdReaseguradora)[0]
            contratoReaseguro = ContratoReaseguro.objects.using('catalogos').filter(IdContratoReaseguro = contrato.IdContratoReaseguro)[0]
            moneda = Moneda.objects.using('catalogos').filter(IdMoneda = contrato.IdMoneda)[0]
            fecha = contrato.FechaContrato.strftime("%d/%m/%Y")
            datos.append({'IdContratoFondo':contrato.IdContratoFondo,'VigenciaContrato':contrato.VigenciaContrato,'Ejercicio':contrato.Ejercicio,'FechaContrato':fecha, 'NumeroContrato': contrato.NumeroContrato,
                          'Reaseguradora':reaseguradora.Descripcion,'ContratoReaseguro':contratoReaseguro.RazonContenido,'Moneda':moneda.Nombre,'ContratoUtilizado':contratoUtilizado})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'contratos':datos})

@dajaxice_register
def eliminar_contratos_fondo(request, idContratoFondo): #Función que recibe el idContratoFondo con el cual se buscará el registro en la base de datos y se eliminara.
    dajax = Dajax()
    ContratoFondo.objects.filter(IdContratoFondo = idContratoFondo).delete()
    
    return dajax.json()

@dajaxice_register
def cargar_Combo_Estados(request):
    dajax = Dajax()
    tiposEstados = Estado.objects.using('catalogos').all()
    
    out = []
    for tipo in tiposEstados:
        out.append("<option value='" + str(tipo.IdEstado) + "'>%s</option>" % tipo.Descripcion)

    dajax.assign('#cmbEstados', 'innerHTML', ''.join(out))
    
    return dajax.json()

@dajaxice_register
def cargar_Combo_Municipios(request, valor):
    #dajax = Dajax()
    Municipios = Municipio.objects.using('catalogos').filter(Estado = valor)
    
    #out = []
    municipios = list()
    for tipo in Municipios:
        municipios.append({"IdMunicipio":tipo.IdMunicipio,"DescripcionMunicipio":tipo.Descripcion})
        #out.append("<option value='" + str(tipo.IdMunicipio) + "'>%s</option>" % tipo.Descripcion)

    #dajax.assign('#cmbMunicipios', 'innerHTML', ''.join(out))
    
    #return dajax.json()
    return simplejson.dumps({'Municipios':municipios})