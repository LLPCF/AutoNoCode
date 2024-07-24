# auto_fix.py
import os
import subprocess

# Lista de diretórios e arquivos a serem verificados
targets = ["C:\\AutoNoCode\\src", "C:\\AutoNoCode\\tests"]

# Verifica se os diretórios existem
existing_targets = [target for target in targets if os.path.exists(target)]

if not existing_targets:
    print("Nenhum dos diretórios especificados existe.")
    exit(1)

# Comandos para executar as ferramentas
commands = [
    ["black"] + existing_targets,
    ["isort"] + existing_targets,
    ["pylint"] + existing_targets,
    ["pyright"]
]

def run_commands(commands):
    for command in commands:
        print(f"Running {' '.join(command)}...")
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print(f"Command {' '.join(command)} failed with output:")
            print(result.stdout)
            print(result.stderr)
        else:
            print(f"Command {' '.join(command)} executed successfully.")

if __name__ == "__main__":
    run_commands(commands)
