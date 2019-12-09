# Robo no Labirinto :space_invader:

## Sumários

- [Configuração inicial](#configuração-inicial)
- [Dependências](#dependências)
- [Simulação 2D](#simulação-2d)
- [Simulação 3D](#simulação-3d)
- [Mapa](#mapa)
- [Navegação](#navegação)
- [Comandos](#comandos)

## Configuração inicial

Abrir um terminal no diretório raiz do projeto e executar os seguintes comandos:
```bash
    make setup
    source ./venv/bin/activate
```

## Dependências:

É necessário instalar o pacote pyopengl e a biblioteca freeglut3.

No linux:
```bash
    pip install pyopengl
    sudo apt install freeglut3-dev
```

## Simulação 2D

Para iniciar a simulação, basta abrir um terminal do diretório raiz do projeto e executar o comando `make run-2d-simulation`.

![Screenshot](/img/simulacao-2d.png)

### Controles da interface 2D:

__Liga/Desliga__: ativa ou desativa a simulação.\
__Mapa__: muda o labirinto, reiniciando a simulação.\
__Ideal/Real__: modo de simulação do controle do robô.\
__Sensores__: mostra a localização da varredura dos sensores.\
__Celulas__: mostra as celulas para as quais o labirinto é abstraido.


## Simulação 3D

Para iniciar a simulação, basta abrir um terminal do diretório raiz do projeto e executar o comando `make run-3d-simulation`.

![Screenshot](/img/simulacao-3d.png)

### Controles da interface 3D:

Acesse a interface utilizando o botão direito.

__Liga/Desliga__: ativa ou desativa a simulação.\
__Mapa__: muda o labirinto, reiniciando a simulação.\
__Modo__: modo de simulação do controle do robô.\
__Sensores__: mostra a localização da varredura dos sensores.\
__Giro Camera__: ativa/desativa giro em torno do labirinto.\
__Modo Camera__: alterna entre vista externa ou visao do robo.

Clique e arraste com o botão esquerdo sobre a tela para girar a cena.


## Mapa:

O ambiente no qual o robô se desloca é dividido em células.\
Um mapa é montado automaticamente conforme a movimentação do robô, de acordo com os dados dos sensores de distância.

## Navegação:

O algoritmo de navegação usado pelo robô para se movimentar pelo labirinto esta localizado no arquivo `algoritmo_de_movimentacao.py`.

__setup()__: Função responsável pelas definições iniciais.\
__loop()__: Função executada a cada passo da simulação, responsável pelo controle.

## Comandos:

Comandos podem ser adicionados a uma lista para execução pelo robô.\
\
__GIRA_DIREITA__: gira para a direita 90 graus;\
__GIRA_ESQUERDA__: gira para a esquerda 90 graus;\
__ANDA1__: anda 1 celula para a frente;\
__ANDA__: anda ate atingir uma parede;\
__PARA__: permanece na mesma célula.\
\
No arquivo `algoritmo_de_movimentacao.py` há um exemplo de como utilizar os comandos.
