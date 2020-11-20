# -*- coding: utf-8 -*-
import os
os.environ['KIVY_WINDOW'] = 'sdl2'
import kivy
kivy.require('1.9.0')
__version__ = '0.1.2'

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen

from telas.login import JanelaLogin

from kivy.core.window import Window


class ServApp(App):
    title = 'Passwall'
    encrypter = None
    def build(self):
        Builder.load_file('templates/login.kv')
        Builder.load_file('templates/collect.kv')
        Builder.load_file('templates/passwd.kv')
        Builder.load_file('templates/utilities.kv')
        #print type(Window)
        #win = Window()
        #win = Window.softinput_mode = 'resize'
        
        sm = ScreenManager()
        sm.add_widget(JanelaLogin(smanager=sm, name='janela_login') )
        
        sm.current = 'janela_login'
        return sm
    
    def on_pause (self):
        return True


if __name__ == '__main__':
    ServApp().run()
    
