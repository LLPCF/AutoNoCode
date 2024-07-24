"""
Arquivo: start_n8n.py
Data: 2024-07-10
Descrição: Script para iniciar o Docker, subir o contêiner do n8n e abrir ou focar a página do n8n no Google Chrome.

Requisitos:
- Docker Desktop instalado no caminho padrão: "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"
- Arquivo docker-compose.yml configurado e localizado em "C:\\AutoNoCode\\docker-compose.yml"
- Bibliotecas Python necessárias: subprocess, time, requests, psutil, webbrowser, win32gui, win32com.client, win32process

Uso:
    python start_n8n.py

Melhores Práticas:
- Seguir o PEP 8 para estilo de código.
- Documentação clara com docstrings.
- Estrutura de arquivos organizada em módulos.
- Tratamento robusto de exceções.
- Boas práticas de importação.
- Uso de anotações de tipo.
- Escrever testes automatizados.
- Manter código limpo e simples.
- Uso de controle de versão.
- Utilizar ferramentas de qualidade de código.

Autor: [Seu Nome]
"""

import os
import subprocess
import time
import ctypes
import requests
import psutil
import webbrowser
import threading
import win32gui
import win32process
import win32com.client
from dotenv import load_dotenv

def log(message: str) -> None:
    """
    Função de log para exibir mensagens com timestamp.

    Args:
        message (str): Mensagem a ser exibida no log.
    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(f"{timestamp} - {message}")

def start_docker() -> bool:
    """
    Inicia o Docker Desktop se não estiver em execução.

    Returns:
        bool: True se o Docker foi iniciado com sucesso ou já estava em execução, False caso contrário.
    """
    docker_path = "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"
    if os.path.exists(docker_path):
        subprocess.Popen(docker_path)
        log("Iniciando Docker Desktop...")
        time.sleep(30)  # Aguarda 30 segundos para o Docker iniciar
    else:
        log("Caminho do Docker Desktop não encontrado.")
        return False
    return True

def is_docker_running() -> bool:
    """
    Verifica se o Docker Desktop está em execução.

    Returns:
        bool: True se o Docker está em execução, False caso contrário.
    """
    try:
        output = subprocess.check_output(['docker', 'info'], stderr=subprocess.STDOUT)
        if b'Containers' in output:
            log("Docker Desktop está em execução.")
            return True
    except subprocess.CalledProcessError:
        log("Docker Desktop não está em execução.")
    return False

def check_n8n_container() -> bool:
    """
    Verifica se o contêiner do n8n está em execução.

    Returns:
        bool: True se o contêiner do n8n está em execução, False caso contrário.
    """
    try:
        output = subprocess.check_output(['docker', 'ps'], universal_newlines=True)
        if 'n8n' in output:
            log("Contêiner do n8n está em execução.")
            return True
        else:
            log("Contêiner do n8n não está em execução.")
            return False
    except subprocess.CalledProcessError as e:
        log(f"Erro ao verificar o contêiner do n8n: {e}")
        return False

def start_n8n_container() -> bool:
    """
    Subir novo contêiner do n8n usando Docker Compose.

    Returns:
        bool: True se o contêiner do n8n foi iniciado com sucesso, False caso contrário.
    """
    try:
        log("Subindo novo contêiner do n8n com docker-compose...")
        subprocess.check_call(['docker-compose', '-f', 'C:\\AutoNoCode\\docker-compose.yml', 'up', '-d'])
        time.sleep(30)  # Aguarda 30 segundos para o n8n iniciar
        return check_n8n_container()
    except subprocess.CalledProcessError as e:
        log(f"Erro ao iniciar o n8n: {e}")
        return False

def show_message_box(message: str) -> None:
    """
    Exibe uma mensagem em uma MessageBox do Windows.

    Args:
        message (str): Mensagem a ser exibida.
    """
    ctypes.windll.user32.MessageBoxW(0, message, "Aviso", 0x40 | 0x1)

def is_chrome_open() -> bool:
    """
    Verifica se o Google Chrome está aberto.

    Returns:
        bool: True se o Chrome está aberto, False caso contrário.
    """
    def enum_window_titles(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                if 'chrome.exe' in process.name().lower():
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        windows.append(title)
            except psutil.NoSuchProcess:
                pass

    chrome_windows = []
    win32gui.EnumWindows(enum_window_titles, chrome_windows)
    return len(chrome_windows) > 0

def check_chrome_and_prompt() -> None:
    """
    Verifica se o Chrome está aberto e, se não estiver, solicita ao usuário para abri-lo.
    """
    while not is_chrome_open():
        show_message_box("Por favor, abra o Google Chrome.")
        time.sleep(5)  # Espera 5 segundos antes de verificar novamente
    log("Google Chrome está aberto.")

def find_chrome_window(url: str):
    """
    Procura a janela do Google Chrome com a URL especificada.

    Args:
        url (str): URL a ser encontrada na janela do Chrome.

    Returns:
        hwnd (int): Handle da janela encontrada ou None se não encontrada.
    """
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    windows = []
    win32gui.EnumWindows(callback, windows)
    for hwnd, title in windows:
        if url in title and "Google Chrome" in title:
            return hwnd
    return None

def focus_window(hwnd) -> None:
    """
    Foca na janela do Google Chrome com a URL especificada.

    Args:
        hwnd (int): Handle da janela a ser focada.
    """
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)

def open_or_focus_n8n_page() -> None:
    """
    Abre ou foca a página do n8n no Google Chrome.
    """
    url = "http://localhost:5678"
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    
    # Procura pela janela do Chrome com a URL desejada
    hwnd = find_chrome_window(url)
    
    if hwnd:
        log(f"Página {url} já está aberta. Movendo o foco para ela.")
        focus_window(hwnd)
    else:
        log(f"Abrindo nova página: {url}")
        webbrowser.get(chrome_path).open(url)
        
        # Espera um pouco para a página carregar e então tenta focar nela
        time.sleep(5)
        hwnd = find_chrome_window(url)
        if hwnd:
            focus_window(hwnd)

def load_api_key() -> str:
    """
    Carrega a API key do n8n a partir do arquivo .env.

    Returns:
        str: API key carregada ou None se não encontrada.
    """
    dotenv_path = "C:\\AutoNoCode\\env\\.env"
    load_dotenv(dotenv_path)
    return os.getenv("N8N_API_KEY")

def wait_for_n8n() -> bool:
    """
    Verifica se o n8n está pronto e respondendo.

    Returns:
        bool: True se o n8n está pronto, False caso contrário.
    """
    url = "http://localhost:5678/healthz"
    for _ in range(30):  # Aguarde até 5 minutos
        try:
            response = requests.get(url)
            if response.status_code == 200:
                log("n8n está pronto.")
                return True
        except requests.exceptions.RequestException as e:
            log(f"Erro ao tentar conectar ao n8n: {e}")
        time.sleep(10)
    return False

def check_initial_setup() -> bool:
    """
    Verifica se a configuração inicial do n8n é necessária.

    Returns:
        bool: True se a configuração inicial for necessária, False caso contrário.
    """
    url = "http://localhost:5678/"
    try:
        response = requests.get(url)
        if "Set up owner account" in response.text:
            log("Configuração inicial do n8n necessária.")
            open_or_focus_n8n_page()
            return True
        return False
    except requests.exceptions.RequestException as e:
        log(f"Erro ao acessar a página inicial do n8n: {e}")
        return False

def list_workflows(api_key: str) -> None:
    """
    Lista os workflows do n8n utilizando a API key.

    Args:
        api_key (str): API key para autenticação.
    """
    url = "http://localhost:5678/api/v1/workflows"
    headers = {
        "X-N8N-API-KEY": api_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        workflows = response.json()
        log(f"Workflows: {workflows}")
    except requests.exceptions.RequestException as e:
        log(f"Erro ao listar workflows: {e}")

def main() -> None:
    """
    Função principal para iniciar o Docker, subir o contêiner do n8n e abrir ou focar a página do n8n.
    """
    # Inicia a verificação do Chrome em uma thread separada
    chrome_thread = threading.Thread(target=check_chrome_and_prompt)
    chrome_thread.start()

    # Executa outras tarefas enquanto verifica o Chrome
    if not is_docker_running():
        if not start_docker():
            show_message_box("Falha ao iniciar o Docker Desktop.")
            return

    if not check_n8n_container():
        if not start_n8n_container():
            show_message_box("Falha ao iniciar o contêiner do n8n.")
            return

    if wait_for_n8n():
        if check_initial_setup():
            show_message_box("Configuração inicial do n8n necessária. Por favor, abra o navegador e siga as instruções.")
            return

        api_key = load_api_key()
        if api_key:
            log("Usando a API key para fazer requisições autenticadas ao n8n.")
            list_workflows(api_key)
        else:
            show_message_box("API key não encontrada no arquivo .env")
    else:
        show_message_box("O n8n não ficou pronto a tempo. Verifique o contêiner e tente novamente.")

    # Aguarda a conclusão da verificação do Chrome e abre ou foca na página do n8n
    chrome_thread.join()
    open_or_focus_n8n_page()

if __name__ == "__main__":
    main()

