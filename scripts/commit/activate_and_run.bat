@echo off
REM Patch: 2.4
REM Linha de comando para copiar e colar no terminal: call C:\AutoNoCode\scripts\commit\activate_and_run.bat
REM Propósito do arquivo: Ativar o ambiente virtual e instalar o pre-commit.
REM Data de criação: 20/07/2024
REM Informações adicionais relevantes: Certifique-se de que o pre-commit está instalado no ambiente virtual.

REM Ativar o ambiente virtual
call C:\AutoNoCode\env\Scripts\activate.bat

REM Verificar se a ativação foi bem-sucedida
if errorlevel 1 (
    echo Falha ao ativar o ambiente virtual
    exit /b 1
)

REM Instalar o pre-commit
C:\AutoNoCode\env\Scripts\pip.exe install pre-commit

REM Verificar se a instalação foi bem-sucedida
if errorlevel 1 (
    echo Falha ao instalar pre-commit
    exit /b 1
)

REM Executar o comando pre-commit install
C:\AutoNoCode\env\Scripts\pre-commit.exe install

REM Verificar se a instalação foi bem-sucedida
if errorlevel 1 (
    echo Falha ao instalar pre-commit hooks
    exit /b 1
)

echo Ambiente virtual ativado e pre-commit instalado com sucesso
