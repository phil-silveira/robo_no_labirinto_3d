# Robo no Labirinto 3D

Simulador simples utilizado na disciplina de inteligência artificial.

![Screenshot](/robo1.png)

![Screenshot](/robot2.png)

![Screenshot](/robot3.png)

Para executar a versão em 3D:

```bash
python Simulacao_robo_opengl.py
```
Para executar a versão em 2D:

```bash
Simulacao_robo_tkinter.py
```

## Dependências:

É necessário instalar o pacote pyopengl e freeglut3

No linux:
```bash
pip install pyopengl
sudo apt-get install freeglut3-dev
```


## Controles na interface 3D:

Acesse a interface utilizando o botão direito.

__Liga/Desliga__: ativa ou desativa a simulação.\
__Mapa__: muda o labirinto, reiniciando a simulação.\
__Modo__: modo de simulação do controle do robô.\
__Sensores__: mostra a localização da varredura dos sensores.\
__Giro Camera__: ativa/desativa giro em torno do labirinto.\
__Modo Camera__: alterna entre vista externa ou visao do robo.

Clique e arraste com o botão esquerdo sobre a tela para girar a cena.

## Controles na interface 2D:

__Liga/Desliga__: ativa ou desativa a simulação.\
__Mapa__: muda o labirinto, reiniciando a simulação.\
__Ideal/Real__: modo de simulação do controle do robô.\
__Sensores__: mostra a localização da varredura dos sensores.\
__Celulas__: mostra as celulas para as quais o labirinto é abstraido.

## Funções:

O algoritmo de navegação no labirinto ficou concentrado no arquivo simple.py para simplicidade.

__setup()__: Função responsável pelas definições iniciais.\
__loop()__: Função executada a cada passo da simulação, responsável pelo controle.

## Mapa:

O ambiente no qual o robô se desloca é dividido em células.\
Um mapa é montado automaticamente conforme a movimentação do robô, de acordo com os dados dos sensores de distância.\
No código (simple.py) há um exemplo de como acessar o mapa.

## Comandos:

Comandos podem ser adicionados a uma lista para execução pelo robô.\
\
__GIRA_DIREITA__: gira para a direita 90 graus;\
__GIRA_ESQUERDA__: gira para a esquerda 90 graus;\
__ANDA1__: anda 1 celula para a frente;\
__ANDA__: anda ate atingir uma parede;\
__PARA__: permanece na mesma célula.\
\
No código (simple.py) há um exemplo de como utilizar os comandos.
