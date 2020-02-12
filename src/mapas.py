from .obstaculos import Quadrados, Gramado
from .objetos import Barreira, Portal
from random import randint
from typing import List, Tuple, NoReturn
from itertools import combinations


# aqui é o local onde coloco todos os mapas. por enquanto só há um.
class Mapas:
    def __init__(self, tela, colunas: int, linhas: int) -> NoReturn:
        self._tela = tela
        self._col, self._lin = colunas, linhas

    def mapa1(self) -> List[Barreira]:
        """Método que cria o mapa 1."""
        # nenhum dos números abaixo poderiam estar neste escopo a não ser que
        # este mapa seja inalterável/permanente.
        tela = self._tela
        itens = Quadrados('│─┌┐└┘', tela, self._col, self._lin).quadrado()
        itens += Quadrados(
            '║═╔╗╚╝', tela, 5, 5, 15, 15
        ).quadrado_quebrado()  # tratar essa excessão na classe
        itens += Quadrados(
            '║═╔╗╚╝', tela, 10, 8, 45, 2
        ).quadrado_quebrado()
        itens += Quadrados(
            '║═╔╗╚╝', tela, 7, 5, 65, 13
        ).quadrado_quebrado()
        portal1, portal2 = Portal(6, 20, tela), Portal(18, 60, tela)
        portal1.conectar_portais(portal2)
        itens += [portal1, portal2]
        itens += Gramado(4, 20, 16, 35, tela).criar()
        itens += Gramado(5, 10, 4, 27, tela).criar()
        return itens
