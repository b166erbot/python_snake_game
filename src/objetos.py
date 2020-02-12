from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, color_pair
from operator import eq
from time import sleep
from typing import NoReturn, Tuple, Iterable, Optional
from types import FunctionType
from random import randint

from .cores import cor


class Objeto:
    def __init__(self, x: int, y: int, tela, character: str) -> NoReturn:
        self._x, self._y = x, y
        self._tela = tela
        self._character = character
        self.posicao_anterior = (x, y)


class Tangivel(Objeto):
    def __init__(
        self, *args, cor: Optional[str] = 'white', **kwargs
    ) -> NoReturn:
        super().__init__(*args, **kwargs)
        self._vida = 1
        self._cor = cor

    def colisao(self, other) -> bool:
        """Método que verifica se dois objetos colediram."""
        self_itens, other_itens = [self._x, self._y], [other._x, other._y]
        return True if all(map(eq, self_itens, other_itens)) else False

    def exibir(self) -> NoReturn:
        """Método que exibe o caracter desta classe no terminal."""
        self._tela.addstr(self._x, self._y, self._character, cor(self._cor))

    def efeito(self, *args, **kwargs) -> NoReturn:
        """Método que genérico que aplica efeitos em outros objetos."""
        mensagem = 'É necessário herdar esta classe e sobrepor este método.'
        raise NotImplementedError(mensagem)

    def definir_posicao(self, tupla: Tuple[int]) -> NoReturn:
        self.posicao_anterior = (self._x, self._y)
        self._x, self._y = tupla


class Aneis(Tangivel):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, cor = 'green', **kwargs)

    def definir_posicao(self, anel) -> NoReturn:
        """Método que altera a posição atual deste objeto."""
        if isinstance(anel, tuple):
            nova_posicao = anel
        else:
            nova_posicao = anel.posicao_anterior
        self.posicao_anterior = (self._x, self._y)
        self._x, self._y = nova_posicao

    def efeito(self, python, cabeca) -> NoReturn:
        """Método que mata a cobra caso haja colisão."""
        python._vida = 0
        # python.alterar_character('☠')


class Python(Tangivel):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self._direcoes = {
            KEY_LEFT: lambda: (self._x, self._y - self._salto),
            KEY_RIGHT: lambda: (self._x, self._y + self._salto),
            KEY_UP: lambda: (self._x - self._salto, self._y),
            KEY_DOWN: lambda: (self._x + self._salto, self._y)
        }
        self._direcoes_opostas = {
            KEY_RIGHT: KEY_LEFT, KEY_LEFT: KEY_RIGHT, KEY_UP: KEY_DOWN,
            KEY_DOWN: KEY_UP
        }
        self.corpo = [Aneis(self._x, self._y, self._tela, self._character)]
        self._direcao = KEY_RIGHT
        self._salto = 1

    def atualizar(self, x: int, y: int) -> NoReturn:
        """Método que atualiza os aneis da cobra na tela."""
        aneis = zip([(x, y)] + self.corpo, self.corpo)
        for x, y in aneis:
            y.definir_posicao(x)

    def andar(self, nova_direcao: int) -> NoReturn:
        """Método que faz a cobra se locomover."""
        if self._direcao_oposta(nova_direcao):
            self._direcao = nova_direcao or self._direcao
        funcao = self._direcoes[self._direcao]
        self.posicao_anterior = (self._x, self._y)
        self._x, self._y = funcao()
        self.atualizar(self._x, self._y)

    def alterar_character(self, character: str) -> NoReturn:
        """Método que altera o caracter da cabeça da cobra."""
        self.corpo[0]._character = character

    def _direcao_oposta(self, direcao: str) -> bool:
        """Método que verifica se a direção é a oposta da atual."""
        return self._direcoes_opostas[self._direcao] != direcao

    def adicionar_anel(self) -> NoReturn:
        """Método que adiciona uma parte a mais na cobra."""
        if self.corpo:
            posicao = self.corpo[-1].posicao_anterior
        else:
            posicao = self.posicao_anterior
        self.corpo.append(Aneis(*posicao, self._tela, '◯'))  # ⓞ∗⏣


class Barreira(Tangivel):
    def __iter__(self) -> Iterable:
        return iter([self])

    def efeito(self, python: Python, cabeca: Aneis) -> NoReturn:
        """Método que mata a cobra caso haja colisão."""
        python._vida = 0
        # python.alterar_character('☠')


class Portal(Tangivel):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, '⏣', cor = 'blue', **kwargs)
        self._interligado = False
        self.saida = []

    def conectar_portais(self, portal) -> NoReturn:
        self._interligado = portal._interligado = True
        portal.saida += [self._x, self._y]
        self.saida += [portal._x, portal._y]

    def efeito(self, python: Python, cabeca: Aneis) -> NoReturn:
        if self._interligado:
            python.definir_posicao(self.saida)

class Grama(Tangivel):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, '≈', cor = 'green', **kwargs)

    def efeito(self, python: Python, cabeca: Aneis) -> NoReturn:
        ...


class Retornavel(Tangivel):
    def __init__(self, *args, nova_posicao: FunctionType, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self._nova_posicao = nova_posicao

    def exibir(self) -> NoReturn:
        self._tela.addstr(self._x, self._y, self._character, cor(self._cor))


class Comida(Retornavel):
    def efeito(self, python: Python, cabeca: Aneis) -> NoReturn:
        """Método que adiciona um anel a cobra."""
        python.adicionar_anel()
        self._x, self._y = self._nova_posicao()


class RetornavelComTempo(Tangivel):
    def __init__(self, *args, nova_posicao: FunctionType, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self._consumivel = iter(range(300)[::-1])
        self.visivel = False
        self._nova_posicao = nova_posicao

    def exibir(self) -> NoReturn:
        caracter = self._character if self.visivel else ' '
        self._tela.addstr(self._x, self._y, caracter, cor(self._cor))
        if next(self._consumivel) == 0:
            self._consumivel = iter(range(randint(120, 150))[::-1])
            self.visivel = True


class BonusRemoverAneis(RetornavelComTempo):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, '⚡', cor = 'yellow', **kwargs)

    def efeito(self, python: Python, cabeca: Aneis) -> NoReturn:
        if all([len(python.corpo) >= 5, self.visivel]):
            python.corpo = python.corpo[:-3]
            self._x, self._y = self._nova_posicao()
            self.visivel = False


# com objetos retornaveis agora não precisa mais de vida no tangíveis?
