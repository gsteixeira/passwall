# -*- coding: utf-8 -*-
from kivy.uix.popup import Popup

from kivy.uix.screenmanager import Screen
from models.senhas import Senha, Collection

import sqlite3
#import sqlitebck
        
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj






class Confirma (Popup):
    def __init__(self, callback=None, text='Confirm?', **kwargs):
        self.callback = callback
        super(Confirma, self).__init__(**kwargs)
        self.title = text
        
    def anwser (self, value):
        self.callback (value)
        self.dismiss()
        
        
        
        

class JanelaSettings (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        super(JanelaSettings, self).__init__(**kwargs)
        
        self.last_window = last_window
        self.smanager = smanager
        
    def call_backups (self):
        from telas.utilities import JanelaBackup
        janela = JanelaBackup(smanager=self.smanager, name='janela_backup')
        self.smanager.add_widget( janela )
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_backup'
        
    def do_erasedb (self):
        p = Confirma (callback=self.really_erasedb, text='Erase Database, Really?')
        p.open()
        
    def really_erasedb (self, value):
        if value:
            from models.senhas import DB_FILE
            import os
            from models.senhas import Senha, Collection
            from peewee import SqliteDatabase
            try:
                os.remove (DB_FILE)
            except:
                pass
            db = SqliteDatabase(DB_FILE)
            db.connect()
            db.create_tables([ Collection, Senha ], safe=True)
            
        
    def voltar (self):
        from telas.collect import JanelaCollect
        janela = JanelaCollect(smanager=self.smanager, name='janela_collect')
        self.smanager.add_widget( janela )
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_collect'
        
        
       

def dump_2plain_text(filename, encrypter):
    cols = Collection.select()
    f = open(filename, 'w')
    for c in cols:
        f.write (u'# %s - %s \n' % (encrypter.decripta (c.nome),c.last_updt))
        sens = Senha.select().where( Senha.collect==c )
        for s in sens:
            f.write (u'>     %s - %s - %s \n' % (
                encrypter.decripta (s.desc), 
                encrypter.decripta (s.valor), 
                s.last_updt))
    f.close()
    
    
class JanelaBackup (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        super(JanelaBackup, self).__init__(**kwargs)
        
        self.last_window = last_window
        self.smanager = smanager
        
    
    def do_backup (self):
        self.ids.lb_result.text = 'Wait...'
        self.copy_bkp('bkp')
        self.ids.lb_result.text = 'Backup done!'
        
    def do_restore (self):
        self.ids.lb_result.text = 'Wait...'
        p = Confirma (callback=self.really_restore, text='Restore from backup?')
        p.open()
        
    def do_dump_2plaintext(self):
        """
            Dump all data into plain text file
        """
        self.ids.lb_result.text = 'Wait...'
        bkp_file = self.ids.tx_bkppath.text
        try:
            dump_2plain_text(bkp_file, self.smanager.encrypter)
            self.ids.lb_result.text = 'Dump done! Keep it safe!!!'
        except:
            self.ids.lb_result.text = 'Error doing backup!!!'
        
    def really_restore (self, value):
        if value:
            self.copy_bkp('restore')
            self.ids.lb_result.text = 'Done Restore!'
        #self.copy_bkp('restore')

    def voltar (self):
        from telas.collect import JanelaCollect
        janela = JanelaCollect(smanager=self.smanager, name='janela_collect')
        self.smanager.add_widget( janela )
        janela.recarrega()
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_collect'

    def copy_bkp (self, mode='bkp'):
        from models.senhas import DB_FILE
        import shutil
        
        bkp_file = self.ids.tx_bkppath.text
        try:
            if mode == 'bkp':
                shutil.copyfile (data , bkp)
            elif mode == 'restore':
                shutil.copyfile (bkp , data)
        except:
            self.ids.lb_result.text = 'Error doing backup!!!'
        #data = sqlite3.connect(DB_FILE)
        #bkp = sqlite3.connect(bkp_file)
        #if mode == 'bkp':
            #sqlitebck.copy(data , bkp)
        #elif mode == 'restore':
            #sqlitebck.copy(bkp , data)
        #data.close()
        #bkp.close()
        
        
    
    #def json_bkp (self):
        #from playhouse.shortcuts import model_to_dict, dict_to_model
        #from models.senhas import Senha, Collection
        #dumpfile = open ('dump.txt', 'w')
        #collects = Collection.objects.select()
        #for c in collects:
            #dic = model_to_dict (c)
            #txt = json.dumps(dic, default=date_handler)
            #dumpfile.write(txt)
            #dumpfile.write('\n')
            
        #sens = Senha.select()
        #for s in sens:
            #dic = model_to_dict (s)
            #txt = json.dumps(dic, default=date_handler)
            #dumpfile.write(txt)
            #dumpfile.write('\n')
            
        #dumpfile.close()
        ################################################
        
        
        
        
        
        
        
        
        
        #path = self.ids.tx_backuppath.text
        #senhas = Senha.objects.select()
        #for s in senhas:
        #for c in collects:
            
        #user = User.select().dicts().get()
        #print json.dumps(user, default=date_handler)

        
        
        #>>> df= sqlite3.connect(DB_FILE)
        #>>> bf = sqlite3.connect(BKP)
        #>>> sqlitebck.copy(df, bf)

        #json_acceptable_string = html.replace("'", "\"")
        #return json.loads (json_acceptable_string)
        
        #>>> D= model_to_dict(s[0])
        #>>> M = dict_to_model (Senha, D, ignore_unknown=True )

        #>>> X = json.dumps(D, default=date_handler)
        #>>> y = json.loads(X)
        #>>> M = dict_to_model (Senha, y, ignore_unknown=True )


        
        #conn2 = sqlite3.connect('/tmp/in_memory_sqlite_db_save.db')
        #sqlitebck.copy(conn, conn2)
        #conn.close()
        #>>> sqlite3.connect(DB_FILE)
        #<sqlite3.Connection object at 0x7efefa098030>
        #>>> sqlite3.connect(BKP)
        #<sqlite3.Connection object at 0x7efefa098118>
        #>>> import sqlitebck
        #>>> sqlitebck.copy()

        
    
    def on_leave(self):
        self.smanager.remove_widget (self)