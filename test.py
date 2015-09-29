# -*- coding: utf-8 -*-


from models.senhas import Senha, Collection

from utils import Encriptador


import hashlib



class ManCollection (object):
    def __init__(self):
        pass
    
    def add (self, data):
        c = Collection()
        c.nome = data['nome']
        c.save()
        print c.nome
        
    def delete (self, aidi):
        c = Collection.select().where(Collection.id==aidi)
        for i in c:
            print i.nome
            i.delete_instance(recursive=True)
        
        
    def edit (self, data):
        #aidi = data['id']
        c = Collection().data_from_dict (data)
        c.save()
        
        
class ManSenha (object):
    def __init__(self, collect, encriptador):
        self.enc = encriptador
        self.collect = collect
        
    def add (self, data):
        c = Collection()
        c.desc = data['desc']
        c.valor = self.enc.encripta( data['valor'] )
        c.collect = self.collect
        c.save()
        
    def edit (self, data):
        #aidi = data['id']
        data_enc = data.copy()
        data_enc['valor'] = self.enc.encripta( data['valor'] )
        
        c = Collection().data_from_dict (data_enc)
        c.save()
        
    def delete (self, aidi):
        c = Collection.select().where(Collection.id==aidi)
        for i in c:
            print i.nome
            i.delete_instance(recursive=True)
            
        
   

#col = Collection()
#col.nome = 'Geral'
#col.save()







senha = 'teste123'
e = Encriptador(senha)


mc = ManCollection()
#data = {
        #'nome': 'Geral2'
    #}
#mc.add (data)


data = {
        'id': 9,
        'nome': 'Geral99'
    }
mc.edit (data)
mc.delete (99)



ms = ManSenha(e, )
data = {
        'desc': '',
        'valor': 'valorXyz'
    }
ms.add (data)

cols = Collection.select()
print "ct", cols.count()
for col in cols:
    print col.nome, col.id
    sens = Senha.select().where(Senha.collect == col)
    for s in sens:
        print s.desc, e.decripta (s.valor)
    
    


s = Senha()
s.collect =  cols[0]
s.desc = 'coisa 3'
s.valor = e.encripta ('v#$@%alorXyxx')
s.save()


