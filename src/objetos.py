from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP
from operator import eq
from time import sleep
from typing import NoReturn


class Objeto:
    def __init__(self, x: int, y: int, tela, character: str) -> NoReturn:
        self._x, self._y = x, y
        self._tela = tela
        self._character = character
        self._posicao_anterior = (x, y)


class Tangiveis(Objeto):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self._vida = 1
        self.exibir()
        self._tela.refresh()

    def colisao(self, other) -> bool:
        """Método que verifica se dois objetos colediram."""
        self_itens, other_itens = [self._x, self._y], [other._x, other._y]
        return True if all(map(eq, self_itens, other_itens)) else False

    def exibir(self) -> NoReturn:
        """Método que exibe o caracter desta classe no terminal."""
        self._tela.addch(self._x, self._y, self._character)

    def efeito(self, *args, **kwargs) -> NoReturn:
        """Método que genérico que aplica efeitos em outros objetos."""
        mensagem = 'É necessário herdar esta classe e sobrepor este método.'
        raise NotImplementedError(mensagem)


class Python(Tangiveis):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self._direcoes = {
            KEY_RIGHT: self._direita, KEY_LEFT: self._esquerda,
            KEY_UP: self._acima, KEY_DOWN: self._abaixo
        }
        self._direcoes_opostas = {
            KEY_RIGHT: KEY_LEFT, KEY_LEFT: KEY_RIGHT, KEY_UP: KEY_DOWN,
            KEY_DOWN: KEY_UP
        }
        self._corpo = [Aneis(self._x, self._y, self._tela, self._character)]
        self._direcao = KEY_RIGHT
        self._dormir = 0.1
        self._salto = 1

    def _esquerda(self) -> NoReturn:
        """Método que vira para a esquerda."""
        self._y -= self._salto

    def _direita(self) -> NoReturn:
        """Método que vira para a direita."""
        self._y += self._salto

    def _acima(self) -> NoReturn:
        """Método que vira para cima."""
        self._x -= self._salto

    def _abaixo(self) -> NoReturn:
        """Método que vira para baixo."""
        self._x += self._salto

    def atualizar(self, x: int, y: int) -> NoReturn:
        """Método que atualiza os aneis da cobra na tela."""
        aneis = zip([(x, y)] + self._corpo, self._corpo)
        for x, y in aneis:
            y.definir_posicao(x)
            y.atualizar()
        self._tela.refresh()

    def andar(self, nova_direcao) -> NoReturn:
        """Método que faz a cobra se locomover."""
        if self._direcao_oposta(nova_direcao):
            self._direcao = nova_direcao or self._direcao
        metodo = self._direcoes[self._direcao]
        metodo()
        self.atualizar(self._x, self._y)
        sleep(self._dormir)

    def alterar_character(self, character: str) -> NoReturn:
        """Método que altera o caracter da cabeça da cobra."""
        self._corpo[0]._character = character

    def _direcao_oposta(self, direcao: str) -> bool:
        """Método que verifica se a direção é a oposta da atual."""
        return self._direcoes_opostas[self._direcao] != direcao

    def adicionar_anel(self) -> NoReturn:
        """Método que adiciona uma parte a mais na cobra."""
        if self._corpo:
            posicao = self._corpo[-1]._posicao_anterior
        else:
            posicao = self._posicao_anterior
        self._corpo.append(Aneis(*posicao, self._tela, '◯'))  # ⓞ∗⏣


class Aneis(Tangiveis):
    def definir_posicao(self, anel) -> NoReturn:
        """Método que altera a posição atual deste objeto."""
        if isinstance(anel, tuple):
            nova_posicao = anel
        else:
            nova_posicao = anel._posicao_anterior
        self._posicao_anterior = (self._x, self._y)
        self._x, self._y = nova_posicao

    def atualizar(self) -> NoReturn:
        """Método que atualiza o caracter desta instância na tela."""
        self._tela.addch(self._x, self._y, self._character)
        self._tela.addch(*self._posicao_anterior, ' ')

    def efeito(self, python, cabeca) -> NoReturn:
        """Método que mata a cobra caso haja colisão."""
        if cabeca.colisao(self):
            python._vida = 0
            python.alterar_character('☠')


class Barreira(Tangiveis):
    def efeito(self, python: Python, cabeca: Aneis) -> NoReturn:
        """Método que mata a cobra caso haja colisão."""
        if cabeca.colisao(self):
            python._vida = 0
            python.alterar_character('☠')


class Comida(Tangiveis):
    def efeito(self, python: Python, cabeca: Aneis) -> NoReturn:
        """Método que adiciona um anel a cobra."""
        if cabeca.colisao(self):
            python.adicionar_anel()
            self._vida -= 1
