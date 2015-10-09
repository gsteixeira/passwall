# -*- coding: utf-8 -*-
from kivy.uix.popup import Popup

        
class Confirma (Popup):
    def __init__(self, callback=None, text='Confirma?', **kwargs):
        self.callback = callback
        super(Confirma, self).__init__(**kwargs)
        self.title = text
            
        
        
    def anwser (self, value):
        self.callback (value)
        self.dismiss()