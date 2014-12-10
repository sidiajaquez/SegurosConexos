#encoding:utf-8
from django.db import models

class Persona(models.Model): #Clase que genera el modelo Persona el cual contiene los campos para la gestión de informacion.
    SEXO = (
            ('M','Masculino'),
            ('F','Femenino'),
    )
    ESTADO_CIVIL = (
                    ('SOLTERO/A','Soltero/a'),
                    ('CASADO/A','Casado/a'),
                    ('DIVORCIADO/A','Divorciado/a'),
                    ('VIUDO/A','Viudo/a'),
                    ('UNION LIBRE','Unión Libre'),
                    ('SEPARADO/A','Separado/a'),
    )
    TIPO_PERSONA = (
                    ('F','Física'),
                    ('M','Moral'),
    )
    
    IdPersona = models.AutoField(primary_key=True)
    Rfc = models.CharField(verbose_name='Rfc', max_length=13)
    Curp = models.CharField(verbose_name='Curp', max_length=18, null=True, blank = True)
    PrimerNombre = models.CharField(verbose_name='Primer Nombre', max_length=50, null=True, blank = True)
    SegundoNombre = models.CharField(verbose_name='Segundo Nombre', max_length=50, null=True, blank = True)
    ApellidoPaterno = models.CharField(verbose_name ='Apellido Paterno', max_length=50, null=True, blank = True)
    ApellidoMaterno = models.CharField(verbose_name = 'Apellido Materno', max_length=50, null=True, blank = True)
    RazonSocial = models.CharField(verbose_name='Razón Social', max_length=200, null=True, blank=True)
    FechaNacimiento = models.DateTimeField(verbose_name='Fecha Nacimiento', null=True, blank = True)
    Email = models.EmailField(verbose_name='E-mail',max_length=100, null=True, blank = True)
    #Foto = models.ImageField(verbose_name='Foto')
    #Firma = models.ImageField(verbose_name='Firma')
    Sexo = models.CharField(max_length=1,choices=SEXO, null=True, blank = True)
    EstadoCivil = models.CharField(max_length=12,choices=ESTADO_CIVIL, null=True, blank = True)
    TipoPersona = models.CharField(max_length=1, choices=TIPO_PERSONA, null= True)
    EsSocio = models.BooleanField(verbose_name='Socio', default=0)
    FechaIngreso = models.DateTimeField(verbose_name='Fecha Ingreso',null=True, blank = True)
    
    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ('Rfc',)
        db_table = "Personas"
        
    def __unicode__(self):
        return self.Rfc
    
class Telefono(models.Model): #Clase que genera el modelo teléfono el cual contiene los campos para la gestión de información y el campo id persona el cual enlaza con el modelo Persona.
    TIPO_TELEFONO = (
                     ('CASA','CASA'),
                     ('CELULAR','CELULAR'),
                     ('TRABAJO','TRABAJO'),
    )
    IdTelefono = models.AutoField(primary_key= True)
    IdPersona = models.ForeignKey(Persona)
    TipoTelefono = models.CharField(max_length=12,choices=TIPO_TELEFONO,blank = True)    
    Numero = models.CharField(verbose_name='Numero', max_length=14)
    
    class Meta:
        verbose_name = 'Telefono'
        verbose_name_plural = 'Telefonos'
        db_table = "Telefonos"
        
    def __unicode__(self):
        return self.Numero

class SocioMoral(models.Model): #Clase para los socios de las personas morales
    IdSocioMoral = models.AutoField(primary_key = True)
    Persona = models.ForeignKey(Persona)
    SocioMoral = models.IntegerField(verbose_name = 'Socio Moral')
    
    class Meta:
        verbose_name = 'SocioMoral'
        verbose_name_plural = 'SociosMoral'
        ordering = ('IdSocioMoral',)
        db_table = "SociosMoral"
        
    def __unicode__(self):
        return self.IdSocioMoral
    
class Estado(models.Model): #Clase que genera el modelo para gestionar los estados en la base de datos catalogos. 
    IdEstado = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=30, null=True, blank = True)
    
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ('IdEstado',)
        db_table = 'Estados'
    
    def __unicode__(self):
        return self.IdEstado    
    
class DatosFondo(models.Model): # Clase que genera el modelo para los datos generales del fondo.    
    #estados = [(e.IdEstado, e.Descripcion) for e in Estado.objects.using('catalogos').all()]
   
    IdDatosFondo = models.AutoField(primary_key=True)
    Persona = models.ForeignKey(Persona)
    NumeroFondo = models.CharField(null=True, blank=True, max_length=4, verbose_name = "Numero de Fondo")
    
    class Meta:
        verbose_name = 'DatosFondo'
        verbose_name_plural = 'DatosFondo'
        ordering = ('IdDatosFondo',)
        db_table = 'DatosFondo'
        
    def __unicode__(self):
        return self.IdDatosFondo
    
class RegistroFondo(models.Model): # Clase que genera el modelo para gestionar los registros del fondo.
    IdRegistroFondo = models.AutoField(primary_key=True)
    DatosFondo = models.ForeignKey(DatosFondo)
    NumeroEscritura = models.IntegerField(verbose_name='Número Escritura',null=True, blank = True)
    FechaEscritura = models.DateTimeField(verbose_name='Fecha Escritura',null=True, blank = True)
    NumeroNotario = models.IntegerField(verbose_name='Número Notario',null=True, blank = True)
    CiudadUbicacionNotario = models.CharField(verbose_name='Ciudad Ubicacion Notario', max_length=30,null=True, blank = True)
    NombreNotario = models.CharField(verbose_name='Nombre Notario', max_length=50,null=True, blank = True)
    NumeroRegistroShcp = models.CharField(verbose_name='Número Registro SHCP', max_length = 50,null=True, blank = True)
    OficioRegistro = models.CharField(verbose_name='Oficio Registro', max_length=20,null=True, blank = True)
    FechaRegistro = models.DateTimeField(verbose_name='Fecha Registro',null=True, blank = True)
    FechaRppc = models.DateTimeField(verbose_name='Fecha RPPC',null=True, blank = True)
    LugarRegistro = models.CharField(verbose_name='Lugar Registro', max_length=30,null=True, blank = True)
    NumeroLibro = models.CharField(verbose_name='Número Libro', max_length = 30,null=True, blank = True)
    Foja = models.CharField(verbose_name='Foja', max_length=20,null=True, blank = True)
    
    class Meta:
        verbose_name = 'RegistroFondo'
        verbose_name_plural = 'registrosfondo'
        ordering = ('IdRegistroFondo',)
        db_table = 'RegistrosFondo'
        
    def __unicode__(self):
        return self.IdRegistroFondo
    
class PersonalApoyo(models.Model): #Clase que genera el modelo para gestionar los registros del personal de apoyo del fondo de aseguramiento
    CARGOS = (
                     ('GERENTE','GERENTE'),
                     ('TECNICO DE CAMPO','TECNICO DE CAMPO'),
                     ('CONTADOR','CONTADOR'),
                     ('SECRETARIO/A','SECRETARIO/A'),
                     ('SUSCRIPTOR','SUSCRIPTOR'),
                     ('AJUSTADOR','AJUSTADOR'),
    )
    
    IdPersonalApoyo = models.AutoField(primary_key=True)
    DatosFondo = models.ForeignKey(DatosFondo)
    Persona = models.ForeignKey(Persona)
    CargoPersonaApoyo = models.CharField(max_length=30, choices=CARGOS, null=True, blank = True)
    
    class Meta:
        verbose_name = 'PersonalApoyo'
        ordering = ('IdPersonalApoyo',)
        db_table = 'PersonalApoyo'
    
    def __unicode__(self):
        return self.IdPersonalApoyo
    
class Municipio(models.Model): #Clase que genera el modelo para gestionar los registros de los municipios del fondo para identificar la zona de influencia
    IdMunicipio = models.AutoField(primary_key=True)
    Estado = models.ForeignKey(Estado)
    Descripcion = models.CharField(max_length=30, null=True, blank = True)
    
    class Meta:
        verbose_name = 'Municipio'
        ordering = ('IdMunicipio',)
        db_table = 'Municipios'
    
    def __unicode__(self):
        return self.IdMunicipio
        
class Bancos(models.Model): #Clase que genera el modelo para gestionar los bancos en la base de datos catalogos.
    IdBanco = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=20, null=True, blank = True)
    
    class Meta:
        verbose_name = 'Bancos'
        verbose_name_plural = 'bancos'
        ordering = ('IdBanco',)
        db_table = 'bancos'
    
    def __unicode__(self):
        return self.IdBanco          
        
class CuentaFondo(models.Model): # Clase que genera el modelo para las cuentas bancarias del fondo.
        
    TiposCuenta = (
                     ('CAPTADORA DE PAGOS','CAPTADORA DE PAGOS'),
                     ('DEPÓSITOS DE SUBSIDIO','DEPÓSITOS DE SUBSIDIO'),
                     ('PREVISIÓN DE GASTOS','PREVISIÓN DE GASTOS'),
                     ('RESERVA DE RIESGOS EN CURSOS','RESERVA DE RIESGOS EN CURSOS'),
                     ('RESERVA ESPECIAL DE CONTIGENCIA','RESERVA ESPECIAL DE CONTIGENCIA'),
    )    
        
    bancos = [(e.IdBanco, e.Descripcion) for e in Bancos.objects.using('catalogos').all()]
    
    IdCuentaFondo = models.AutoField(primary_key=True)
    DatosFondo = models.ForeignKey(DatosFondo)
    TipoCuenta = models.CharField(verbose_name='Tipo Cuenta', max_length=50, choices= TiposCuenta)
    IdBanco = models.CharField(max_length=30, null=True, blank = True, verbose_name = 'Id Banco', choices= bancos)
    NumeroCuenta = models.CharField(verbose_name='Número Cuenta', max_length=30)
    Clave = models.CharField(verbose_name='Clave', max_length=20)
    
    class Meta:
        verbose_name = 'CuentaFondo'
        verbose_name_plural = 'CuentasFondo'
        ordering = ('IdCuentaFondo',)
        db_table = 'CuentasFondo'
        
    def __unicode__(self):
        return self.IdCuentaFondo
    
class Reaseguradora(models.Model): #Clase que genera el modelo para gestionar las reaseguradoras en la base de datos catálogos.
    IdReaseguradora = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=30, null=True, blank = True)
    
    class Meta:
        verbose_name = 'Reaseguradora'
        verbose_name_plural = 'reaseguradora'
        ordering = ('IdReaseguradora',)
        db_table = 'reaseguradora'
    
    def __unicode__(self):
        return self.IdReaseguradora     

class ContratoReaseguro(models.Model): #Clase para generar el modelo que permita la gestion de los tipos de contrato que maneja el reaseguro
    IdContratoReaseguro = models.AutoField(primary_key=True)
    Obligacion = models.CharField(null=True,blank=True,max_length=30,verbose_name="Obligatoriedad del Reaseguro")
    RazonContenido = models.CharField(null=True,blank=True,max_length=20,verbose_name="Razon del Contenido")
    
    class Meta:
        verbose_name = 'ContratoReaseguro'
        verbose_name_plural = 'ContratosReaseguro'
        ordering =('IdContratoReaseguro',)
        db_table = 'ContratoReaseguro'
    
    def __unicode__(self):
        return self.IdContratoReaseguro 

class Moneda(models.Model): #Clase para gestionar el catalogo de monedas
    IdMoneda = models.AutoField(primary_key=True)
    Clave = models.CharField(null=True,blank=True,max_length=3,verbose_name="Clave de Moneda")
    Nombre = models.CharField(null=True,blank=True,max_length=50,verbose_name="Nombre de la Moneda")
    Descripcion = models.CharField(null=True,blank=True,max_length=50,verbose_name="Descripcion de la Moneda")
    
    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'
        ordering = ('IdMoneda',)
        db_table = 'Moneda'
    
    def __unicode__(self):
        return self.IdMoneda
    
class ContratoFondo(models.Model): # Clase que genera el modelo para los contratos del fondo.
    vigenciaContrato = (
                        ('INDEFINIDO','INDEFINIDO'),
                        ('ANUAL','ANUAL'),
    )
      
    reaseguradora = [(e.IdReaseguradora, e.Descripcion) for e in Reaseguradora.objects.using('catalogos').all()]
    contratosReaseguradora = [(e.IdContratoReaseguro, e.RazonContenido) for e in ContratoReaseguro.objects.using('catalogos').all()]
    monedas = [(e.IdMoneda, e.Nombre) for e in Moneda.objects.using('catalogos').all()]
    
    IdContratoFondo = models.AutoField(primary_key=True)
    DatosFondo = models.ForeignKey(DatosFondo)
    VigenciaContrato = models.CharField(verbose_name='Vigencia Contrato', max_length=10, null = True, blank = True, choices = vigenciaContrato)
    Ejercicio = models.CharField(max_length=4, null=True, blank = True, verbose_name = 'Ejercicio')
    FechaContrato = models.DateTimeField(verbose_name='Fecha Contrato',null=True, blank = True)
    NumeroContrato = models.CharField(verbose_name='Número Contrato', max_length=20)
    IdReaseguradora = models.CharField(max_length=30, null=True, blank=True, verbose_name = 'Id Reaseguradora', choices= reaseguradora)
    IdContratoReaseguro = models.CharField(max_length=50,null=True, blank=True, verbose_name='Contrato Reaseguro', choices=contratosReaseguradora)
    IdMoneda = models.CharField(max_length=50,null=True, blank=True, verbose_name='Tipo Moneda', choices=monedas)

    class Meta:
        verbose_name = 'ContratoFondo'
        verbose_name_plural = 'ContratosFondo'
        ordering = ('IdContratoFondo',)
        db_table = 'ContratosFondo'
        
    def __unicode__(self):
        return self.IdContratoFondo
   
class MiembroConsejoAdministracion(models.Model): # Clase que genera el modelo para almacenar a los miembros del consejo de adminsitración del fondo.
        
    cargos = (
             ('PRESIDENTE','PRESIDENTE'),
             ('SECRETARIO','SECRETARIO'),
             ('TESORERO','TESORERO'),
             ('VOCAL','VOCAL'),                     
    )    
    
    IdConsejoAdministracion = models.AutoField(primary_key=True)
    Cargo = models.CharField(max_length=20, null=True, blank = True, verbose_name = 'Cargo', choices=cargos)
    FechaEleccion = models.DateTimeField(verbose_name='Fecha Elección',null=True, blank = True)
    Duracion = models.CharField(max_length=10, null=True, blank = True, verbose_name = 'Duración')
    Persona = models.ForeignKey(Persona)
    DatosFondo = models.ForeignKey(DatosFondo)
    
    class Meta:
        verbose_name = 'MiembroConsejoAdministracion'
        verbose_name_plural = 'MiembrosConsejoAdministracion'
        ordering = ('IdConsejoAdministracion',)
        db_table = 'MiembrosConsejoAdministracion'
        
    def __unicode__(self):
        return self.IdConsejoAdministracion

class AreaInfluencia(models.Model): # Clase que genera el modelo para almacenar el area de influencia del fondo de aseguramiento
    IdAreaInfluencia = models.AutoField(primary_key=True)
    Municipio_id = models.IntegerField()
    
    class Meta:
        verbose_name = 'AreaInfluencia'
        verbose_name_plural = 'AreasInfluencia'
        ordering = ('IdAreaInfluencia',)
        db_table = 'AreaInfluencia'
    
    def __unicode__(self):
        return self.IdAreaInfluencia    