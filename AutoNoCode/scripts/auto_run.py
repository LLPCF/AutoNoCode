import os
import subprocess
import time
import ctypes
import webbrowser
from dotenv import load_dotenv
import psutil

def start_docker():
    try:
        output = subprocess.check_output(['docker', 'info'])
        if b'Containers' in output:
            return True
    except subprocess.CalledProcessError:
        try:
            subprocess.Popen(["C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"])
            time.sleep(30)
            output = subprocess.check_output(['docker', 'info'])
            if b'Containers' in output:
                return True
        except Exception as e:
            print(f"Erro ao iniciar o Docker Desktop: {e}")
    return False

def check_n8n_container():
    try:
        output = subprocess.check_output(['docker', 'ps'], universal_newlines=True)
        return 'n8n' in output
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar o contêiner do n8n: {e}")
        return False

def start_n8n():
    try:
        subprocess.check_call(['docker', 'run', '-d', '--name', 'n8n', '-p', '5678:5678', 'n8nio/n8n:latest'])
        time.sleep(30)
        return check_n8n_container()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar o n8n: {e}")
        return False

def show_message_box():
    message = (
        "Por favor, abra o navegador e acesse a URL:\n\n"
        "http://localhost:5678/\n\n"
        "Em seguida, faça login com seu usuário e senha."
    )
    ctypes.windll.user32.MessageBoxW(0, message, "Aviso", 0x40 | 0x1)

def open_browser():
    url = "http://localhost:5678/"
    if not is_url_open(url):
        webbrowser.open(url)

def is_url_open(url):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in ['chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe']:
            try:
                for item in proc.open_files():
                    if url in item.path:
                        return True
            except psutil.AccessDenied:
                continue
    return False

def load_credentials():
    dotenv_path = os.path.join("C:\\AutoNoCode\\env", ".env")
    load_dotenv(dotenv_path)
    user = os.getenv("N8N_USER")
    password = os.getenv("N8N_PASSWORD")
    return user, password

def main():
    if not start_docker():
        raise EnvironmentError("Falha ao iniciar o Docker Desktop.")
    
    if not check_n8n_container():
        if not start_n8n():
            show_message_box()
            return

    open_browser()
    user, password = load_credentials()
    if user and password:
        print(f"Use as seguintes credenciais para fazer login:\nUsuário: {user}\nSenha: {password}")
    else:
        print("Credenciais não encontradas no arquivo .env")
    show_message_box()

if __name__ == "__main__":
    main()
