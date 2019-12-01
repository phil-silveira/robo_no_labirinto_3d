import random
from direcoes import Direcoes


def setup(self):
    """
        Inicializacao.
    """
    self.lista_de_comandos = []  # limpa lista de comandos
    self.lista_de_comandos.append(self.Estados.ANDA1)  # adiciona comando inicial a lista

    # variaveis auxiliares
    #  ...
    

def loop(self):

    '''
        Mapeamento em duas etapas:
        - etapa 1: costear o mapa pela direita até delimitar sua margem
        - etapa 2: percorrer as regiaos do mapa ainda desconhecidas. como ????        
    '''


    # Etapa 1 - costear o mapa pela direita até delimitar sua margem
    if self.estado == self.Estados.PARA:
        print(self.mapa.celulas)

        if self.aberto_direita():
            self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
            self.lista_de_comandos.append(self.Estados.ANDA1)
        elif self.aberto_adiante():
            self.lista_de_comandos.append(self.Estados.ANDA1)

        elif self.aberto_esquerda():
            self.lista_de_comandos.append(self.Estados.GIRA_ESQUERDA)
            self.lista_de_comandos.append(self.Estados.ANDA1)
        else:
            self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
            self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
            self.lista_de_comandos.append(self.Estados.ANDA1)
            
