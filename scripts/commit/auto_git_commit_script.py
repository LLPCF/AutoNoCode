# Patch 1.13
# Linha de comando para copiar e colar no terminal:
# python C:/AutoNoCode/scripts/commit/auto_git_commit_script.py
# Propósito do arquivo: Realizar commit e push automáticos para um repositório Git.
# Data de criação: 20/07/2024
# Informações adicionais relevantes: Certifique-se de que a biblioteca GitPython, python-dotenv e pre-commit estão instaladas.

import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import subprocess
from typing import Optional
from git import Repo, GitCommandError

# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carregar variáveis de ambiente do arquivo .env
env_path = 'C:/AutoNoCode/env/.env'
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    logging.error(f"Arquivo .env não encontrado em {env_path}")
    exit(1)

# Constantes
VENV_PATH = r'C:\AutoNoCode\env_pre_commit'  # Use um ambiente virtual isolado para pre-commit
REPO_PATH = os.getenv('REPO_PATH')
REPO_URL = os.getenv('REPO_URL')
GIT_USERNAME = os.getenv('GIT_USERNAME')
GIT_EMAIL = os.getenv('GIT_EMAIL')
COMMIT_MESSAGE = 'Auto commit'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Verificação de variáveis de ambiente e ambiente virtual
if not os.path.exists(VENV_PATH):
    logging.error(f"Ambiente virtual não encontrado em {VENV_PATH}")
    exit(1)
if not REPO_PATH:
    logging.error("REPO_PATH não está definido no arquivo .env")
    exit(1)
if not REPO_URL:
    logging.error("REPO_URL não está definido no arquivo .env")
    exit(1)
if not GIT_USERNAME:
    logging.error("GIT_USERNAME não está definido no arquivo .env")
    exit(1)
if not GIT_EMAIL:
    logging.error("GIT_EMAIL não está definido no arquivo .env")
    exit(1)
if not GITHUB_TOKEN:
    logging.error("GITHUB_TOKEN não está definido no arquivo .env")
    exit(1)

def setup_repo(repo_path: str) -> Repo:
    """
    Configura o repositório Git com as informações do usuário.

    Args:
        repo_path (str): Caminho para o repositório local.

    Returns:
        Repo: Objeto Repo configurado.
    """
    try:
        repo = Repo(repo_path)
        with repo.config_writer() as git_config:
            git_config.set_value('user', 'name', GIT_USERNAME)
            git_config.set_value('user', 'email', GIT_EMAIL)
        return repo
    except GitCommandError as e:
        logging.error(f"Erro ao configurar o repositório: {e}")
        raise

def remove_lock_file(repo_path: str) -> None:
    """
    Remove o arquivo de bloqueio do repositório Git, se existir.

    Args:
        repo_path (str): Caminho para o repositório local.
    """
    lock_file_path = os.path.join(repo_path, '.git', 'index.lock')
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)
        logging.info(f'Removido o arquivo de bloqueio: {lock_file_path}')

def delete_pre_commit_hook(repo_path: str) -> None:
    """
    Remove o arquivo de hook pre-commit, se existir.

    Args:
        repo_path (str): Caminho para o repositório local.
    """
    hook_file_path = os.path.join(repo_path, '.git', 'hooks', 'pre-commit')
    if os.path.exists(hook_file_path):
        os.remove(hook_file_path)
        logging.info(f'Removido o arquivo de hook: {hook_file_path}')

def fix_pre_commit_hook(repo_path: str) -> None:
    """
    Cria um hook pre-commit compatível com Windows.

    Args:
        repo_path (str): Caminho para o repositório local.
    """
    hook_file_path = os.path.join(repo_path, '.git', 'hooks', 'pre-commit')
    bat_file_path = os.path.join(repo_path, '.git', 'hooks', 'pre-commit.bat')

    # Criar o arquivo .bat
    bat_content = f"""@echo off
call "{VENV_PATH}\\Scripts\\activate.bat"
"{VENV_PATH}\\Scripts\\pre-commit.exe" run --all-files
"""
    try:
        with open(bat_file_path, 'w', newline='\r\n') as file:
            file.write(bat_content)
        logging.info(f"Arquivo .bat criado: {bat_file_path}")
    except Exception as e:
        logging.error(f"Erro ao criar arquivo .bat: {e}")

    # Verificar se o arquivo .bat foi criado
    if os.path.exists(bat_file_path):
        logging.info(f"Arquivo .bat verificado: {bat_file_path}")
    else:
        logging.error(f"Falha ao criar arquivo .bat: {bat_file_path}")

    # Criar o arquivo pre-commit que chama o .bat
    hook_content = f"""#!/bin/sh
cmd.exe /c "{bat_file_path.replace('\\', '/')}"
"""
    try:
        with open(hook_file_path, 'w', newline='\n') as file:
            file.write(hook_content)
        logging.info(f"Arquivo pre-commit criado: {hook_file_path}")
    except Exception as e:
        logging.error(f"Erro ao criar arquivo pre-commit: {e}")

    # Verificar se o arquivo pre-commit foi criado
    if os.path.exists(hook_file_path):
        logging.info(f"Arquivo pre-commit verificado: {hook_file_path}")
    else:
        logging.error(f"Falha ao criar arquivo pre-commit: {hook_file_path}")

def install_pre_commit_hooks(repo_path: str) -> None:
    """
    Instala os hooks de pre-commit.

    Args:
        repo_path (str): Caminho para o repositório local.
    """
    try:
        delete_pre_commit_hook(repo_path)

        # Instalar pre-commit no ambiente virtual
        subprocess.run([os.path.join(VENV_PATH, 'Scripts', 'python.exe'), '-m', 'pip', 'install', '--force-reinstall', 'pre-commit'], check=True)

        # Instalar os hooks de pre-commit
        subprocess.run([os.path.join(VENV_PATH, 'Scripts', 'pre-commit.exe'), 'install'], cwd=repo_path, check=True)

        fix_pre_commit_hook(repo_path)

        logging.info("Hooks de pre-commit instalados com sucesso")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao instalar hooks de pre-commit: {e}")
        raise

def verify_hook_files(repo_path: str) -> None:
    """
    Verifica se os arquivos de hook foram criados corretamente.

    Args:
        repo_path (str): Caminho para o repositório local.
    """
    hook_file_path = os.path.join(repo_path, '.git', 'hooks', 'pre-commit')
    bat_file_path = os.path.join(repo_path, '.git', 'hooks', 'pre-commit.bat')

    if os.path.exists(hook_file_path):
        logging.info(f"Arquivo pre-commit encontrado: {hook_file_path}")
        with open(hook_file_path, 'r') as file:
            logging.info(f"Conteúdo do pre-commit:\n{file.read()}")
    else:
        logging.error(f"Arquivo pre-commit não encontrado: {hook_file_path}")

    if os.path.exists(bat_file_path):
        logging.info(f"Arquivo pre-commit.bat encontrado: {bat_file_path}")
        with open(bat_file_path, 'r') as file:
            logging.info(f"Conteúdo do pre-commit.bat:\n{file.read()}")
    else:
        logging.error(f"Arquivo pre-commit.bat não encontrado: {bat_file_path}")

def auto_commit(repo_path: str) -> None:
    """
    Realiza o commit e push automáticos para o repositório Git.

    Args:
        repo_path (str): Caminho para o repositório local.
    """
    logging.info("Iniciando processo de auto commit")
    try:
        repo = setup_repo(repo_path)
        remove_lock_file(repo_path)
        install_pre_commit_hooks(repo_path)
        verify_hook_files(repo_path)

        repo.git.add(A=True)
        if repo.is_dirty(untracked_files=True):
            repo.index.commit(COMMIT_MESSAGE)
            origin = repo.remote(name='origin')
            origin.push()
            logging.info(f'Commit realizado em {datetime.now()}')
        else:
            logging.info('Nenhuma mudança para commit')
    except GitCommandError as e:
        logging.error(f"Erro durante operações Git: {e}")
        raise
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        raise

def check_pre_commit_installation():
    """
    Verifica se o pre-commit está instalado corretamente.
    """
    try:
        result = subprocess.run([os.path.join(VENV_PATH, 'Scripts', 'pre-commit.exe'), '--version'],

          capture_output=True, text=True, check=True)
        logging.info(f"pre-commit version: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao verificar a instalação do pre-commit: {e}")
        raise

def check_git_shell():
    """
    Verifica e configura o shell do Git para cmd.exe no Windows.
    """
    try:
        # Verifica se o Git está instalado
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, check=True)
        logging.info(f"Git está instalado: {result.stdout.strip()}")

        # Configurações do Git
        subprocess.run(['git', 'config', '--global', 'core.autocrlf', 'true'], check=True)
        logging.info("Git configurado para usar autocrlf=true")

        subprocess.run(['git', 'config', '--global', 'core.longpaths', 'true'], check=True)
        logging.info("Git configurado para suportar caminhos longos")

        subprocess.run(['git', 'config', '--global', 'core.shell', 'cmd'], check=True)
        logging.info("Git configurado para usar cmd.exe como shell")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao configurar o Git: {e}")
        raise

def main() -> None:
    """
    Função principal para verificar se o repositório está clonado e realizar o commit automático.
    """
    try:
        check_git_shell()

        if not os.path.exists(REPO_PATH):
            logging.info(f"Clonando repositório {REPO_URL} para {REPO_PATH}")
            Repo.clone_from(REPO_URL, REPO_PATH)

        check_pre_commit_installation()
        auto_commit(REPO_PATH)
    except Exception as e:
        logging.error(f"Erro na função principal: {e}")
        raise

if __name__ == '__main__':
    main()
