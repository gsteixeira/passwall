from kivy.uix.screenmanager import Screen
#from kivy.lang import Builder


from models.senhas import Senha, Collection

from kivy.uix.button import Button
#from kivy.uix.label import Label
#from kivy.uix.checkbox import CheckBox
#from kivy.uix.dropdown import DropDown

from kivy.uix.gridlayout import GridLayout
#from kivy.uix.behaviors import DragBehavior, ButtonBehavior

class JanelaPassList (Screen):
    def __init__(self, col=None, last_window=None, **kwargs):
        self.last_window = last_window
        self.collection = col
        super(JanelaPassList, self).__init__(**kwargs)
        self.ids.area_pass.bind(minimum_height=self.ids.area_pass.setter('height'))
        
        
        
        
        sens = Senha.select().where( Senha.collect=self.collection )
        for s in sens:
            print s.desc
            #b = ItemColecao (c)
            #self.ids.area_collects.add_widget(b)
    
    
    
    
    