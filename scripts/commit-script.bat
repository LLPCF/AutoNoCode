::C:\AutoNoCode\scripts\commit-script.bat "Sua mensagem de commit aqui"
:: cmd /c "C:\AutoNoCode\scripts\commit-script.bat \"Sua mensagem de commit aqui\""

@echo off
:: Ativar o ambiente virtual
call C:\AutoNoCode\env\Scripts\activate.bat

:: Verificar se pre-commit está instalado
where pre-commit >nul 2>nul
if %errorlevel% neq 0 (
    echo pre-commit não está instalado. Instalando...
    pip install pre-commit
)

:: Instalar os hooks pre-commit se necessário
pre-commit install -f -c C:\AutoNoCode\.pre-commit-config.yaml

:: Verificar se a instalação do pre-commit foi bem-sucedida
if %errorlevel% neq 0 (
    echo Falha na instalação do pre-commit. Verifique os erros acima.
    exit /b 1
)

:: Executar pre-commit
pre-commit run --all-files

:: Verificar se o pre-commit executou com sucesso
if %errorlevel% neq 0 (
    echo Falha na execução do pre-commit. Verifique os erros acima.
    exit /b 1
)

:: Adicionar os arquivos ao stage
git add .

:: Fazer o commit com uma mensagem
set "commitMessage=%~1"
if "%commitMessage%"=="" (
    echo Por favor, forneça uma mensagem de commit.
    exit /b 1
)
git commit -m "%commitMessage%"

:: Verificar se o commit foi bem-sucedido
if %errorlevel% neq 0 (
    echo Falha ao criar o commit. Verifique os erros acima.
    exit /b 1
)

:: Enviar o commit para o repositório remoto
git push

:: Verificar se o push foi bem-sucedido
if %errorlevel% neq 0 (
    echo Falha ao enviar o commit. Verifique sua conexão e permissões.
    exit /b 1
)

echo Commit e push realizados com sucesso.
exit /b 0
