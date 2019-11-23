from tkinter import *

from nucleo_simulacao import *


class Gui:
    def __init__(self, janela_raiz):
        self.nucleo_simulacao = NucleoSimulacao()

        janela_raiz.title('Simulator de Robos')
        self.canvas = Canvas(janela_raiz, width=self.nucleo_simulacao.largura_labirinto + self.nucleo_simulacao.largura_mapa, height=self.nucleo_simulacao.altura_labirinto)
        self.canvas.pack()
        self.frame = Frame(janela_raiz)
        self.frame.pack()
        self.janela_raiz = janela_raiz

        self.botao_liga_desliga = Button(self.frame, text='Liga', background='blue', command=self.liga_desliga)
        self.botao_liga_desliga.pack(side=LEFT)
        self.botao_tipo_mapa = Button(self.frame, text='Mapa 0', background='blue', command=self.troca_mapa)
        self.botao_tipo_mapa.pack(side=LEFT)
        self.botao_modo = Button(self.frame, text='Ideal', background='blue', command=self.troca_modo)
        self.botao_modo.pack(side=LEFT)
        self.botao_sensores = Button(self.frame, text='Sensores', background='blue', command=self.nucleo_simulacao.troca_exibicao_sensores)
        self.botao_sensores.pack(side=LEFT)
        self.botao_grid = Button(self.frame, text='Celulas', background='blue', command=self.nucleo_simulacao.troca_exibicao_grid)
        self.botao_grid.pack(side=LEFT)

        self.desenha_piso()
        self.desenha_obstaculos()
        self.nucleo_simulacao.monta_simulacao()
        self.desenha()

    def liga_desliga(self):
        self.nucleo_simulacao.liga_desliga()
        if self.nucleo_simulacao.ligado:
            self.botao_liga_desliga["text"] = "Desliga"
            self.janela_raiz.after(self.nucleo_simulacao.intervalo_de_simulacao, self.executa)
        else:
            self.botao_liga_desliga["text"] = "Liga"

    def troca_modo(self):
        self.nucleo_simulacao.troca_modo()
        if not self.nucleo_simulacao.robo.ideal:
            self.botao_modo["text"] = "Real"
        else:
            self.botao_modo["text"] = "Ideal"

    def troca_mapa(self):
        self.nucleo_simulacao.troca_mapa()
        if self.nucleo_simulacao.tipo_mapa == 0:
            self.botao_tipo_mapa["text"] = "Mapa 0"
        elif self.nucleo_simulacao.tipo_mapa == 1:
            self.botao_tipo_mapa["text"] = "Mapa 1"
        elif self.nucleo_simulacao.tipo_mapa == 2:
            self.botao_tipo_mapa["text"] = "Mapa 2"
        elif self.nucleo_simulacao.tipo_mapa == 3:
            self.botao_tipo_mapa["text"] = "Mapa 3"
        elif self.nucleo_simulacao.tipo_mapa == 4:
            self.botao_tipo_mapa["text"] = "Mapa 4"
        self.botao_modo["text"] = "Ideal"
        self.canvas.delete("all")
        self.desenha_piso()
        self.desenha_obstaculos()

    def desenha_robo(self):
        """
            Desenha um robo na janela principal.
            Y cresce para baixo na tela
        """
        coord_x = self.nucleo_simulacao.robo.coord_x
        coord_y = self.nucleo_simulacao.robo.coord_y
        angulo = self.nucleo_simulacao.robo.angulo
        raio = self.nucleo_simulacao.robo.raio

        for reta in self.nucleo_simulacao.robo.retas:
            x1, y1 = self.nucleo_simulacao.robo.rotaciona(reta[0], reta[1], angulo)
            x2, y2 = self.nucleo_simulacao.robo.rotaciona(reta[2], reta[3], angulo)
            if reta[4] is None:
                reta[4] = self.canvas.create_line(coord_x + x1, -coord_y - y1, coord_x + x2, -coord_y - y2)
            else:
                self.canvas.coords(reta[4], coord_x + x1, -coord_y - y1, coord_x + x2, -coord_y - y2)

        if self.nucleo_simulacao.mostra_sensores:
            for sensor in self.nucleo_simulacao.robo.sensores_distancia:
                x1 = sensor.coord_x_ini_varredura
                y1 = sensor.coord_y_ini_varredura
                x2 = sensor.coord_x_fim_varredura
                y2 = sensor.coord_y_fim_varredura
                if sensor.referencia_figura is None:
                    sensor.referencia_figura = self.canvas.create_line(x1, -y1, x2, -y2)
                else:
                    self.canvas.coords(sensor.referencia_figura, x1, -y1, x2, -y2)
        else:
            for sensor in self.nucleo_simulacao.robo.sensores_distancia:
                if sensor.referencia_figura is not None:
                    self.canvas.delete(sensor.referencia_figura)
                    sensor.referencia_figura = None

        # Corpo do robo
        x1 = coord_x - raio
        y1 = -coord_y + raio
        x2 = coord_x + raio
        y2 = -coord_y - raio
        if self.nucleo_simulacao.robo.referencia_figura is None:
            self.nucleo_simulacao.robo.referencia_figura = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
        else:
            self.canvas.coords(self.nucleo_simulacao.robo.referencia_figura, x1, y1, x2, y2)

    def desenha_piso(self):
        self.canvas.create_rectangle(0, 0, self.nucleo_simulacao.largura_labirinto, self.nucleo_simulacao.altura_labirinto, fill='white')
        self.canvas.create_rectangle(self.nucleo_simulacao.largura_labirinto, 0, self.nucleo_simulacao.largura_labirinto + self.nucleo_simulacao.largura_mapa, self.nucleo_simulacao.altura_labirinto, fill='black')

    def desenha_obstaculos(self):
        for obstaculo in self.nucleo_simulacao.obstaculos:
            self.canvas.create_rectangle(obstaculo[0], -obstaculo[1], obstaculo[2], -obstaculo[3], fill='gray')

    def desenha_mapa(self):
        tamanho_celula = self.nucleo_simulacao.largura_mapa / (self.nucleo_simulacao.robo.mapa.largura_em_celulas - 1)
        for LY in range(0, self.nucleo_simulacao.robo.mapa.altura_em_celulas - 1):
            for LX in range(0, self.nucleo_simulacao.robo.mapa.largura_em_celulas - 1):
                coordenada_esquerda = self.nucleo_simulacao.largura_labirinto + LX * tamanho_celula
                coordenada_direita = self.nucleo_simulacao.largura_labirinto + (LX + 1) * tamanho_celula - 1
                coordenada_superior = LY * tamanho_celula
                coordenada_inferior = (LY + 1) * tamanho_celula - 1
                if not self.nucleo_simulacao.robo.mapa.celulas[LY][LX].aberto_leste:
                    coordenada_direita -= 1
                if not self.nucleo_simulacao.robo.mapa.celulas[LY][LX].aberto_oeste:
                    coordenada_esquerda += 1
                if not self.nucleo_simulacao.robo.mapa.celulas[LY][LX].aberto_norte:
                    coordenada_superior += 1
                if not self.nucleo_simulacao.robo.mapa.celulas[LY][LX].aberto_sul:
                    coordenada_inferior -= 1
                if (self.nucleo_simulacao.robo.mapa.indice_x_robo == LX) and (self.nucleo_simulacao.robo.mapa.indice_y_robo == LY):
                    preenchimento = 'red'
                else:
                    if self.nucleo_simulacao.robo.mapa.celulas[LY][LX].desconhecido:
                        preenchimento = 'gray'
                    else:
                        preenchimento = 'white'
                if self.nucleo_simulacao.robo.mapa.celulas[LY][LX].referencia_figura is None:
                    self.nucleo_simulacao.robo.mapa.celulas[LY][LX].referencia_figura = self.canvas.create_rectangle(coordenada_esquerda , coordenada_superior , coordenada_direita , coordenada_inferior , outline = preenchimento , fill = preenchimento)
                else:
                    self.canvas.coords(self.nucleo_simulacao.robo.mapa.celulas[LY][LX].referencia_figura, coordenada_esquerda, coordenada_superior, coordenada_direita, coordenada_inferior)
                    self.canvas.itemconfig(self.nucleo_simulacao.robo.mapa.celulas[LY][LX].referencia_figura, outline=preenchimento, fill=preenchimento)

    def desenha_celulas(self):
        if self.nucleo_simulacao.mostra_celulas:
            for LY in range(0, self.nucleo_simulacao.robo.mapa.altura_em_celulas * self.nucleo_simulacao.robo.mapa.MARCADORES_POR_CELULA):
                for LX in range(0, self.nucleo_simulacao.robo.mapa.largura_em_celulas * self.nucleo_simulacao.robo.mapa.MARCADORES_POR_CELULA):
                    marcador = self.nucleo_simulacao.robo.mapa.marcadores[LY][LX]
                    coordenada_esquerda = marcador.coord_x - 1
                    coordenada_direita = marcador.coord_x + 1
                    coordenada_superior = marcador.coord_y - 1
                    coordenada_inferior = marcador.coord_y + 1
                    if not marcador.dentro:
                        if (coordenada_direita < self.nucleo_simulacao.largura_labirinto) and (coordenada_inferior < self.nucleo_simulacao.altura_labirinto):
                            preenchimento = 'green'
                            if marcador.referencia_figura is None:
                                marcador.referencia_figura = self.canvas.create_rectangle(coordenada_esquerda, coordenada_superior, coordenada_direita, coordenada_inferior,outline=preenchimento, fill=preenchimento)
                            else:
                                self.canvas.coords(marcador.referencia_figura, coordenada_esquerda, coordenada_superior, coordenada_direita,coordenada_inferior)
        else:
            for LY in range(0, self.nucleo_simulacao.robo.mapa.altura_em_celulas * self.nucleo_simulacao.robo.mapa.MARCADORES_POR_CELULA):
                for LX in range(0, self.nucleo_simulacao.robo.mapa.largura_em_celulas * self.nucleo_simulacao.robo.mapa.MARCADORES_POR_CELULA):
                    marcador = self.nucleo_simulacao.robo.mapa.marcadores[LY][LX]
                    if marcador.referencia_figura is not None:
                        self.canvas.delete(marcador.referencia_figura)
                        marcador.referencia_figura = None

    def desenha(self):
        self.desenha_robo()
        self.desenha_mapa()
        self.desenha_celulas()

        # Atualiza tela
        self.canvas.update()
        self.janela_raiz.after(self.nucleo_simulacao.intervalo_de_simulacao, self.executa)

    def executa(self):
        """
            Laco principal da simulacao.
        """
        if not self.nucleo_simulacao.ligado:
            return()

        # Simulacao do movimento do robo
        self.nucleo_simulacao.robo.dinamica_robo(self.nucleo_simulacao.obstaculos)
        self.desenha()


def main():
    raiz = Tk()
    Gui(raiz)
    raiz.mainloop()


if __name__ == '__main__':
    main() 
