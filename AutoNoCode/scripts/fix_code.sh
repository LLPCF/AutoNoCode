#!/bin/bash

# Formatar o código com black
black .

# Ordenar importações com isort
isort .

# Verificar a qualidade do código com flake8
flake8 .

# Verificar tipos com mypy
mypy .

# Verificar código com pyright
pyright
