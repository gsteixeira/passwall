from kivy.uix.screenmanager import Screen
#from kivy.lang import Builder

# -*- coding: utf-8 -*-
from models.senhas import Senha, Collection

from kivy.uix.button import Button
#from kivy.uix.label import Label
#from kivy.uix.checkbox import CheckBox
#from kivy.uix.dropdown import DropDown
from kivy.core.clipboard import Clipboard

from kivy.uix.gridlayout import GridLayout


from telas.utilities import Confirma
#from telas.collect import JanelaEditCollect
#from telas.collect import JanelaAddPass, JanelaEditCollect

#from kivy.uix.behaviors import DragBehavior, ButtonBehavior

class JanelaPassView (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        
        super(JanelaPassView, self).__init__(**kwargs)
        self.last_window = last_window
        self.smanager = smanager
    
    def setup (self, passwd=None):
        self.passwd = passwd
        self.ids.tx_desc.text = self.smanager.encrypter.decripta ( passwd.desc )
        self.ids.pass_field.text = '******'
        
    
    def show (self):
        modo = self.ids.butt_show.text
        if modo == 'show':
            self.ids.pass_field.text = self.smanager.encrypter.decripta ( self.passwd.valor )
            self.ids.butt_show.text = 'hide'
        else:
            self.ids.pass_field.text = '******'
            self.ids.butt_show.text = 'show'
    
    def on_leave (self):
        self.smanager.remove_widget(self)
        
    def _really_delete(self, really):
        if really:
            self.passwd.delete_instance(recursive=True)
            self.voltar()
            
    def delete (self):
        p = Confirma (callback=self._really_delete, text='Remover senha?')
        p.open()
        
    def edit (self):
        janela = JanelaEditPass(smanager=self.smanager, name='janela_edit_pass') 
        self.smanager.add_widget( janela )
        janela.setup(self.passwd)
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_edit_pass'
        
    def clip (self):
        Clipboard.put(self.smanager.encrypter.decripta ( self.passwd.valor ), 'UTF8_STRING')
        
    def voltar (self):
        self.ids.pass_field.text = ''
        self.ids.tx_desc.text = ''
        
        #janela = self.smanager.get_screen('janela_pass_list')
        from telas.passwd import JanelaPassList
        janela = JanelaPassList( smanager=self.smanager, name='janela_pass_list')
        self.smanager.add_widget( janela )
        janela.setup(col=self.passwd.collect)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_list'
    
class JanelaPassList (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        self.last_window = last_window
        super(JanelaPassList, self).__init__(**kwargs)
        self.ids.area_pass.bind(minimum_height=self.ids.area_pass.setter('height'))
        self.smanager = smanager
    
    def setup (self, col=None):
        self.collection = col
        self.ids.nome_colecao.text = self.smanager.encrypter.decripta (self.collection.nome)
        
        self.recarrega()
        #self.ids.area_pass.clear_widgets()
        #sens = Senha.select().where( Senha.collect==self.collection )
        #for s in sens:
            #b = ItemPass (passwd=s, smanager=self.smanager)
            #self.ids.area_pass.add_widget(b)
    def on_pre_enter(self):
        self.recarrega()
        
    def recarrega (self):
        self.ids.area_pass.clear_widgets()
        sens = Senha.select().where( Senha.collect==self.collection )
        for s in sens:
            b = ItemPass (passwd=s, smanager=self.smanager)
            self.ids.area_pass.add_widget(b)
    
    def on_leave (self):
        self.smanager.remove_widget(self)
        
    def add (self):
        #janela = self.smanager.get_screen('janela_add_pass')
        from telas.passwd import JanelaAddPass
        janela = JanelaAddPass(smanager=self.smanager, name='janela_add_pass')
        self.smanager.add_widget( janela )
        
        janela.setup (col=self.collection)
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_add_pass'
    
    def edit_collect (self):
        from telas.collect import JanelaEditCollect
        janela = JanelaEditCollect(smanager=self.smanager, name='janela_edit_collect') 
        self.smanager.add_widget( janela )
        janela.setup (self.collection)
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_edit_collect'
        
    def voltar (self):
        from telas.collect import JanelaCollect
        janela = JanelaCollect(smanager=self.smanager, name='janela_collect')
        self.smanager.add_widget( janela )
        janela.recarrega()
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_collect'
        
        #janela = self.smanager.get_screen('janela_collect')
        #janela.recarrega()
        #self.smanager.transition.direction = 'right'
        #self.smanager.current = 'janela_collect'
    
    

class ItemPass (Button):
    def __init__ (self, passwd, smanager=None, **kwargs):
        super(ItemPass, self).__init__(**kwargs)
        self.passwd = passwd
        self.smanager = smanager
        self.text = self.smanager.encrypter.decripta (passwd.desc)
        
        
    def on_release (self, **kwargs):
        super(ItemPass, self).on_release(**kwargs)
        #jan = JanelaPassList( col=self.collection, name='janela_pass_list')
        #self.smanager.add_widget( jan )
        #janela = self.smanager.get_screen('janela_pass_view')
        from telas.passwd import JanelaPassView
        janela = JanelaPassView(smanager=self.smanager, name='janela_pass_view')
        self.smanager.add_widget( janela )
        
        janela.setup (passwd=self.passwd)
    
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_pass_view'
    
   

   
class JanelaAddPass (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        super(JanelaAddPass, self).__init__(**kwargs)
        self.last_window = last_window
        self.smanager = smanager
        self.collect = None
        
    def setup (self, col=None):
        self.collect = col
    
    def salvar (self):
        s = Senha()
        s.collect = self.collect
        s.desc = self.smanager.encrypter.encripta (self.ids.tx_desc.text)
        s.valor = self.smanager.encrypter.encripta (self.ids.tx_password.text)
        s.save()
        # Vai pra view
        from telas.passwd import JanelaPassView
        janela = JanelaPassView(smanager=self.smanager, name='janela_pass_view')
        self.smanager.add_widget( janela )
        
        #janela = self.smanager.get_screen('janela_pass_view')
        janela.setup (passwd=s)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_view'
       
       
    def on_leave (self):
        self.smanager.remove_widget(self)
        
    def on_pre_enter(self):
        self.ids.tx_desc.text = ''
        self.ids.tx_password.text = ''
        
    def add (self, data):
        c = Collection()
        c.desc = data['desc']
        c.valor = self.enc.encripta( data['valor'] )
        c.collect = self.collect
        c.save()
        
    def voltar (self):
        #janela = self.smanager.get_screen('janela_pass_list')
        from telas.passwd import JanelaPassList
        janela = JanelaPassList(smanager=self.smanager, name='janela_pass_list')
        self.smanager.add_widget( janela )
        janela.setup(col=self.collect)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_list'
        
        
        
class JanelaEditPass (JanelaAddPass):
    def setup (self, passwd):
        self.passwd = passwd
    
    def on_pre_enter(self):
        self.ids.tx_desc.text = self.smanager.encrypter.decripta (self.passwd.desc)
        try:
            self.ids.tx_password.text = self.smanager.encrypter.decripta (self.passwd.valor)
        except:
            self.ids.tx_password.text = ''
    
    def on_leave(self):
        self.smanager.remove_widget (self)
        
    def voltar (self):
        #janela = self.smanager.get_screen('janela_pass_view')
        from telas.passwd import JanelaPassView
        janela = JanelaPassView(smanager=self.smanager, name='janela_pass_view')
        self.smanager.add_widget( janela )
        
        janela.setup (passwd=self.passwd)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_view'
        
    def salvar (self):
        s = self.passwd
        s.collect = self.passwd.collect
        s.desc = self.smanager.encrypter.encripta (self.ids.tx_desc.text)
        if (self.ids.tx_password.text):
            s.valor = self.smanager.encrypter.encripta (self.ids.tx_password.text)
        s.save()
        self.passwd = s
        #janela = self.smanager.get_screen('janela_pass_view')
        
        from telas.passwd import JanelaPassView
        janela = JanelaPassView(smanager=self.smanager, name='janela_pass_view')
        self.smanager.add_widget( janela )
        
        janela.setup (passwd=s)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_view'
        
        
        