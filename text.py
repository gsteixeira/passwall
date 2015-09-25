from models.senhas import Senha, Collection










class Menu():
    """
        Esta classe exibe um menu e executa a funcao correspondente a opcao do usuario
        
    """
    def __init__ (self, txt_opts, funopts, funargs=None, default="0"):
        self.txt_opts = txt_opts
        self.funopts = funopts
        self.default = default
        self.run()
        
    def run (self):
        var = None
        while ( var != "0" ):
            cls()
            print self.txt_opts
            var = raw_input ('Selecione a opção?')
            if not var:
                print "nao informou nada"
                var = self.default
            self.funopts[var]()
            #try:
            #   self.funopts[var]()
            #   
            #except (KeyboardInterrupt, SystemExit):
            #   print "Parada solicitada..."
            #   sys.exit(0)
            #except:
            #   print "Opcao invalida\n-------------------"
            #   print "Unexpected error:", sys.exc_info()
        return True
    
    
    
def main_menu ():
            
            opts = """
            
        Escolha a Opção:
            1 - Listar Colecoes 
            -------------------
            0 - Menu principal
            """
            default = "1"
            
        funopts = {
            '1': lista_colecoes,
            '0': nada,
            }
    cls()
    
    
    return Menu(opts, funopts, None, default)