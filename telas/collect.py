# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
#from kivy.lang import Builder


from models.senhas import Senha, Collection

from kivy.uix.button import Button
#from kivy.uix.label import Label
#from kivy.uix.checkbox import CheckBox
#from kivy.uix.dropdown import DropDown

from kivy.uix.gridlayout import GridLayout
#from telas.passwd import JanelaPassList
import sys
#from kivy.uix.behaviors import DragBehavior, ButtonBehavior

class JanelaCollect (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        super(JanelaCollect, self).__init__(**kwargs)
        
        self.last_window = last_window
        self.ids.area_collects.bind(minimum_height=self.ids.area_collects.setter('height'))
        self.smanager = smanager
        self.recarrega()
        
    def recarrega (self):
        self.ids.area_collects.clear_widgets()
        cols = Collection.select()
        for c in cols:
            b = ItemColecao (c, smanager=self.smanager)
            self.ids.area_collects.add_widget(b)
            
    def on_pre_enter(self):
        self.recarrega()
    
    def add (self):
        
        janela = self.smanager.get_screen('janela_add_collect')
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_add_collect'
        
            
    def voltar (self):
        sys.exit(0)
        


class ItemColecao (Button):
    def __init__ (self, col, smanager=None, **kwargs):
        super(ItemColecao, self).__init__(**kwargs)
        self.collection = col
        self.text = col.nome
        self.smanager = smanager
        
    def on_release (self, **kwargs):
        super(ItemColecao, self).on_release(**kwargs)
        #jan = JanelaPassList( col=self.collection, name='janela_pass_list')
        #self.manager.add_widget( jan )
        janela = self.smanager.get_screen('janela_pass_list')
        janela.setup (col=self.collection)
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_pass_list'
        
        
        
        
class JanelaAddCollect (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        super(JanelaAddCollect, self).__init__(**kwargs)
        self.last_window = last_window
        self.smanager = smanager
        
    def on_pre_enter(self):
        self.ids.tx_nome.text = ''
        
    def salvar (self):
        c = Collection()
        c.nome = self.ids.tx_nome.text
        c.save()
        # Vai pra view
        janela = self.smanager.get_screen('janela_pass_list')
        janela.setup (col=c)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_list'
        
    def voltar (self):
        janela = self.smanager.get_screen('janela_collect')
        janela.recarrega()
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_collect'
    
        
        
class JanelaEditCollect (JanelaAddCollect):
    def setup (self, col):
        self.collect = col
    
    def on_pre_enter(self):
        self.ids.tx_nome.text = self.collect.nome
    
    
    def salvar (self):
        c = self.collect
        c.nome = self.ids.tx_nome.text
        c.save()
        # Vai pra view
        janela = self.smanager.get_screen('janela_pass_list')
        janela.setup (col=c)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_list'
        #self.smanager.switch_to = 'janela_pass_list'
        