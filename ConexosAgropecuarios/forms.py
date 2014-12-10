#encoding:utf-8
from django.forms import ModelForm, TextInput
from ConexosAgropecuarios.models import Persona, Telefono, RegistroFondo, CuentaFondo, ContratoFondo, MiembroConsejoAdministracion, PersonalApoyo
from django import forms
from django.forms.widgets import CheckboxInput

class NumberInput(TextInput):
    input_type = 'number'

class PersonaFisicaForm(ModelForm): #Generación del formulario persona física a partir del modelo Persona el cual contiene los campos del formulario y su comportamiento.
        class Meta:
            model = Persona
            fields = ['Rfc', 'Curp', 'PrimerNombre', 'SegundoNombre', 'ApellidoPaterno', 'ApellidoMaterno', 'FechaNacimiento', 'Email', 'Sexo', 'EstadoCivil', 'EsSocio']
            widgets = {
                        'Rfc' : TextInput(attrs = {'class':'input-medium','required':'','placeholder':'Rfc'}),
                        'Curp' : TextInput(attrs = {'class':'input-medium','required':'','placeholder':'Curp'}),
                        'PrimerNombre' : TextInput(attrs = {'class':'input-medium','required':'','placeholder':'Primer Nombre','autofocus':''}),
                        'SegundoNombre' : TextInput(attrs = {'class':'input-medium','placeholder':'Segundo Nombre'}),
                        'ApellidoPaterno' : TextInput(attrs = {'class':'input-medium','required':'','placeholder':'Apellido Paterno'}),
                        'ApellidoMaterno' : TextInput(attrs = {'class':'input-medium','required':'','placeholder':'Apellido Materno'}),
                        'FechaNacimiento' : TextInput(attrs = {'class':'input-small','placeholder':'dd/mm/aaaa'}),
                        'Email' : TextInput(attrs = {'class':'span3','placeholder':'Email'}),
                        'Sexo' : forms.Select(attrs= {'class':'input-medium'}),
                        'EstadoCivil' : forms.Select(attrs= {'class':'input-medium'}),
                        'EsSocio' : CheckboxInput(attrs= {'default':'False'})
            }
            
class PersonaMoralForm(ModelForm): # Clase para crear el formulario de persona moral por medio del modelo persona, se especifican los campos necesarios y los atributos que tendra el html      
    class Meta:
        model = Persona
        fields = ['Rfc','RazonSocial','FechaNacimiento','Email','EsSocio']
        widgets = {
                   'Rfc': TextInput(attrs={'class':'input-medium','required':'','placeholder':'Rfc','autofocus':''}),
                   'RazonSocial': TextInput(attrs={'class':'input-xxlarge','required':'','placeholder':'Razón Social'}),
                   'FechaNacimiento': TextInput(attrs={'class':'input-small','required':'','placeholder':'dd/mm/aaaa'}),
                   'Email': TextInput(attrs={'class':'span2','placeholder':'Email'}),
                   'EsSocio' : CheckboxInput(attrs={'checked':''}),
        }
        

class TelefonoForm(ModelForm):# Genera el formulario teléfono a partir del modelo Teléfono el cual contiene los campos del formulario y su comportamiento.
    class Meta:
        model = Telefono    
        fields = ['TipoTelefono','Numero']   
        widgets = {
                    'TipoTelefono' : forms.Select(attrs= {'class':'input-medium'}),
                    'Numero' : TextInput(attrs={'class':'input-medium','placeholder':'Número'}),
        }
     
class RegistroFondoForm(ModelForm):# Genera el formulario de registros del fondo a partir del modelo RegistroFondo.
    class Meta:
        model = RegistroFondo
        fields = ['NumeroEscritura','FechaEscritura','NumeroNotario','CiudadUbicacionNotario','NombreNotario','NumeroRegistroShcp','OficioRegistro',
                    'FechaRegistro','FechaRppc','LugarRegistro','NumeroLibro','Foja']   
        widgets = {
                    'NumeroEscritura' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Número Escritura'}),
                    'FechaEscritura' : TextInput(attrs = {'class':'input-small','required':'','placeholder':'dd/mm/aaaa'}),
                    'NumeroNotario' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Número Notario'}),
                    'CiudadUbicacionNotario' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Ciudad Notario'}),
                    'NombreNotario' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Nombre Notario'}),
                    'NumeroRegistroShcp': TextInput(attrs={'class':'input-medium','required':'','placeholder':'Número Registro'}),
                    'OficioRegistro' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Oficio Registro'}),
                    'FechaRegistro' : TextInput(attrs = {'class':'input-small','required':'','placeholder':'dd/mm/aaaa'}),
                    'FechaRppc' : TextInput(attrs = {'class':'input-small','required':'','placeholder':'dd/mm/aaaa'}),
                    'LugarRegistro' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Lugar Registro'}),
                    'NumeroLibro': TextInput(attrs={'class':'input-medium','required':'','placeholder':'Número Libro'}),
                    'Foja' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Foja'}),
        }
        
class CuentaBancoForm(ModelForm):# Genera el formulario cuentas bancarias a partir del modelo CuentaFondo el cual contiene los campos del formulario y su comportamiento.
    class Meta:
        model = CuentaFondo   
         
        fields = ['TipoCuenta','IdBanco', 'NumeroCuenta','Clave']   
        widgets = {
                    'TipoCuenta' : forms.Select(attrs= {'class':'input-medium'}),     
                    'IdEstado': forms.Select(attrs= {'class':'input-medium'}),     
                    'NumeroCuenta' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Número Cuenta'}),
                    'Clave' : TextInput(attrs={'class':'input-medium','required':'','placeholder':'Clabe'}),
        }  
        
class ContratoFondoForm(ModelForm):# Genera el formulario contratos del fondo a partir del modelo ContratosFondo el cual contiene los campos del formulario y su comportamiento.
    class Meta:
        model = ContratoFondo   
         
        fields = ['VigenciaContrato','Ejercicio','FechaContrato','NumeroContrato','IdReaseguradora','IdContratoReaseguro','IdMoneda']   
        widgets = {
                    'VigenciaContrato' : forms.Select(attrs={'class':'input-medium'}),   
                    'Ejercicio': TextInput(attrs={'class':'input-small','placeholder':'Ejercicio'}),   
                    'FechaContrato' : TextInput(attrs = {'class':'input-small','placeholder':'dd/mm/aaaa'}),
                    'NumeroContrato' : TextInput(attrs={'class':'input-medium','placeholder':'Número de Contrato'}),
                    'IdReaseguradora' : forms.Select(attrs= {'class':'input-large'}),
                    'IdContratoReaseguro' : forms.Select(attrs= {'class':'input-large'}),
                    'IdMoneda' : forms.Select(attrs= {'class':'input-large'}),
        }
        
class ConsejoAdminsitracionForm(ModelForm):# Genera el formulario Consejo de administeción del fondo a partir del modelo ConsejoAdministracion el cual contiene los campos del formulario y su comportamiento.
    class Meta:
        model = MiembroConsejoAdministracion   
         
        fields = ['Cargo','FechaEleccion','Duracion']   
        widgets = {
                    'Cargo' : forms.Select(attrs= {'class':'input-medium'}),  
                    'FechaEleccion' : TextInput(attrs = {'class':'input-small','placeholder':'dd/mm/aaaa'}),
                    'Duracion' : TextInput(attrs={'class':'input-medium','placeholder':'Duracion'}),
        }
        
class PersonalApoyoForm(ModelForm):
        class Meta:
            model = PersonalApoyo
             
            fields = ['CargoPersonaApoyo']   
            widgets = {
                        'CargoPersonaApoyo' : forms.Select(attrs= {'class':'input-medium'}),  
            }