# -*- coding: utf-8 -*-

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
        self, e = self.get_or_create (id=dictionary['id'])
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

    
db.create_tables([ Collection, Senha ], safe=True)
