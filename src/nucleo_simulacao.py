# -*- coding: utf-8 -*-

import math
from robo import Robo
from mapa import Mapa


class NucleoSimulacao:
    """
        Janela principal de simulacao
    """
    def __init__(self):
        self.robo = None
        self.obstaculos = []

        self.ligado = False
        self.intervalo_de_simulacao = 30

        self.tipo_mapa = 0
        self.altura_labirinto = 430  # pixels
        self.largura_labirinto = 400  # pixels
        self.largura_mapa = 300

        self.mostra_sensores = False
        self.mostra_celulas = False
        
        self.monta_simulacao()

    def liga_desliga(self):
        if not self.ligado:
            self.ligado = True
        else:
            self.ligado = False

    def troca_mapa(self):
        NUM_MAPS = 5

        self.tipo_mapa = (self.tipo_mapa + 1) % NUM_MAPS

        self.monta_simulacao()

    def troca_modo(self):
        if self.robo.ideal:
            self.robo.ideal = False
        else:
            self.robo.ideal = True

    def troca_exibicao_sensores(self):
        self.mostra_sensores = not self.mostra_sensores

    def troca_exibicao_grid(self):
        self.mostra_celulas = not self.mostra_celulas
        
    def monta_simulacao(self):
        self.robo = None

        if self.tipo_mapa == 0:
            self.robo = Robo(30, -30, 0, 10)
        elif self.tipo_mapa == 1:
            self.robo = Robo(370, -30, -math.pi / 2, 10)
        elif self.tipo_mapa == 2:
            self.robo = Robo(30, -270, 0, 10)
        elif self.tipo_mapa == 3:
            self.robo = Robo(30, -270, 0, 10)
        elif self.tipo_mapa == 4:
            self.robo = Robo(30, -30, 0, 10)

        self.monta_obstaculos()

    def monta_obstaculos(self):
        """
            Adiciona as paredes do labirinto
        """
        self.obstaculos = []

        # Moldura
        self.obstaculos.append([0, 0, 5, -self.altura_labirinto])
        self.obstaculos.append([self.largura_labirinto - 5, 0, self.largura_labirinto, -self.altura_labirinto])
        self.obstaculos.append([0, 0, self.largura_labirinto, -5])
        self.obstaculos.append([0, -(self.altura_labirinto - 5), self.largura_labirinto, -self.altura_labirinto])

        if self.tipo_mapa == 0:
            # Barreiras - Conjunto 1
            self.obstaculos.append([0, -60, self.largura_labirinto - 60, -65])
            self.obstaculos.append([60, -120, self.largura_labirinto, -125])
            self.obstaculos.append([0, -180, self.largura_labirinto - 60, -185])
            self.obstaculos.append([60, -240, self.largura_labirinto, -245])
            self.obstaculos.append([0, -300, self.largura_labirinto - 60, -305])
            self.obstaculos.append([60, -360, self.largura_labirinto, -365])

        if self.tipo_mapa == 1:
            # Barreiras - Conjunto 2
            self.obstaculos.append([self.largura_labirinto - 65, 0, self.largura_labirinto - 60, -65])
            self.obstaculos.append([60, -self.altura_labirinto + 65, 65, -self.altura_labirinto])
            self.obstaculos.append([0, -60, self.largura_labirinto - 60, -65])
            self.obstaculos.append([60, -120, self.largura_labirinto, -125])
            self.obstaculos.append([self.largura_labirinto / 2 + 30, -180, self.largura_labirinto, -185])
            self.obstaculos.append([0, -180, self.largura_labirinto / 2 - 30, -185])
            self.obstaculos.append([self.largura_labirinto / 2 + 30, -240, self.largura_labirinto, -245])
            self.obstaculos.append([0, -240, self.largura_labirinto / 2 - 30, -245])
            self.obstaculos.append([0, -300, self.largura_labirinto - 60, -305])
            self.obstaculos.append([60, -360, self.largura_labirinto, -365])

        if self.tipo_mapa == 2:
            # Barreiras - Conjunto 3
            self.obstaculos.append([self.largura_labirinto - 65, 0, self.largura_labirinto - 60, -65])
            self.obstaculos.append([60, -self.altura_labirinto + 65, 65, -self.altura_labirinto])
            self.obstaculos.append([0, -60, self.largura_labirinto - 60, -65])
            self.obstaculos.append([60, -120, self.largura_labirinto, -125])
            self.obstaculos.append([60, -180, self.largura_labirinto - 60, -185])
            self.obstaculos.append([60, -240, self.largura_labirinto - 60, -245])
            self.obstaculos.append([0, -300, self.largura_labirinto - 60, -305])
            self.obstaculos.append([60, -360, self.largura_labirinto, -365])

        if self.tipo_mapa == 3:
            # Barreiras - Conjunto 4
            self.obstaculos.append([self.largura_labirinto - 65, 0, self.largura_labirinto - 60, -65])
            self.obstaculos.append([60, -self.altura_labirinto + 65, 65, -self.altura_labirinto])
            self.obstaculos.append([self.largura_labirinto / 2, -180, self.largura_labirinto / 2 + 5, -240])
            self.obstaculos.append([0, -60, self.largura_labirinto - 60, -65])
            self.obstaculos.append([60, -120, self.largura_labirinto, -125])
            self.obstaculos.append([60, -180, self.largura_labirinto - 60, -185])
            self.obstaculos.append([60, -240, self.largura_labirinto - 60, -245])
            self.obstaculos.append([0, -300, self.largura_labirinto - 60, -305])
            self.obstaculos.append([60, -360, self.largura_labirinto, -365])

        if self.tipo_mapa == 4:
            # Barreiras - Conjunto 5
            self.obstaculos.append([0, -60, self.largura_labirinto - 60, -65])
            self.obstaculos.append([60, -360, self.largura_labirinto, -365])
        
    def executa(self):
        if not self.ligado:
            return()    
        self.robo.dinamica_robo(self.obstaculos)
