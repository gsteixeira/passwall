# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
from Crypto.Cipher import AES


import hashlib


AES_BLOCK_SIZE = 256  # Tamanho do bloco AES
AES_IV = 16 * '\x00' # Initialization vector do AES


class Encriptador(object):
    def __init__ (self, senha):
        senha_hash = hashlib.md5 (senha)
        self.chave_aes = senha_hash.hexdigest()

    def _pad (self, txt):
        bs = AES_BLOCK_SIZE
        length = bs - (len(txt) % bs)
        txt += chr(length)*length
        return txt

    def _unpad (self, txt):
        
        return txt[0:-ord(txt[-1])]
        
    def encripta (self, txt):
        enc = AES.new(
                self.chave_aes,
                AES.MODE_CBC,
                AES_IV
            )
        ciphertext = enc.encrypt( self._pad(txt) )
        b64_txt = b64encode (ciphertext)
        #return b64_txt
        # valid chars + / =
        # replace     - _ !
        #             < > ?
        crypt_txt = b64_txt.replace('+','<').replace('/','>').replace('=','?')
        return crypt_txt

    def decripta (self, crypt_txt):
        ciphertext = crypt_txt.replace('<','+').replace('>','/').replace('?','=')
        b64_txt = b64decode ( ciphertext )
        #b64_txt = b64decode ( crypt_txt )
        enc = AES.new(
                self.chave_aes,
                AES.MODE_CBC,
                AES_IV
            )
        txt = enc.decrypt( b64_txt )
        return self._unpad(txt)


# user abre o programa
# pede a senha, faz o hash e guarda numa variavel CHAVE_AES
# testa se ta certa, continua, senao volta
# se de certo tu tem um encriptador com a chave setada, so usalo daqui pra frente
# 


#Sincronizacao
#A B
# qdo grava, sync=False, last_update=agora
# qdo for sincronizar: ver
# opcao A: pela rede : abrir um socket e conversar por REST
# opcao B: USB -> direto no arquivo
# opcao C: programa servidor o cara tem q instalar na maquina
