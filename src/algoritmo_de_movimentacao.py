import random
from direcoes import Direcoes


def setup(self):
    """
        Inicializacao.
    """
    self.lista_de_comandos = []  # limpa lista de comandos
    self.lista_de_comandos.append(self.Estados.ANDA1)  # adiciona comando inicial a lista

    # exemplo de variavel adicional
    # self.variavel = 10

def loop(self):

    """
        # Campos importantes:

        # direcao do robo; pode ser Direcoes.LESTE, Direcoes.NORTE, Direcoes.SUL, Direcoes.OESTE
        self.direcao

        # indices do robo no mapa
        self.mapa.indice_x_robo e self.mapa.indice_y_robo

        # mapa, com indicacao das paredes:
        self.mapa.celulas[self.mapa.indice_y_robo][self.mapa.indice_x_robo]
        self.mapa.celulas[self.mapa.indice_y_robo][self.mapa.indice_x_robo].aberto_leste
        self.mapa.celulas[self.mapa.indice_y_robo][self.mapa.indice_x_robo].aberto_oeste
        self.mapa.celulas[self.mapa.indice_y_robo][self.mapa.indice_x_robo].aberto_norte
        self.mapa.celulas[self.mapa.indice_y_robo][self.mapa.indice_x_robo].aberto_sul

        # lista de comandos:
        self.lista_de_comandos

        # adicao de comando:
        self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)  # gira para a direita 90 graus
        self.lista_de_comandos.append(self.Estados.GIRA_ESQUERDA)  # gira para a esquerda 90 graus
        self.lista_de_comandos.append(self.Estados.ANDA1)  # anda 1 celula para a frente
        self.lista_de_comandos.append(self.Estados.ANDA)  # anda ate atingir uma parede
        self.lista_de_comandos.append(self.Estados.PARA)


        # Exemplo de algoritmo de controle aleatorio
        r = random.randint(0,4)
        if (r==0):
            self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
        if (r==1):
            self.lista_de_comandos.append(self.Estados.GIRA_ESQUERDA)
        if (r==2):
            self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
            self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
        if (r==3):
            self.lista_de_comandos.append(self.Estados.ANDA1)  # Anda 1 celula para frente no mapa

        # Exemplo de acesso ao mapa (atualizado dinamicamente)
        robo_indice_x_atual = self.mapa.indice_x_robo
        robo_indice_y_atual = self.mapa.indice_y_robo
        if self.direcao == Direcoes.LESTE:
           if self.mapa.celulas[robo_indice_y_atual][robo_indice_x_atual].aberto_leste:
               self.lista_de_comandos.append(self.Estados.ANDA1)
    """

    '''
        Mapeamento em duas etapas:
        - etapa 1: costear o mapa pela direita até delimitar sua margem
        - etapa 2: percorrer as regiaos do mapa ainda desconhecidas. como ????        
    '''


    # Etapa 1 - costear o mapa pela direita até delimitar sua margem
    if self.estado == self.Estados.PARA:
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
            
