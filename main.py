# -*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0')
__version__ = '0.1.0'

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen

from telas.login import JanelaLogin
#from telas.collect import JanelaCollect, JanelaAddCollect
#from telas.passwd import JanelaPassList, JanelaPassView, JanelaAddPass

from kivy.core.window import Window



class ServApp(App):
    title = 'Passwall'
    encrypter = None
    def build(self):
        Builder.load_file('templates/login.kv')
        Builder.load_file('templates/collect.kv')
        Builder.load_file('templates/passwd.kv')
        Builder.load_file('templates/utilities.kv')
        win = Window.softinput_mode = 'resize'
        
        sm = ScreenManager()
        sm.add_widget(JanelaLogin(smanager=sm, name='janela_login') )
        #sm.add_widget(JanelaPassView(smanager=sm, name='janela_pass_view') )
        #sm.add_widget(JanelaPassList(smanager=sm, name='janela_pass_list') )
        #sm.add_widget(JanelaAddPass(smanager=sm, name='janela_add_pass') )
        #sm.add_widget(JanelaCollect(smanager=sm, name='janela_collect') )
        #sm.add_widget(JanelaAddCollect(smanager=sm, name='janela_add_collect') )
        
        sm.current = 'janela_login'
        return sm
    
    def on_pause (self):
        return True


if __name__ == '__main__':
    ServApp().run()
    
