from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from Nucleo_simulacao import *


class Gui:
    def __init__(self):
        self.nucleo_simulacao = NucleoSimulacao()
        self.angulo = 180
        self.variacao_angulo = 10 * 0.1
        self.posicao_x_observador = 400 * math.cos(self.angulo * math.pi / 180)
        self.posicao_y_observador = 400 * math.sin(self.angulo * math.pi / 180)
        self.largura_tela = 640
        self.altura_tela = 400
        self.largura_mapa = 100
        self.tela2d_superior = 200
        self.tela2d_inferior = -200
        self.tela2d_esquerda = -200
        self.tela2d_direita = 200
        self.mouse_ligado = False
        self.angulo_inicial = 0
        self.x_mouse = 0
        self.x_mouse_inicial = 0
        self.visao_robo = False
        self.inicializa_interface()
        self.cria_controles()

    def inicializa_interface(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.largura_tela, self.altura_tela)
        glutCreateWindow("Simulator de Robos")

        glClearColor(0., 0., 0., 1.)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)

        # Nao desenha as faces opostas
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        glutDisplayFunc(self.desenha)

        glShadeModel(GL_SMOOTH)

    def cria_controles(self):
        menu = glutCreateMenu(self.executa_comando)
        glutAddMenuEntry("Liga/Desliga", 1)
        glutAddMenuEntry("Mapa", 2)
        glutAddMenuEntry("Modo", 3)
        glutAddMenuEntry("Sensores", 4)
        glutAddMenuEntry("Giro camera", 5)
        glutAddMenuEntry("Modo camera", 6)
        return menu

    def executa_comando(self, comando):
        if comando == 1:
            self.nucleo_simulacao.liga_desliga()
        elif comando == 2:
            self.nucleo_simulacao.troca_mapa()
        elif comando == 3:
            self.nucleo_simulacao.troca_modo()
        elif comando == 4:
            self.nucleo_simulacao.troca_exibicao_sensores()
        elif comando == 5:
            if self.variacao_angulo == 0:
                self.variacao_angulo = 0.1
            else:
                self.variacao_angulo = 0
        elif comando == 6:
            if not self.visao_robo:
                self.visao_robo = True
            else:
                self.visao_robo = False
        return 0

    def responde_mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_ligado = True
                self.angulo_inicial = self.angulo
                self.x_mouse_inicial = x
                self.x_mouse = x
            if state == GLUT_UP:
                self.mouse_ligado = False
        glutPostRedisplay()

    def move_mouse(self, x, y):
        self.x_mouse = x
        glutPostRedisplay()

    def define_iluminacao(self):

        # Iluminacao
        glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 50, 400, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1.0])

        glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0)
        glLightfv(GL_LIGHT1, GL_POSITION, [400, 50, 0, 1])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [1, 1, 1, 1])
        glLightfv(GL_LIGHT1, GL_SPECULAR, [1, 1, 1, 1])

        glEnable(GL_LIGHTING)

        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

    def rotaciona(self, x, y, angulo):
        x_rotacionado = x * math.cos(angulo) - y * math.sin(angulo)
        y_rotacionado = x * math.sin(angulo) + y * math.cos(angulo)
        return x_rotacionado, y_rotacionado

    def desenha_robo(self):
        angulo_robo = self.nucleo_simulacao.robo.angulo * 180 / math.pi
        coord_x_robo = self.nucleo_simulacao.robo.coord_x
        coord_y_robo = -self.nucleo_simulacao.robo.coord_y

        altura = 20
        raio = 10
        num_pontos = 40

        glPushAttrib(GL_CURRENT_BIT)

        pontos = []
        for i in range(int(num_pontos) + 1):
            angulo = 2 * math.pi * i / num_pontos
            x = raio * math.cos(angulo)
            y = raio * math.sin(angulo)
            pontos.append((x, y))

        glColor(1, 0, 0)

        if self.nucleo_simulacao.mostra_sensores:
            for sensor in self.nucleo_simulacao.robo.sensores_distancia:
                x1 = sensor.coord_x_ini_varredura
                y1 = sensor.coord_y_ini_varredura
                x2 = sensor.coord_x_fim_varredura
                y2 = sensor.coord_y_fim_varredura
                glLineWidth(3)
                glBegin(GL_LINES)
                glVertex3f(x1, altura * 0.9, -y1)
                glVertex3f(x2, altura * 0.9, -y2)
                glEnd()

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        glTranslate(coord_x_robo, 0, coord_y_robo)
        glRotatef(angulo_robo, 0, 1, 0)

        # Circulo superior
        glColor(0.8, 0.2, 0.2)
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, 1, 0)
        for (x, y) in reversed(pontos):
            glVertex3f(x, altura, y)
        glEnd()

        # Laterais
        x_anterior = None
        y_anterior = None
        for (x, y) in pontos:
            if x_anterior is not None:
                glBegin(GL_POLYGON)
                x_norm, y_norm = self.rotaciona(x - x_anterior, y - y_anterior, -90)
                glNormal3f(x_norm, 0, y_norm)
                glVertex3f(x_anterior, altura, y_anterior)
                glVertex3f(x, altura, y)
                glVertex3f(x, altura / 2, y)
                glVertex3f(x_anterior, altura / 2, y_anterior)
                glEnd()
            x_anterior = x
            y_anterior = y

        glEnable(GL_BLEND)  # Habilita transparencia
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Sombra
        glColor4f(0.1, 0.2, 0.1, 0.8)
        glBegin(GL_TRIANGLE_FAN)
        for (x, y) in reversed(pontos):
            glVertex3f(x, 0.5, y)
        glEnd()

        glDisable(GL_BLEND)

        # Rodas
        glColor(0.2, 0.2, 0.2)

        # Laterais roda esquerda
        glBegin(GL_TRIANGLE_FAN)
        for (x, y) in reversed(pontos):
            glNormal3f(0, 0, 1)
            glVertex3f(x, altura / 2 + y, - raio - 1)
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        for (x, y) in pontos:
            glNormal3f(0, 0, -1)
            glVertex3f(x, altura / 2 + y, - raio - 2)
        glEnd()

        # Contorno roda esquerda
        x_anterior = None
        y_anterior = None
        for (x, y) in pontos:
            if x_anterior is not None:
                glBegin(GL_POLYGON)
                x_norm, y_norm = self.rotaciona(x - x_anterior, y - y_anterior, -90)
                glNormal3f(x_norm, y_norm, 0)
                glVertex3f(x_anterior, altura / 2 + y_anterior, - raio - 2)
                glVertex3f(x, altura / 2 + y, - raio - 2)
                glVertex3f(x, altura / 2 + y, - raio)
                glVertex3f(x_anterior, altura / 2 + y_anterior, - raio)
                glEnd()
            x_anterior = x
            y_anterior = y

        # Laterais roda direita
        glBegin(GL_TRIANGLE_FAN)
        for (x, y) in reversed(pontos):
            glNormal3f(0, 0, -1)
            glVertex3f(x, altura / 2 + y, raio + 1)
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        for (x, y) in pontos:
            glNormal3f(0, 0, 1)
            glVertex3f(x, altura / 2 + y, raio + 2)
        glEnd()

        # Contorno roda direita
        x_anterior = None
        y_anterior = None
        for (x, y) in pontos:
            if x_anterior is not None:
                glBegin(GL_POLYGON)
                x_norm, y_norm = self.rotaciona(x - x_anterior, y - y_anterior, -90)
                glNormal3f(x_norm, y_norm, 0)
                glVertex3f(x_anterior, altura / 2 + y_anterior, raio)
                glVertex3f(x, altura / 2 + y, raio)
                glVertex3f(x, altura / 2 + y, raio + 2)
                glVertex3f(x_anterior, altura / 2 + y_anterior, raio + 2)
                glEnd()
            x_anterior = x
            y_anterior = y

        glPopMatrix()

        glMatrixMode(GL_PROJECTION)

        glPopAttrib(GL_CURRENT_BIT)

    def desenha_obstaculo(self, obstaculo):
        x1 = obstaculo[0]
        y1 = -obstaculo[1]
        x2 = obstaculo[2]
        y2 = -obstaculo[3]
        altura = 25

        glPushAttrib(GL_CURRENT_BIT)

        glColor3f(0.4, 0.6, 0.4)

        glBegin(GL_POLYGON)
        glNormal3f(0, 0, -1)
        glVertex3f(x1, altura, y1)
        glVertex3f(x2, altura, y1)
        glVertex3f(x2, 0, y1)
        glVertex3f(x1, 0, y1)
        glEnd()

        glBegin(GL_POLYGON)
        glNormal3f(0, 0, 1)
        glVertex3f(x1, 0, y2)
        glVertex3f(x2, 0, y2)
        glVertex3f(x2, altura, y2)
        glVertex3f(x1, altura, y2)
        glEnd()

        glBegin(GL_POLYGON)
        glNormal3f(-1, 0, 0)
        glVertex3f(x1, 0, y1)
        glVertex3f(x1, 0, y2)
        glVertex3f(x1, altura, y2)
        glVertex3f(x1, altura, y1)
        glEnd()

        glBegin(GL_POLYGON)
        glNormal3f(1, 0, 0)
        glVertex3f(x2, altura, y1)
        glVertex3f(x2, altura, y2)
        glVertex3f(x2, 0, y2)
        glVertex3f(x2, 0, y1)
        glEnd()

        glBegin(GL_POLYGON)
        glNormal3f(0, 1, 0)
        glVertex3f(x1, altura, y2)
        glVertex3f(x2, altura, y2)
        glVertex3f(x2, altura, y1)
        glVertex3f(x1, altura, y1)
        glEnd()

        glPopAttrib(GL_CURRENT_BIT)

    def desenha_obstaculos(self):
        for obstaculo in self.nucleo_simulacao.obstaculos:
            self.desenha_obstaculo(obstaculo)

    def desenha_piso(self):
        tamanho_celula = 50
        glPushAttrib(GL_CURRENT_BIT)

        glColor3f(0.8, 0.8, 0.6)
        for x in range(-self.nucleo_simulacao.largura_labirinto, 2 * self.nucleo_simulacao.largura_labirinto, tamanho_celula):
            for y in range(-self.nucleo_simulacao.altura_labirinto, 2 * self.nucleo_simulacao.altura_labirinto,
                           tamanho_celula):
                glBegin(GL_POLYGON)
                glNormal3f(0, 1, 0)
                glVertex3f(x + 1, 0, y + tamanho_celula - 1)
                glVertex3f(x + tamanho_celula - 1, 0, y + tamanho_celula - 1)
                glVertex3f(x + tamanho_celula - 1, 0, y + 1)
                glVertex3f(x + 1, 0, y + 1)
                glEnd()

        glPopAttrib(GL_CURRENT_BIT)

    def desenha_mapa(self):
        glPushAttrib(GL_CURRENT_BIT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        glLoadIdentity()

        glOrtho(self.tela2d_esquerda, self.tela2d_direita, self.tela2d_inferior, self.tela2d_superior, 1, 1000)

        glNormal3f(0, 0, -1)

        glDisable(GL_LIGHTING)

        glDisable(GL_CULL_FACE)

        glEnable(GL_BLEND)  # Habilita transparencia
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        tamanho_celula = self.largura_mapa / (self.nucleo_simulacao.robo.mapa.largura_em_celulas - 1)
        for LY in range(0, self.nucleo_simulacao.robo.mapa.altura_em_celulas - 1):
            for LX in range(0, self.nucleo_simulacao.robo.mapa.largura_em_celulas - 1):
                coordenada_esquerda = self.tela2d_direita - self.largura_mapa + LX * tamanho_celula
                coordenada_direita = self.tela2d_direita - self.largura_mapa + (LX + 1) * tamanho_celula
                coordenada_superior = self.tela2d_superior / 2 - LY * tamanho_celula
                coordenada_inferior = self.tela2d_superior / 2 - (LY + 1) * tamanho_celula

                if not self.nucleo_simulacao.robo.mapa.celulas[LY][LX].aberto_leste:
                    coordenada_direita -= 1
                if not self.nucleo_simulacao.robo.mapa.celulas[LY][LX].aberto_oeste:
                    coordenada_esquerda += 1

                if not self.nucleo_simulacao.robo.mapa.celulas[LY][LX].aberto_norte:
                    coordenada_superior -= 1
                if not self.nucleo_simulacao.robo.mapa.celulas[LY][LX].aberto_sul:
                    coordenada_inferior += 1

                if (self.nucleo_simulacao.robo.mapa.indice_x_robo == LX) and (
                        self.nucleo_simulacao.robo.mapa.indice_y_robo == LY):
                    glColor4f(1, 0, 0, 0.5)
                else:
                    if self.nucleo_simulacao.robo.mapa.celulas[LY][LX].desconhecido:
                        glColor4f(0.5, 0.5, 0.5, 0.5)
                    else:
                        glColor4f(1, 1, 1, 0.5)
                glBegin(GL_POLYGON)
                glVertex3f(coordenada_esquerda, coordenada_inferior, 10)
                glVertex3f(coordenada_esquerda, coordenada_superior, 10)
                glVertex3f(coordenada_direita, coordenada_superior, 10)
                glVertex3f(coordenada_direita, coordenada_inferior, 10)
                glEnd()

        glEnable(GL_CULL_FACE)

        glEnable(GL_LIGHTING)

        glPopAttrib(GL_CURRENT_BIT)

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

    def desenha(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()  # Inicializa a matriz

        x, y, self.largura_tela, self.altura_tela = glGetIntegerv(GL_VIEWPORT)
        gluPerspective(60, self.largura_tela / self.altura_tela, 0.1, 1500)

        # Observador, alvo, orientacao da camera
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if not self.visao_robo:
            gluLookAt(200 + self.posicao_x_observador, 220, 200 + self.posicao_y_observador,
                      200, 0, 200,
                      0.0, 1.0, 0.0)

        else:
            sensor = self.nucleo_simulacao.robo.sensores_distancia[0]
            xt = sensor.coord_x_fim_varredura
            yt = sensor.coord_y_fim_varredura
            gluLookAt(self.posicao_x_observador, 30, self.posicao_y_observador,
                      xt, 30, -yt,
                      0.0, 1.0, 0.0)

        self.define_iluminacao()

        self.desenha_piso()

        self.desenha_obstaculos()

        self.desenha_robo()

        glFlush()

        self.desenha_mapa()

        glutPostRedisplay()
        glutSwapBuffers()

    def executa(self, dt):
        self.angulo += self.variacao_angulo
        if not self.mouse_ligado:
            if self.angulo >= 360:
                self.angulo -= 360
        else:
            self.angulo = self.angulo_inicial + (self.x_mouse - self.x_mouse_inicial) / 2
        if not self.visao_robo:
            self.posicao_x_observador = 400 * math.cos(self.angulo * math.pi / 180)
            self.posicao_y_observador = 400 * math.sin(self.angulo * math.pi / 180)
        else:
            self.posicao_x_observador = self.nucleo_simulacao.robo.coord_x
            self.posicao_y_observador = -self.nucleo_simulacao.robo.coord_y

        self.nucleo_simulacao.executa()

        glutTimerFunc(50, self.executa, 5)


def main():
    gui = Gui()
    glutAttachMenu(GLUT_RIGHT_BUTTON)
    glutMouseFunc(gui.responde_mouse)
    glutMotionFunc(gui.move_mouse)
    gui.executa(0)
    glutMainLoop()


if __name__ == '__main__':
    main()
