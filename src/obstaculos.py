from itertools import chain, cycle
from random import choice
from typing import Any, Iterator, List, Tuple, NoReturn

from .objetos import Barreira, Grama


class Quadrados:
    def __init__(self, caracteres: str, tela,
                 x: int, y: int, x2: int = 0, y2: int = 0) -> NoReturn:
        self._tela = tela
        self._caracteres = caracteres
        self._posicoes = [x, y, x2, y2]

    def _construir(self, a: int, b: int, a2: int, b2: int) -> Iterator[Barreira]:
        colunas, linhas = range(a2 + 1, a + a2), range(b2 + 1, b + b2)
        chars = self._caracteres
        # cada map representa uma parte da parede do quadrado.
        # barreira esquerda, inferior, direita e superior, nesta mesma ordem
        barreiras = [
            Barreira(b2, a2, self._tela, chars[2]),
            map(lambda x: Barreira(x, a2, self._tela, chars[0]), linhas),
            Barreira(b + b2, a2, self._tela, chars[4]),
            map(lambda x: Barreira(b + b2, x, self._tela, chars[1]), colunas),
            Barreira(b + b2, a + a2, self._tela, chars[5]),
            map(lambda y: Barreira(y, a + a2, self._tela, chars[0]), linhas),
            Barreira(b2, a + a2, self._tela, chars[3]),
            map(lambda y: Barreira(b2, y, self._tela, chars[1]), colunas),
        ]
        return chain(*barreiras)

    def quadrado(self) -> List[Barreira]:
        return list(self._construir(*self._posicoes))

    def quadrado_quebrado(self, buracos: int = 1) -> List[Barreira]:
        if buracos not in range(1, 4):
            raise ValueError('o argumento buracos precisa estar entre 1 e 3')
        barreiras = list(enumerate(self._construir(*self._posicoes)))
        tamanho_barreias = len(barreiras)
        tamanho_buraco = tamanho_barreias // 3
        tamanho_permitido = range(abs(tamanho_buraco - tamanho_barreias))
        for _ in range(buracos):
            comeco = choice(tamanho_permitido)
            buraco = range(comeco, comeco + tamanho_buraco)
            barreiras = list(filter(lambda x: x[0] not in buraco, barreiras))
            tamanho_barreias = len(barreiras)
            tamanho_permitido = range(abs(tamanho_buraco - tamanho_barreias))
        return list(map(lambda x: x[1], barreiras))


class Gramado:
    def __init__(
        self, x: int, y: int, inicio_x: int, inicio_y: int, tela
    ) -> NoReturn:
        self._x = x + inicio_x
        self._y = y + inicio_y
        self._inicio_x = inicio_x
        self._inicio_y = inicio_y
        self._tela = tela

    def _indices(self, range_x: range, range_y: range) -> List[Tuple[int]]:
        indices = [(x, y) for x in range_x for y in range_y]
        return indices

    def preenchido(self) -> List[Grama]:
        range_x = range(self._inicio_x, self._x)
        range_y = range(self._inicio_y, self._y)
        indices = self._indices(range_x, range_y)
        return list(map(lambda x: Grama(*x, self._tela), indices))

    def espacado(self) -> List[Grama]:
        range_x = range(self._inicio_x, self._x)
        range_y = range(self._inicio_y, self._y, 2)
        indices = self._indices(range_x, range_y)
        return list(map(lambda x: Grama(*x, self._tela), indices))

    def xadres(self) -> List[Grama]:
        range_x = range(self._inicio_x, self._x)
        range_y = range(self._inicio_y, self._y, 2)
        range_y2 = range(self._inicio_y + 1, self._y - 1, 2)
        ciclo_y = cycle([range_y, range_y2])
        indices = [(x, y) for x in range_x for y in next(ciclo_y)]
        return list(map(lambda x: Grama(*x, self._tela), indices))
