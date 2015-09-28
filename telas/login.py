from kivy.uix.screenmanager import Screen
#from kivy.lang import Builder



from utils import Encriptador


class JanelaLogin (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        self.last_window = last_window
        super(JanelaLogin, self).__init__(**kwargs)
        self.smanager = smanager
        
        
    def do_unlock (self):
        senha = self.ids.tx_password.text
        print senha
        self.manager.encrypter = Encriptador (senha)
        # faz uma verificacao pra ver se ta certa
        self.manager.transition.direction = 'right'
        self.manager.current = 'janela_collect'
        