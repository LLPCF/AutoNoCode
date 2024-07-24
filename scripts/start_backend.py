# Patch: 1.1
# Linha de comando para copiar e colar no terminal: python C:\AutoNoCode\scripts\start_backend.py
# Propósito do arquivo: Iniciar e configurar o contêiner do backend do n8n e abrir o navegador.
# Data de criação: 19/07/2024
# Data de modificação: 20/07/2024
# Informações adicionais relevantes: Certifique-se de que o Docker Desktop esteja instalado no sistema.

import os
import subprocess
import time
import logging
from typing import Optional
from dotenv import load_dotenv
import requests
import webbrowser

# Constantes
N8N_HEALTH_URL = "http://localhost:5678/healthz"
N8N_URL = "http://localhost:5678"
MAX_WAIT_TIME = 300  # 5 minutos
WAIT_INTERVAL = 10

# Configurando o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_docker() -> bool:
    """
    Função para iniciar o Docker Desktop, se não estiver em execução.

    Returns:
        bool: True se o Docker estiver em execução ou foi iniciado com sucesso, False caso contrário.
    """
    try:
        output = subprocess.check_output(['docker', 'info'], stderr=subprocess.STDOUT)
        if b'Containers' in output:
            logging.info("Docker Desktop está em execução.")
            return True
    except subprocess.CalledProcessError:
        logging.info("Docker Desktop não está em execução. Tentando iniciar...")
        try:
            subprocess.Popen(["C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"])
            time.sleep(30)
            output = subprocess.check_output(['docker', 'info'], stderr=subprocess.STDOUT)
            if b'Containers' in output:
                logging.info("Docker Desktop iniciado com sucesso.")
                return True
        except Exception as e:
            logging.error(f"Erro ao iniciar o Docker Desktop: {e}")
    return False

def check_n8n_container() -> bool:
    """
    Função para verificar se o contêiner do n8n está em execução.

    Returns:
        bool: True se o contêiner do n8n estiver em execução, False caso contrário.
    """
    try:
        output = subprocess.check_output(['docker', 'ps'], universal_newlines=True)
        if 'n8n' in output:
            logging.info("Contêiner do n8n está em execução.")
            return True
        else:
            logging.info("Contêiner do n8n não está em execução.")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao verificar o contêiner do n8n: {e}")
        return False

def stop_existing_n8n_container():
    """
    Função para parar e remover contêineres n8n existentes.
    """
    try:
        output = subprocess.check_output(['docker', 'ps', '-q', '--filter', 'name=n8n'], universal_newlines=True)
        container_ids = output.strip().split('\n')
        for container_id in container_ids:
            if container_id:
                logging.info(f"Parando e removendo contêiner existente: {container_id}")
                subprocess.check_call(['docker', 'stop', container_id])
                subprocess.check_call(['docker', 'rm', container_id])
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao parar e remover contêiner existente: {e}")

def start_n8n() -> bool:
    """
    Função para iniciar o contêiner do n8n usando docker-compose.

    Returns:
        bool: True se o contêiner do n8n foi iniciado com sucesso, False caso contrário.
    """
    stop_existing_n8n_container()
    try:
        logging.info("Iniciando o contêiner do n8n com docker-compose...")
        subprocess.check_call(['docker-compose', '-f', 'C:\\AutoNoCode\\env\\docker-compose.yml', 'up', '-d'])
        time.sleep(30)
        return check_n8n_container()
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao iniciar o n8n: {e}")
        return False

def wait_for_n8n(timeout: int = MAX_WAIT_TIME) -> bool:
    """
    Aguarda até que o n8n esteja pronto ou até que o tempo limite seja atingido.

    Args:
        timeout (int): Tempo máximo de espera em segundos. Padrão é 300 segundos (5 minutos).

    Returns:
        bool: True se o n8n estiver pronto, False caso contrário.
    """
    logging.info(f"Aguardando n8n ficar pronto. Timeout: {timeout} segundos")
    for _ in range(0, timeout, WAIT_INTERVAL):
        try:
            response = requests.get(N8N_HEALTH_URL, timeout=5)
            if response.status_code == 200:
                logging.info("n8n está pronto.")
                return True
        except requests.exceptions.RequestException as e:
            logging.debug(f"n8n ainda não está pronto: {e}")
        time.sleep(WAIT_INTERVAL)
    logging.error("Tempo limite excedido aguardando n8n ficar pronto.")
    return False

def main():
    """
    Função principal para iniciar e configurar o backend do n8n.
    """
    env_path = "C:\\AutoNoCode\\env\\.env"
    if not os.path.exists(env_path):
        logging.error(f"Arquivo .env não encontrado em {env_path}. Certifique-se de que ele existe.")
        return

    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv(env_path)

    # Inicia o Docker se não estiver em execução
    if not start_docker():
        logging.error("Falha ao iniciar o Docker Desktop. Certifique-se de que ele está instalado corretamente.")
        return

    # Inicia o contêiner do n8n
    if not start_n8n():
        logging.error("Falha ao iniciar o contêiner do n8n.")
        return

    # Aguarda até que o n8n esteja pronto
    if not wait_for_n8n():
        logging.error("n8n não está respondendo. Verifique se ele foi iniciado corretamente.")
        return

    logging.info("Backend do n8n iniciado com sucesso.")
    webbrowser.open(N8N_URL)

if __name__ == "__main__":
    main()
