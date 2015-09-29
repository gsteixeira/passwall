
from peewee import *

import os

DB_FILE='../databases/var/db/passwall.db'

if not os.path.exists(DB_FILE):
    os.mkdir('../databases/')
    os.mkdir('../databases/var')
    os.mkdir('../databases/var/db/')
    f = open (DB_FILE, 'w+')
    f.close()

db = SqliteDatabase(DB_FILE)



db.connect()

from datetime import datetime


# -*- coding: utf-8 -*-

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
    last_updt = DateTimeField ( null=True )
    
    def save(self, *args, **kwargs):
        self.last_updt = datetime.now()
        return super(Collection, self).save(*args, **kwargs)
        
    
    
class Senha (BaseModel):
    desc = CharField (max_length=70, null=True)
    valor = CharField (max_length=4096, null=True)
    collect = ForeignKeyField (Collection, related_name='senha_collect', null=True)
    
    last_updt = DateTimeField ( null=True )
    
    def save(self, *args, **kwargs):
        self.last_updt = datetime.now()
        return super(Senha, self).save(*args, **kwargs)
        
        
    





#class ManCollection (object):
    #def __init__(self):
        #pass
    
    #def add (self, data):
        #c = Collection()
        #c.nome = data['nome']
        #c.save()
        #print c.nome
        
    #def delete (self, aidi):
        #c = Collection.select().where(Collection.id==aidi)
        #for i in c:
            #print i.nome
            #i.delete_instance(recursive=True)
        
        
    #def edit (self, data):
        ##aidi = data['id']
        #c = Collection().data_from_dict (data)
        #c.save()
        
        
#class ManSenha (object):
    #def __init__(self, collect, encriptador):
        #self.enc = encriptador
        #self.collect = collect
        
    #def add (self, data):
        #c = Collection()
        #c.desc = data['desc']
        #c.valor = self.enc.encripta( data['valor'] )
        #c.collect = self.collect
        #c.save()
        
    #def edit (self, data):
        ##aidi = data['id']
        #data_enc = data.copy()
        #data_enc['valor'] = self.enc.encripta( data['valor'] )
        
        #c = Collection().data_from_dict (data_enc)
        #c.save()
        
    #def delete (self, aidi):
        #c = Collection.select().where(Collection.id==aidi)
        #for i in c:
            #print i.nome
            #i.delete_instance(recursive=True)


    
    
db.create_tables([ Collection, Senha ], safe=True)
