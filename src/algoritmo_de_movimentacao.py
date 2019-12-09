import random
from direcoes import Direcoes
from enum import Enum 


class MazeMappingState(Enum):
    IDLE = 'IDLE'
    GET_AROUND_MAZE_BY_RIGHT = 'GET_AROUND_MAZE_BY_RIGHT'
    EXPLORE_UNKONWN_POSITIONS = 'EXPLORE_UNKONWN_POSITIONS'

def setup(self):
    """
        Inicializacao.
    """
    self.lista_de_comandos = []  # limpa lista de comandos
    # adiciona comando inicial a lista
    self.lista_de_comandos.append(self.Estados.ANDA1)

    # variaveis auxiliares
    self._initial_position = self.mapa.celula_atual()
    self.maze_mapping_state = MazeMappingState.GET_AROUND_MAZE_BY_RIGHT


def loop(self):
    '''
        Mapeamento em duas etapas:
        - etapa 1: costear o mapa pela direita até delimitar sua margem
        - etapa 2: percorrer as regiaos do mapa ainda desconhecidas. como ????
    '''

    if self.estado == self.Estados.PARA:
        explore_unknown_positions(self)


def get_around_the_maze_by_the_right(self):
    if self.aberto_direita():
        self.lista_de_comandos += [self.Estados.GIRA_DIREITA, self.Estados.ANDA1]

    elif self.aberto_adiante():
        self.lista_de_comandos += [self.Estados.ANDA1]

    elif self.aberto_esquerda():
        self.lista_de_comandos += [self.Estados.GIRA_ESQUERDA, self.Estados.ANDA1]

    else:
        self.lista_de_comandos += [self.Estados.GIRA_DIREITA, self.Estados.GIRA_DIREITA, self.Estados.ANDA1]


def explore_unknown_positions(self):
    if self.aberto_direita() and _is_right_position_unknown(self):
        self.lista_de_comandos += [self.Estados.GIRA_DIREITA, self.Estados.ANDA1]
        print('*** UNKNOWN RIGHT')

    elif self.aberto_adiante() and _is_front_position_unknown(self):
        self.lista_de_comandos += [self.Estados.ANDA1]
        print('*** UNKNOWN FRONT')

    elif self.aberto_esquerda() and _is_left_position_unknown(self):
        self.lista_de_comandos += [self.Estados.GIRA_ESQUERDA, self.Estados.ANDA1]
        print('*** UNKNOWN LEFT')

    
    else:
        get_around_the_maze_by_the_right(self)

   
def _is_left_position_unknown(self):
    direction_to_index = {
        Direcoes.NORTE: (0,-1),
        Direcoes.LESTE: (-1,0),
        Direcoes.SUL: (0,1),
        Direcoes.OESTE: (1,0),
    }

    current_position = _get_position_index_on_map(self)

    index = direction_to_index[self.direcao]

    return self.mapa.celulas[current_position[0] + index[0]][current_position[1] + index[1]].desconhecido

def _is_front_position_unknown(self):
    direction_to_index = {
        Direcoes.NORTE: (-1,0),
        Direcoes.LESTE: (0,1),
        Direcoes.SUL: (1,0),
        Direcoes.OESTE: (0,-1),
    }

    current_position = _get_position_index_on_map(self)

    index = direction_to_index[self.direcao]

    return self.mapa.celulas[current_position[0] + index[0]][current_position[1] + index[1]].desconhecido

def _is_right_position_unknown(self):
    direction_to_index = {
        Direcoes.NORTE: (0,1),
        Direcoes.LESTE: (1,0),
        Direcoes.SUL: (0,-1),
        Direcoes.OESTE: (-1,0)
    }

    current_position = _get_position_index_on_map(self)

    index = direction_to_index[self.direcao]

    return self.mapa.celulas[current_position[0] + index[0]][current_position[1] + index[1]].desconhecido


def _get_position_index_on_map(self):
        for i in range(len(self.mapa.celulas)):
            for j in range(len(self.mapa.celulas[0])):
                if self.mapa.celulas[i][j] == self.mapa.celula_atual():
                    return [i, j]
        return None