# Patch: C:\AutoNoCode\scripts\start_docker.py
# Propósito do arquivo: Iniciar o Docker Desktop e verificar se está em execução.
# Data de criação: 20/07/2024
# Informações adicionais: Utiliza subprocessos para iniciar o Docker Desktop e verificar seu status.

import subprocess
import time

def start_docker() -> bool:
    """
    Tenta iniciar o Docker Desktop se não estiver em execução.

    Returns:
        bool: True se o Docker Desktop estiver em execução, False caso contrário.
    """
    try:
        output = subprocess.check_output(['docker', 'info'], stderr=subprocess.STDOUT)
        if b'Containers' in output:
            print("Docker Desktop está em execução.")
            return True
    except subprocess.CalledProcessError:
        print("Docker Desktop não está em execução. Tentando iniciar...")
        try:
            subprocess.Popen(["C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"])
            time.sleep(30)
            output = subprocess.check_output(['docker', 'info'], stderr=subprocess.STDOUT)
            if b'Containers' in output:
                print("Docker Desktop iniciado com sucesso.")
                return True
        except Exception as e:
            print(f"Erro ao iniciar o Docker Desktop: {e}")
    return False

if __name__ == "__main__":
    if start_docker():
        print("Docker Desktop está rodando corretamente.")
    else:
        print("Falha ao iniciar o Docker Desktop.")
