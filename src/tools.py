# from types import FunctionType
# from typing import NoReturn  # , Tuple, Any, List
#
# def twice(funcao: FunctionType, *args, **kwargs) -> Tuple[Any]:
#     """Função que repete repete uma outra função duas vezes."""
#     return (funcao(*args, **kwargs), funcao(*args, **kwargs))
#
# def chunk(lista: List[Any], numero: int) -> List[List[Any]]:
#     """Função que recorta uma lista em partes."""
#     return [lista[x: x + numero] for x in range(0, len(lista), numero)]
#
# def adicionar_texto(tela, texto: str, x: int = 0, y: int = 0) -> NoReturn:
#     """Função que adiciona um texto na tela."""
#     tela.addstr(x, y, texto)
#     tela.refresh()
