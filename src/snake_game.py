import curses
from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP
from functools import namedtuple
from itertools import chain
from os import get_terminal_size as get_size
from random import choice
from time import sleep
from typing import NoReturn, Tuple

from .objetos import Barreira, Comida, Python, Grama, BonusRemoverAneis
from .obstaculos import Quadrados
from .mapas import Mapas


class Jogo:
    def __init__(self, tela, linhas: int, colunas: int) -> NoReturn:
        self._tela = tela
        linhas -= 1
        colunas -= 2
        self._linhas = linhas
        self._colunas = colunas
        self._dormir = 0.15
        self._teclas = [KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN]
        self._cobra = Python(5, 5, tela, '◯')
        self._itens = Mapas(tela, colunas, linhas).mapa1()
        self._itens.append(BonusRemoverAneis(
            *self.lugar_vazio_aleatorio(), tela,
            nova_posicao = self.lugar_vazio_aleatorio
        ))
        self._itens.append(Comida(
            *self.lugar_vazio_aleatorio(), self._tela, '◉',
            nova_posicao = self.lugar_vazio_aleatorio
        ))

    def _colisoes(self) -> NoReturn:
        # muitas iteracoes, alterar para somente a head verificar a colisao
        """Método verifica colisões, aplica os efeitos nos itens e os remove."""
        self._itens = list(filter(lambda x: x._vida > 0, self._itens))
        cabeca, *corpo = self._cobra.corpo
        itens = filter(lambda x: x.colisao(cabeca), chain(self._itens, corpo))
        for tangivel in itens:
            tangivel.efeito(self._cobra, cabeca)

    def lugar_vazio_aleatorio(self) -> Tuple[int]:
        itens = chain(self._itens, self._cobra.corpo)
        itens = filter(lambda x: not isinstance(x, Grama), itens)
        posicoes = list(map(lambda x: (x._x, x._y), itens))
        range_x = range(1, self._linhas - 1)
        range_y = range(1, self._colunas)
        mapa = [(x, y) for x in range_x for y in range_y]
        posicoes_filtradas = list(filter(lambda x: x not in posicoes, mapa))
        return choice(posicoes_filtradas)

    def _atualizar_tela(self):
        """Método que atualiza os frames na tela."""
        self._tela.erase()
        for tangivel in chain(self._itens, self._cobra.corpo):
            tangivel.exibir()

    def rodar(self) -> NoReturn:
        """Método que roda todo o jogo."""
        while all([self._cobra._vida > 0, list(get_size()) == [80, 24]]):
            tecla = self._tela.getch()
            self._cobra.andar(tecla if tecla in self._teclas else False)
            self._colisoes()
            self._atualizar_tela()
            sleep(self._dormir)
        self._tela.erase()
        self._tela.addstr(0, 0, 'Fim.')
        if list(get_size()) != [80, 24]:
            self._tela.addstr(1, 0, 'redimensione sua tela para 80 x 24.')
        self._tela.refresh()
        sleep(1.5)


def configurar(tela) -> NoReturn:
    """Função que executa configurações iniciais."""
    tela.keypad(True)
    curses.curs_set(0)  # oculta o pipe
    tela.nodelay(True)
    curses.noecho()
    curses.start_color()
    curses.use_default_colors()
    for x in range(10):
        curses.init_pair(x + 1, x, -1)


def main():
    """Função principal."""
    try:
        curses.initscr()
        colunas, linhas = get_size()
        tela = curses.newwin(linhas, colunas + 1)
        configurar(tela)
        Jogo(tela, linhas, colunas).rodar()
    finally:
        curses.endwin()  # volta tudo ao normal.


# TODO: comida com tempo.
# TODO: modo imune com tempo, (quebrar barreiras?).
# TODO: modo fantasma com tempo.
# TODO: criar um gramado estilo xadres.
# TODO: arrumar o bug ao redimensionar janelas e colocar tamanho mínimo para
# o jogo rodar.
# TODO: bonus seta para aumentar a velocidade.


# caracteres: ☠▢▣◯◉⚠☢✇☣⚙⚛✧⌬⦗⦘⚡☀☁☃❄❆❅☽☾✗✘✓✔ⓞ☉☄★☆▤▥▦⬚▧▨▩♺⎔⎕⏣⌗⥢⥣⥤⥥⟁◎❖✵◯∗⌌⌍⌎⌏
# ☯ colocar os caracteres katacanas na cobra com isto?
# ☘ dar pontos a mais com este trevo?
# Ω god of war?
