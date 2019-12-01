import math 
import enum
import random

from direcoes import Direcoes
from sensor_distancia import SensorDistancia
from mapa import Mapa

import algoritmo_de_movimentacao

class Robo:
    """
        Robo

        Variaveis do estado:
            x , y , angulo: posicao do robo no ambiente.
            raio: tamanho do robo.
            vel_motor_direita , vel_motor_esquerda: utilizadas na dinamica do robo
    
    """

    class Params:
        VELOCIDADE_MAXIMA_MOTOR = 2
        REDUCAO_MOTOR_CORREDOR = 0.99  # reducao percentual da velocidade maxima usada no controle. Padrao: 0.99
        REDUCAO_MOTOR_CAMPO_ABERTO = 0.90  # reducao percentual da velocidade maxima usada no controle. Padrao: 0.99
        VARIACAO_MOTORES = 0.1  # variacao aleatoria na velocidade dos motores. Padrao: 0.1 (10% maximo)
        DISTANCIA_MINIMA_PARADA = 15  # distancia minima de uma parede a frente. Padrao: 15
        LARGURA_CORREDOR = 60  # Padrao: 60

    def __init__(self, x, y, angulo, raio):
        self.coord_x = x
        self.coord_y = y
        self.angulo = angulo
        self.direcao = Direcoes.LESTE
        self.raio = raio
        self.vel_motor_direita = 0
        self.vel_motor_esquerda = 0
        self.dist_esquerda_anterior = 0
        self.dist_direita_anterior = 0

        self.mapa = Mapa()
        self.mapa.inicializa()

        self.lista_de_comandos = []
        self.algoritmo_de_movimentacao = algoritmo_de_movimentacao
        self.algoritmo_de_movimentacao.setup(self)

        self.estado = self.Estados.PARA
        self.contagem = 0

        self.sensores_distancia = []

        self.sensores_distancia.append(SensorDistancia(raio, 0, 0))  # sensor frontal
        self.sensores_distancia.append(SensorDistancia(0, raio, math.pi / 2))  # sensor esquerdo
        self.sensores_distancia.append(SensorDistancia(0, -raio, -math.pi / 2))  # sensor direito

        self.retas = []
        self.retas.append([-raio, -raio, raio, -raio, None])  # Roda direita
        self.retas.append([-raio, raio, raio, raio, None])  # Roda esquerda
        self.referencia_figura = None

        self.ideal = True

    def mostra_direcao(self):
        if self.direcao == Direcoes.NORTE:
            print("NORTE")
        if self.direcao == Direcoes.SUL:
            print("SUL")
        if self.direcao == Direcoes.LESTE:
            print("LESTE")
        if self.direcao == Direcoes.OESTE:
            print("OESTE")
        if self.direcao == 0:
            print("INDEFINIDA")

    def determina_direcao(self):
        self.direcao = 0
        if (self.angulo <= math.pi / 4) and (self.angulo > -math.pi / 4):
            self.direcao = Direcoes.LESTE
        if (self.angulo > math.pi / 4) and (self.angulo <= 3 * math.pi / 4):
            self.direcao = Direcoes.NORTE
        if (self.angulo < -math.pi / 4) and (self.angulo >= -3 * math.pi / 4):
            self.direcao = Direcoes.SUL
        if (self.angulo > 3 * math.pi / 4) or (self.angulo < -3 * math.pi / 4):
            self.direcao = Direcoes.OESTE

    class Estados(enum.Enum):
        ANDA = 1  # anda indefinidamente
        ANDA1 = 2  # anda uma celula
        PARA = 3
        GIRA_DIREITA = 4
        GIRA_ESQUERDA = 5

    def mostra_estado(self):
        if self.estado == self.Estados.ANDA:
            print("ANDA")
        if self.estado == self.Estados.ANDA1:
            print("ANDA1")
        elif self.estado == self.Estados.PARA:
            print("PARA")
        elif self.estado == self.Estados.GIRA_DIREITA:
            print("GIRA_DIREITA")
        elif self.estado == self.Estados.GIRA_ESQUERDA:
            print("GIRA_ESQUERDA")
        elif self.estado == self.Estados.GIRA_PARA:
            print("PARA")

    @staticmethod
    def rotaciona(x, y, angulo):
        x_rotacionado = x * math.cos(angulo) - y * math.sin(angulo)
        y_rotacionado = x * math.sin(angulo) + y * math.cos(angulo)
        return x_rotacionado, y_rotacionado

    def atualiza_sensores(self, lista_obstaculos):
        """
            Atualiza a leitura dos sensores
        """
        for sensor in self.sensores_distancia:
            sensor.inicializa()
        for obstaculo in lista_obstaculos:
            for sensor in self.sensores_distancia:
                coord_x_rotacionada, coord_y_rotacionada = self.rotaciona(sensor.coord_x_relativa, sensor.coord_y_relativa, self.angulo)
                coord_x_absoluta = self.coord_x + coord_x_rotacionada
                coord_y_absoluta = self.coord_y + coord_y_rotacionada
                sensor.determina_distancia_obstaculo(coord_x_absoluta, coord_y_absoluta, self.angulo + sensor.angulo_relativo, obstaculo)

    def verifica_colisao(self, lista_obstaculos, coord_x_prevista, coord_y_prevista):
        restringe_x = False
        restringe_y = False

        for obstaculo in lista_obstaculos:
            x1 = obstaculo[0]
            y1 = obstaculo[1]
            x2 = obstaculo[2]
            y2 = obstaculo[3]
            limite_direito = coord_x_prevista + self.raio
            limite_esquerdo = coord_x_prevista - self.raio
            limite_superior = coord_y_prevista - self.raio
            limite_inferior = coord_y_prevista + self.raio
            if ((limite_direito > x1) and (limite_direito < x2)) or ((limite_esquerdo > x1) and (limite_esquerdo < x2)):
                if (limite_inferior < y1) and (limite_inferior > y2) or (limite_superior < y1) and (limite_superior > y2):
                    restringe_x = True
                    restringe_y = True

        if restringe_x:
            coord_x_final = self.coord_x
        else:
            coord_x_final = coord_x_prevista

        if restringe_y:
            coord_y_final = self.coord_y
        else:
            coord_y_final = coord_y_prevista

        return coord_x_final, coord_y_final

    def dinamica_robo(self, lista_obstaculos):
        """
            Atualiza a posicao e angulo do robo com base no algoritmo de controle.
        """
        self.atualiza_sensores(lista_obstaculos)

        self.controle()

        velocidade = (self.vel_motor_direita + self.vel_motor_esquerda) / 2

        self.angulo = self.angulo + (self.vel_motor_direita - self.vel_motor_esquerda) * math.pi / 24

        if self.angulo > math.pi:
            self.angulo -= 2 * math.pi            
        if self.angulo < -math.pi:
            self.angulo += 2 * math.pi            

        coord_x_prevista = self.coord_x + velocidade * math.cos(self.angulo)
        coord_y_prevista = self.coord_y + velocidade * math.sin(self.angulo)
            
        self.coord_x, self.coord_y = self.verifica_colisao(lista_obstaculos, coord_x_prevista, coord_y_prevista)

        self.determina_direcao()

        # self.mostra_direcao()
        dist_frente = self.sensores_distancia[0].distancia
        dist_esquerda = self.sensores_distancia[1].distancia
        dist_direita = self.sensores_distancia[2].distancia
        if (self.estado == self.Estados.ANDA) or (self.estado == self.Estados.ANDA1):
            self.mapa.atualiza(self.coord_x, self.coord_y, dist_frente, dist_esquerda, dist_direita, self.direcao)

        if self.estado == self.Estados.PARA:
            self.avanca_sequencia_de_comandos()
            self.algoritmo_de_movimentacao.loop(self)

    def avanca_sequencia_de_comandos(self):
        #self.mostra_estado()
        if len(self.lista_de_comandos) > 0:
            self.estado = self.lista_de_comandos[0]
            del self.lista_de_comandos[0]
            if self.estado == self.Estados.ANDA1:
                if (self.direcao == Direcoes.LESTE) or (self.direcao == Direcoes.OESTE):
                    self.contagem = int(self.mapa.fator_escala_x / self.Params.VELOCIDADE_MAXIMA_MOTOR) + 1
                if (self.direcao == Direcoes.NORTE) or (self.direcao == Direcoes.SUL):
                    self.contagem = int(self.mapa.fator_escala_y / self.Params.VELOCIDADE_MAXIMA_MOTOR) + 1
            if self.estado == self.Estados.GIRA_DIREITA:
                if self.ideal:
                    self.contagem = 9
                else:
                    self.contagem = 8 + random.randint(0, 2)
            if self.estado == self.Estados.GIRA_ESQUERDA:
                if self.ideal:
                    self.contagem = 9
                else:
                    self.contagem = 8 + random.randint(0, 2)
        #self.mostra_estado()

    def aberto_direita(self):
        if self.direcao == Direcoes.OESTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_norte:
                return True
            else:
                return False
        if self.direcao == Direcoes.LESTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_sul:
                return True
            else:
                return False
        if self.direcao == Direcoes.NORTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_leste:
                return True
            else:
                return False
        if self.direcao == Direcoes.SUL:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_oeste:
                return True
            else:
                return False

    def aberto_esquerda(self):
        if self.direcao == Direcoes.OESTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_sul:
                return True
            else:
                return False
        if self.direcao == Direcoes.LESTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_norte:
                return True
            else:
                return False
        if self.direcao == Direcoes.NORTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_oeste:
                return True
            else:
                return False
        if self.direcao == Direcoes.SUL:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_leste:
                return True
            else:
                return False

    def aberto_adiante(self):
        if self.direcao == Direcoes.OESTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_oeste:
                return True
            else:
                return False
        if self.direcao == Direcoes.LESTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_leste:
                return True
            else:
                return False
        if self.direcao == Direcoes.NORTE:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_norte:
                return True
            else:
                return False
        if self.direcao == Direcoes.SUL:
            celula_atual = self.mapa.celula_atual()
            if celula_atual.aberto_sul:
                return True
            else:
                return False

    def controle(self):
        """
            Algoritmo de controle dos motores do robo.

            O robo eh controlado por:
                self.vel_motor_direita
                self.vel_motor_esquerda

            Os sensores são lidos na configuracao atual do robo em:
                self.sensores_distancia[0].distancia # frontal;
                self.sensores_distancia[1].distancia # esquerdo;
                self.sensores_distancia[2].distancia # direito;

            O estado atual do robo pode ser lido em:
                self.estado
            e pode ser:
                self.Estados.ANDA - anda ate encontrar uma parede;
                self.Estados.ANDA1 - anda uma celula a frente e para;
                self.Estados.GIRA_DIREITA - gira para a direita;
                self.Estados.GIRA_ESQUERDA - gira para a esquerda;

            O tempo em cada etapa eh controlado por
                self.contagem

        """
        dist_frontal = self.sensores_distancia[0].distancia
        dist_esquerda = self.sensores_distancia[1].distancia
        dist_direita = self.sensores_distancia[2].distancia

        #self.mostra_estado()
        if (self.estado == self.Estados.ANDA) or (self.estado == self.Estados.ANDA1):
            if dist_frontal > self.Params.DISTANCIA_MINIMA_PARADA:
                if self.ideal:
                    self.vel_motor_direita = self.Params.VELOCIDADE_MAXIMA_MOTOR
                    self.vel_motor_esquerda = self.Params.VELOCIDADE_MAXIMA_MOTOR
                else:
                    self.vel_motor_direita = self.Params.VELOCIDADE_MAXIMA_MOTOR + self.Params.VARIACAO_MOTORES * random.random()
                    self.vel_motor_esquerda = self.Params.VELOCIDADE_MAXIMA_MOTOR + self.Params.VARIACAO_MOTORES * random.random()
            if not self.ideal:
                if dist_direita + dist_esquerda < self.Params.LARGURA_CORREDOR:
                    if dist_direita > dist_esquerda:
                        self.vel_motor_direita = self.Params.VELOCIDADE_MAXIMA_MOTOR * self.Params.REDUCAO_MOTOR_CORREDOR
                    if dist_esquerda > dist_direita:
                        self.vel_motor_esquerda = self.Params.VELOCIDADE_MAXIMA_MOTOR * self.Params.REDUCAO_MOTOR_CORREDOR
                else:
                    if dist_direita > dist_esquerda:
                        if dist_esquerda > self.dist_esquerda_anterior:
                            self.vel_motor_esquerda = self.Params.VELOCIDADE_MAXIMA_MOTOR * self.Params.REDUCAO_MOTOR_CAMPO_ABERTO
                            self.vel_motor_direita = self.Params.VELOCIDADE_MAXIMA_MOTOR
                        else:
                            self.vel_motor_direita = self.Params.VELOCIDADE_MAXIMA_MOTOR * self.Params.REDUCAO_MOTOR_CAMPO_ABERTO
                            self.vel_motor_esquerda = self.Params.VELOCIDADE_MAXIMA_MOTOR
                    if dist_esquerda > dist_direita:
                        if dist_direita > self.dist_direita_anterior:
                            self.vel_motor_direita = self.Params.VELOCIDADE_MAXIMA_MOTOR * self.Params.REDUCAO_MOTOR_CAMPO_ABERTO
                            self.vel_motor_esquerda = self.Params.VELOCIDADE_MAXIMA_MOTOR
                        else:
                            self.vel_motor_esquerda = self.Params.VELOCIDADE_MAXIMA_MOTOR * self.Params.REDUCAO_MOTOR_CAMPO_ABERTO
                            self.vel_motor_direita = self.Params.VELOCIDADE_MAXIMA_MOTOR
            else:
                if self.direcao == Direcoes.LESTE:
                    self.angulo = 0
                elif self.direcao == Direcoes.OESTE:
                    self.angulo = math.pi
                elif self.direcao == Direcoes.NORTE:
                    self.angulo = math.pi / 2
                elif self.direcao == Direcoes.LESTE:
                    self.angulo = -math.pi / 2

            if dist_frontal < self.Params.DISTANCIA_MINIMA_PARADA:
                self.vel_motor_direita = 0
                self.vel_motor_esquerda = 0
                self.estado = self.Estados.PARA

            if self.estado == self.Estados.ANDA1:
                self.contagem -= 1
                if self.contagem == 0:
                    self.estado = self.Estados.PARA

        if self.estado == self.Estados.PARA:
            self.vel_motor_direita = 0
            self.vel_motor_esquerda = 0

        if self.estado == self.Estados.GIRA_DIREITA:
            self.vel_motor_direita = -self.Params.VELOCIDADE_MAXIMA_MOTOR / 3
            self.vel_motor_esquerda = self.Params.VELOCIDADE_MAXIMA_MOTOR / 3
            self.contagem = self.contagem - 1
            if self.contagem == 0:
                self.estado = self.Estados.PARA

        if self.estado == self.Estados.GIRA_ESQUERDA:
            self.vel_motor_direita = self.Params.VELOCIDADE_MAXIMA_MOTOR / 3
            self.vel_motor_esquerda = -self.Params.VELOCIDADE_MAXIMA_MOTOR / 3
            self.contagem = self.contagem - 1
            if self.contagem == 0:
                self.estado = self.Estados.PARA

        #self.mostra_estado()

        self.dist_esquerda_anterior = self.dist_esquerda_anterior * 0.7 + dist_esquerda * 0.3
        self.dist_direita_anterior = self.dist_direita_anterior * 0.7 + dist_direita * 0.3
