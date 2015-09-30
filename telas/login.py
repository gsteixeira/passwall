# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
#from kivy.lang import Builder


CHECK_FILE = '../databases/var/db/pcheck.chk'
CHECK_STR = 'this should be readable'



from utils import Encriptador
import os



import hashlib




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
            
            
            
            
    def check_pass (self):
        f = open (CHECK_FILE, 'r')
        check = f.read()
        f.close()
        if self.smanager.encrypter.decripta ( check ) == CHECK_STR:
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
        janela = self.smanager.get_screen('janela_collect')
        janela.recarrega()
        # faz uma verificacao pra ver se ta certa
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
            
            janela = self.smanager.get_screen('janela_collect')
            janela.recarrega()
            # faz uma verificacao pra ver se ta certa
            self.smanager.transition.direction = 'up'
            self.smanager.current = 'janela_collect'
        
        
        
        