from direcoes import Direcoes


class Mapa:
    class CelulaMapa:
        def __init__(self):
            self.aberto_norte = False
            self.aberto_oeste = False
            self.aberto_sul = False
            self.aberto_leste = False
            self.desconhecido = True  # celula nao percorrida
            self.referencia_figura = None

    class MarcadorMapa:
        def __init__(self):
            self.dentro = False
            self.coord_x = 0
            self.coord_y = 0
            self.referencia_figura = None

    def __init__(self):
        self.celulas = []
        self.largura_em_celulas = 11  # em numero de celulas
        self.altura_em_celulas = 11  # em numero de celulas
        self.fator_escala_x = 57  # dimensao X da celula em pixels
        self.fator_escala_y = 60  # dimensao Y da celula em pixels
        self.dist_limite_aberta = 50  # menor distancia para considerar que a parede esta aberta
        self.indice_x_robo = 0  # indice X onde se encontra o robo no mapa
        self.indice_y_robo = 0  # indice Y onde se encontra o robo no mapa

        self.marcadores = []
        self.MARCADORES_POR_CELULA = 5

    def inicializa(self):
        self.celulas = []
        for LY in range(0, self.altura_em_celulas):
            self.celulas.append([])
            for LX in range(0, self.largura_em_celulas):
                self.celulas[LY].append(self.CelulaMapa())
        self.inicializa_marcadores()

    def inicializa_marcadores(self):
        self.marcadores = []
        for LY in range(0, self.altura_em_celulas * self.MARCADORES_POR_CELULA):
            self.marcadores.append([])
            for LX in range(0, self.largura_em_celulas * self.MARCADORES_POR_CELULA):
                self.marcadores[LY].append(self.MarcadorMapa())

        for LY in range(0, self.altura_em_celulas):
            for LX in range(0, self.largura_em_celulas):
                for indice_y in range(0,self.MARCADORES_POR_CELULA):
                    for indice_x in range(0,self.MARCADORES_POR_CELULA):
                        self.marcadores[LY * self.MARCADORES_POR_CELULA + indice_y][LX * self.MARCADORES_POR_CELULA + indice_x].coord_x = LX * self.fator_escala_x + indice_x * self.fator_escala_x / self.MARCADORES_POR_CELULA
                        self.marcadores[LY * self.MARCADORES_POR_CELULA + indice_y][LX * self.MARCADORES_POR_CELULA + indice_x].coord_y = LY * self.fator_escala_y + indice_y * self.fator_escala_y / self.MARCADORES_POR_CELULA
                        self.marcadores[LY * self.MARCADORES_POR_CELULA + indice_y][LX * self.MARCADORES_POR_CELULA + indice_x].referencia_figura = None
                        if (indice_x == 0) or (indice_y == 0):
                            self.marcadores[LY * self.MARCADORES_POR_CELULA + indice_y][LX * self.MARCADORES_POR_CELULA + indice_x].dentro = False
                        else:
                            self.marcadores[LY * self.MARCADORES_POR_CELULA + indice_y][LX * self.MARCADORES_POR_CELULA + indice_x].dentro = True

    def celula_atual(self):
        return self.celulas[self.indice_y_robo][self.indice_x_robo]

    def atualiza(self, coord_x_estimada, coord_y_estimada, dist_frontal, dist_esquerda, dist_direita, direcao):
        class Params:
            BORDA = 0.2
        self.indice_x_robo = int(coord_x_estimada / self.fator_escala_x)
        self.indice_y_robo = int(-coord_y_estimada / self.fator_escala_y)
        
        celula = self.celulas[self.indice_y_robo][self.indice_x_robo]
        
        celula_oeste = None
        celula_leste = None
        celula_norte = None
        celula_sul = None
        
        if self.indice_x_robo > 0:
            celula_oeste = self.celulas[self.indice_y_robo][self.indice_x_robo - 1]
        if self.indice_x_robo < self.largura_em_celulas - 1:
            celula_leste = self.celulas[self.indice_y_robo][self.indice_x_robo + 1]
        if self.indice_y_robo > 0:
            celula_norte = self.celulas[self.indice_y_robo - 1][self.indice_x_robo]
        if self.indice_y_robo < self.altura_em_celulas - 1:
            celula_sul   = self.celulas[self.indice_y_robo + 1][self.indice_x_robo]
        
        celula.desconhecido = False
        coord_x_celula = (coord_x_estimada / self.fator_escala_x - self.indice_x_robo )
        coord_y_celula = (- coord_y_estimada / self.fator_escala_y - self.indice_y_robo )
        if (coord_x_celula > Params.BORDA) and (coord_x_celula < (1 - Params.BORDA)) and (coord_y_celula > Params.BORDA) and (coord_y_celula < (1 - Params.BORDA)):
            dentro = True
        else:
            dentro = False
        if dentro:
            if direcao == Direcoes.OESTE:
                if dist_frontal > self.dist_limite_aberta:
                    celula.aberto_oeste = True
                    if celula_oeste is not None:
                        celula_oeste.aberto_leste = True
                else:
                    celula.aberto_oeste = False
                if dist_esquerda > self.dist_limite_aberta:
                    celula.aberto_sul = True
                    if celula_sul is not None:
                        celula_sul.aberto_norte = True
                else:
                    celula.aberto_sul = False
                if dist_direita > self.dist_limite_aberta:
                    celula.aberto_norte = True
                    if celula_norte is not None:
                        celula_norte.aberto_sul = True                   
                else:
                    celula.aberto_norte = False

            if direcao == Direcoes.LESTE:
                if dist_frontal > self.dist_limite_aberta:
                    celula.aberto_leste = True
                    if celula_leste is not None:
                        celula_leste.aberto_oeste = True
                else:
                    celula.aberto_leste = False
                if dist_esquerda > self.dist_limite_aberta:
                    celula.aberto_norte = True
                    if celula_norte is not None:
                        celula_norte.aberto_sul = True
                else:
                    celula.aberto_norte = False
                if dist_direita > self.dist_limite_aberta:
                    celula.aberto_sul = True
                    if celula_sul is not None:
                        celula_sul.aberto_norte = True                    
                else:
                    celula.aberto_sul = False

            if direcao == Direcoes.NORTE:
                if dist_frontal > self.dist_limite_aberta:
                    celula.aberto_norte = True
                    if celula_norte is not None:
                        celula_norte.aberto_sul = True                    
                else:
                    celula.aberto_norte = False
                if dist_esquerda > self.dist_limite_aberta:
                    celula.aberto_oeste = True
                    if celula_oeste is not None:
                        celula_oeste.aberto_leste = True                    
                else:
                    celula.aberto_oeste = False
                if dist_direita > self.dist_limite_aberta:
                    celula.aberto_leste = True
                    if celula_leste is not None:
                        celula_leste.aberto_oeste = True                    
                else:
                    celula.aberto_leste = False

            if direcao == Direcoes.SUL:
                if dist_frontal > self.dist_limite_aberta:
                    celula.aberto_sul = True
                    if celula_sul is not None:
                        celula_sul.aberto_norte = True                    
                else:
                    celula.aberto_sul = False
                if dist_esquerda > self.dist_limite_aberta:
                    celula.aberto_leste = True
                    if celula_leste is not None:
                        celula_leste.aberto_oeste = True                    
                else:
                    celula.aberto_leste = False
                if dist_direita > self.dist_limite_aberta:
                    celula.aberto_oeste = True
                    if celula_oeste is not None:
                        celula_oeste.aberto_leste = True                    
                else:
                    celula.aberto_oeste = False
