# Patch: 1.1
# Linha de comando para copiar e colar no terminal: python C:\AutoNoCode\scripts\start_frontend.py
# Propósito do arquivo: Iniciar o frontend do projeto e abrir no navegador.
# Data de criação: 20/07/2024
# Informações adicionais relevantes: Certifique-se de que todas as dependências do Node.js estejam instaladas.

import os
import subprocess
import webbrowser

def start_frontend():
    os.chdir("C:\\AutoNoCode\\frontend")
    subprocess.check_call(["npm", "install"])
    subprocess.check_call(["npm", "run", "serve"], shell=True)

def main():
    print("Iniciando o frontend...")
    start_frontend()
    webbrowser.open("http://localhost:8080")  # Supondo que o frontend Vue.js esteja configurado para rodar na porta 8080

if __name__ == "__main__":
    main()
