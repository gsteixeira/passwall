

from peewee import *

db = SqliteDatabase('var/db/passwall.db')



db.connect()

from datetime import datetime







class BaseModel(Model):
    class Meta:
        database = db

    def data_from_dict (self, dictionary, fields=None):
        
            
        #if 'id' in dictionary.keys():
        self, e = self.get_or_create (id=dictionary['id'])
        #print "model, e", self, e
        
        if (fields != None):
            for key in fields:
                if ( key in self._meta.fields.keys()) and ( key in dictionary.keys() ):
                    self.__dict__['_data'][key] = dictionary[key]
        else:        
            for key in dictionary.keys():
                if key in self._meta.fields.keys():
                    self.__dict__['_data'][key] = dictionary[key]
        return self
        
        
class Collection (BaseModel):
    nome = CharField (max_length=70, null=True)
    
    
    
class Senha (BaseModel):
    desc = CharField (max_length=70, null=True)
    valor = CharField (max_length=70, null=True)
    collect = ForeignKeyField (Collection, related_name='senha_collect', null=True)
    