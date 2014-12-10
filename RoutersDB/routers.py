class SiobicxRouter(object):
    '''
    A router to controll all database operations on models in the Siobics application
    '''
    app_list = ('BuscadorPersonas','Cobranza','ConexosAgropecuarios','Constancias','Cotizador','Direcciones','Endoso','Programas','Reporteador','Solicitud','Siniestro')
    def db_for_read(self, model, **hints):
        '''
        Attempts to read auth models go to siobicx
        '''
        if model._meta.app_label in self.app_list:
            return 'siobicx'
        return None
    
    def db_for_write(self, model, **hints):
        '''
        Attempts to write auth models go to siobicx
        '''
        if model._meta.app_label in self.app_list:
            return 'siobicx'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        '''
        Allow relations if a model in the Siobicx is involved
        '''
        if obj1._meta.app_label in self.app_list or obj2._meta.app_label in self.app_list:
            return True
        return None
    
    def allow_migrate(self, db, model):
        return True