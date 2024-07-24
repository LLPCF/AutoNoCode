import os
from typing import List

# Lista de diretórios que devem conter um __init__.py
required_dirs: List[str] = [
    "backend/app",
    "backend/app/services",
    "backend/app/controllers",
    "backend/tests",
]

# Função para verificar e criar __init__.py
def ensure_init_py(directory: str) -> None:
    init_file = os.path.join(directory, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w"):
            pass
        print(f"Created {init_file}")
    else:
        print(f"{init_file} already exists")

# Verificar cada diretório na lista
for directory in required_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)
    ensure_init_py(directory)

print("Verification complete.")
