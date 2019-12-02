import random
from direcoes import Direcoes


def setup(self):
    """
        Inicializacao.
    """
    self.lista_de_comandos = []  # limpa lista de comandos
    self.lista_de_comandos.append(self.Estados.ANDA1)  # adiciona comando inicial a lista

    # variaveis auxiliares
    self._initial_position = self.mapa.celula_atual()
    self._already_round_maze = None
    self._is_step_1_completed = None
    self._already_round_maze = None

def loop(self):

    '''
        Mapeamento em duas etapas:
        - etapa 1: costear o mapa pela direita até delimitar sua margem
        - etapa 2: percorrer as regiaos do mapa ainda desconhecidas. como ????        
    '''


    if self.estado == self.Estados.PARA:
        if self._initial_position == self.mapa.celula_atual():
            self._is_step_1_completed = True if self._is_step_1_completed == False else False 

        # Etapa 1 - costear o mapa pela direita até delimitar sua margem
        if not self._is_step_1_completed:
            get_around_the_maze_by_the_right(self)

        # # Etapa 2 - andar por regiões desconhecidas
        # elif not self._is_step_2_completed:
        #     explore_unknown_position()
        
        else:
           keep_spinning(self) 

def get_around_the_maze_by_the_right(self):
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

def explore_unknown_position(self):
    current_position = self.mapa.celula_atual()

    def get_position_index_on_map(position):
        for i in range(len(self.mapa.celulas)):
            for j in range(len(self.mapa.celulas[0])):
                if self.mapa.celulas[i][j] == current_position:
                    return (i, j) 
        return None

    position = get_position_index_on_map(current_position)

    self.sensor_distancia[0] 

    self.mapa.celulas[position[0]][position[1]]

    get_around_the_maze_by_the_right(self)

def keep_spinning(self):
    self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
    self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
    self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
    self.lista_de_comandos.append(self.Estados.GIRA_DIREITA)
