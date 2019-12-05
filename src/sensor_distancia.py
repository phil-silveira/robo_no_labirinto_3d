import math


class SensorDistancia:
    DISTANCIA_MAXIMA = 300

    def __init__(self, x, y, angulo):
        # valores relativos em relacao ao robo
        self.coord_x_relativa = x
        self.coord_y_relativa = y
        self.coord_x_alvo = x
        self.coord_y_alvo = y
        self.angulo_relativo = angulo
        self.distancia = self.DISTANCIA_MAXIMA
        self.coord_x_ini_varredura = 0
        self.coord_y_ini_varredura = 0
        self.coord_x_fim_varredura = 0
        self.coord_y_fim_varredura = 0
        self.referencia_figura = None

    def inicializa(self):
        self.distancia = self.DISTANCIA_MAXIMA

    def determina_distancia_obstaculo(self, coord_x_absoluta, coord_y_absoluta, angulo_absoluto, obstaculo):
        """
        Determina a distancia do sensor ao obstaculo.

        Realiza uma varredura iniciando em x,y (coordenadas absolutas do sensor).
        O angulo da varredura eh o angulo absoluto do sensor (soma do angulo do robo com o angulo relativo do sensor).
        """
        x1 = obstaculo[0]
        y1 = obstaculo[1]
        x2 = obstaculo[2]
        y2 = obstaculo[3]
        self.coord_x_ini_varredura = coord_x_absoluta
        self.coord_y_ini_varredura = coord_y_absoluta
        # a varredura eh realizada sempre ate o obstaculo mais proximo ja encontrado
        for progressao in range(0, self.distancia):
            coord_x_varredura = coord_x_absoluta + \
                progressao * math.cos(angulo_absoluto)
            coord_y_varredura = coord_y_absoluta + \
                progressao * math.sin(angulo_absoluto)
            self.coord_x_fim_varredura = coord_x_varredura
            self.coord_y_fim_varredura = coord_y_varredura
            # verifica se o ponto esta dentro do objeto
            # considerar que as coordenadas sao negativas
            if (coord_x_varredura > x1) and (coord_x_varredura < x2) and (coord_y_varredura < y1) and (coord_y_varredura > y2):
                if self.distancia > progressao:
                    self.distancia = progressao
                break
        self.coord_x_alvo = self.coord_x_relativa + \
            self.distancia * math.cos(self.angulo_relativo)
        self.coord_y_alvo = self.coord_y_relativa + \
            self.distancia * math.sin(self.angulo_relativo)
