import curses
from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP
from itertools import chain
from os import get_terminal_size as get_size
from random import choice
from time import sleep
from typing import NoReturn

from .objetos import Barreira, Comida, Python


class Jogo:
    def __init__(self, tela, linhas: int, colunas: int) -> NoReturn:
        self._tela = tela
        linhas -= 2
        colunas -= 3
        self._linhas = linhas
        self._colunas = colunas
        self._teclas = [KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN]
        self._cobra = Python(5, 5, tela, '⌬')
        col, lin = range(1, colunas + 1), range(1, linhas + 1)
        # barreira esquerda, inferior, superior, direita. nesta mesma ordem
        itens = [
            map(lambda x: Barreira(x, 0, tela, '│'), lin),
            map(lambda x: Barreira(linhas + 1, x, tela, '─'), col),
            map(lambda y: Barreira(0, y, tela, '─'), col),
            map(lambda y: Barreira(y, colunas + 1, tela, '│'), lin),
            [
                Barreira(0, 0, tela, '┌'), Barreira(0, colunas + 1, tela, '┐'),
                Barreira(linhas + 1, colunas + 1, tela, '┘'),
                Barreira(linhas + 1, 0, tela, '└')
            ]
        ]
        self._itens = list(chain(*itens))
        self.repor_comida()

    def colisoes(self) -> NoReturn:
        """Método verifica colisões, aplica os efeitos nos itens e os remove."""
        self._itens = list(filter(lambda x: x._vida > 0, self._itens))
        cabeca, *corpo = self._cobra._corpo
        for tangivel in chain(self._itens, corpo):
            tangivel.efeito(self._cobra, cabeca)

    def repor_comida(self) -> NoReturn:
        """Método que repõe a comida caso não haja mais."""
        if not any(map(lambda x: isinstance(x, Comida), self._itens)):
            posicoes = map(lambda x: (x._x, x._y), self._cobra._corpo)
            lista_x, lista_y = zip(*posicoes)
            range_x = range(1, self._linhas - 1)
            range_y = range(1, self._colunas)
            lista_x = list(filter(lambda x: x not in lista_x, range_x))
            lista_y = list(filter(lambda y: y not in lista_y, range_y))
            x, y = choice(lista_x), choice(lista_y)
            self._itens.append(Comida(x, y, self._tela, '◉'))

    def rodar(self) -> NoReturn:
        """Método que roda todo o jogo."""
        while self._cobra._vida > 0:
            tecla = self._tela.getch()
            self._cobra.andar(tecla if tecla in self._teclas else False)
            self.colisoes()
            self.repor_comida()
        self._tela.addstr(5, 5, 'Fim.')
        self._tela.refresh()
        sleep(1)


def configurar(tela) -> NoReturn:
    """Função que executa configurações iniciais."""
    tela.keypad(True)
    curses.curs_set(0)  # oculta o pipe
    tela.nodelay(True)
    curses.noecho()


def main():
    """Função principal."""
    curses.initscr()
    colunas, linhas = get_size()
    tela = curses.newwin(linhas, colunas + 1)
    configurar(tela)
    # não altere a ordem do código acima.
    try:
        Jogo(tela, linhas, colunas).rodar()
    finally:
        curses.endwin()  # volta tudo ao normal.


# TODO: comida não deve sobrepor a cobra
# TODO: colocar cor na cobra
# TODO: colocar mapas diferenciados
# TODO: limpar a tela para exibir o fim


# caracteres: ☠▢▣◯◉⚠☢✇☣⚙⚛✧⌬⦗⦘☀☁☃❄❆❅☽☾✗✘✓✔ⓞ☉☄★☆▤▥▦⬚▧▨▩♺⎔⎕⏣⌗⥢⥣⥤⥥⟁◎❖✵◯∗
# ☯ colocar os caracteres katacanas na cobra com isto?
# ☘ dar pontos a mais com este trevo?
# Ω god of war?
