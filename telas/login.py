# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
#from kivy.lang import Builder

CHECK_FILE = '../databases/var/db/pcheck.chk'
CHECK_STR = 'this should be readable'


from utils import Encriptador
import os



import hashlib

def migra (e):
    from models.senhas import Senha, Collection
    cols = Collection.select()
    for c in cols:
        nome = e.decripta (c.nome)
        c.nome = e.encripta (nome)
        print "migrando colection ", nome
        c.save()
        
    sens = Senha.select()
    for s in sens:
        desc = e.decripta (s.desc)
        valor = e.decripta (s.valor)
        s.desc = e.encripta (desc)
        s.valor = e.encripta (valor)
        print "migrando senha ", desc
        s.save()
    
    f = open (CHECK_FILE, 'w')
    f.write ( e.encripta (CHECK_STR) )
    f.close()
    
        
def change_password (new_pass, old_pass):
    enc_novo = Encriptador (new_pass)
    enc_velho = Encriptador (old_pass)
    # testa se a senha informada esta correta
    f = open (CHECK_FILE, 'r')
    check = f.read()
    f.close()
    if enc_velho.decripta ( check ) != CHECK_STR:
        return False
        # se nao tiver cai fora

    cols = Collection.select()
    for c in cols:
        nome = enc_velho.decripta (c.nome)
        c.nome = enc_novo.encripta (nome)
        print "migrando colection ", nome
        c.save()
        
    sens = Senha.select()
    for s in sens:
        desc = enc_velho.decripta (s.desc)
        valor = enc_velho.decripta (s.valor)
        s.desc = enc_novo.encripta (desc)
        s.valor = enc_novo.encripta (valor)
        print "migrando senha ", desc
        s.save()
        
    f = open (CHECK_FILE, 'w')
    f.write ( enc_novo.encripta (CHECK_STR) )
    f.close()
        
        

class JanelaLogin (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        self.last_window = last_window
        super(JanelaLogin, self).__init__(**kwargs)
        self.smanager = smanager
        
    def on_pre_enter (self):
        # verifica se ja existe uma senha
        # Senao, chama o JanelaFirst
        if not os.path.exists(CHECK_FILE):
            print "pcheck nao existe!!!"
                
            janela = JanelaFirstLogin(smanager=self.smanager, name='janela_first_login') 
            self.smanager.add_widget( janela )
            self.smanager.transition.direction = 'left'
            self.smanager.current = 'janela_first_login'
        else:
            self.ids.tx_password.focus = True

    def on_leave (self):
        self.smanager.remove_widget(self)
        
    def check_pass (self):
        f = open (CHECK_FILE, 'r')
        check = f.read()
        f.close()
        
        if self.smanager.encrypter.decripta ( check ) == CHECK_STR:
            # Migra da versao 0.0.8 para 0.0.9
            if len(check.split('#')) < 2:
                migra (self.smanager.encrypter)
            return True
        else:
            return False
     
        
    def do_unlock (self):

        senha = self.ids.tx_password.text
        self.smanager.encrypter = Encriptador (senha)
        # verifica se a senha e correta
        if not self.check_pass():
            print "senha errada"
            self.ids.tx_aviso.text = 'As senha nao confere!'
            return False
        
        from telas.collect import JanelaCollect
        janela = JanelaCollect(smanager=self.smanager, name='janela_collect')
        self.smanager.add_widget( janela )
        janela.recarrega()
        self.smanager.transition.direction = 'up'
        self.smanager.current = 'janela_collect'
    
    
    
    
class JanelaFirstLogin (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        self.last_window = last_window
        super(JanelaFirstLogin, self).__init__(**kwargs)
        self.smanager = smanager
    
    def on_leave(self):
        self.smanager.remove_widget (self)   
        
    def do_unlock (self):
        senha = self.ids.tx_password.text
        senha2 = self.ids.tx_password_confirm.text
    
        if (senha != senha2):
            self.ids.tx_aviso.text = 'As senhas nao conferem!'
            return False
        else:
            self.smanager.encrypter = Encriptador (senha)
            f = open (CHECK_FILE, 'w')
            f.write ( self.smanager.encrypter.encripta (CHECK_STR) )
            f.close()
            
            from telas.collect import JanelaCollect
            janela = JanelaCollect(smanager=self.smanager, name='janela_collect')
            self.smanager.add_widget( janela )
            janela.recarrega()
            self.smanager.transition.direction = 'up'
            self.smanager.current = 'janela_collect'
            
            #janela = self.smanager.get_screen('janela_collect')
            #janela.recarrega()
            ## faz uma verificacao pra ver se ta certa
            #self.smanager.transition.direction = 'up'
            #self.smanager.current = 'janela_collect'
        
        
        
        