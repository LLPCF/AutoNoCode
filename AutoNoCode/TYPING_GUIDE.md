# Guia de Tipagem Python

Este guia fornece uma introdução rápida à tipagem em Python.

## Tipos Básicos

- `int`: números inteiros
- `float`: números de ponto flutuante
- `str`: strings
- `bool`: valores booleanos

## Coleções

- `List[T]`: lista de elementos do tipo T
- `Dict[K, V]`: dicionário com chaves do tipo K e valores do tipo V
- `Tuple[T1, T2, ...]`: tupla com tipos específicos

## Funções

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
