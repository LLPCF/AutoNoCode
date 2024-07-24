import os
from typing import Any, Dict, List

# Estrutura esperada do projeto
expected_structure: Dict[str, Any] = {
    "backend": {
        "app": ["__init__.py", "main.py", "models.py", "schemas.py"],
        "services": ["__init__.py"],
        "controllers": [
            "__init__.py",
            "video_controller.py",
            "admin_controller.py",
            "stats_controller.py",
            "upload_controller.py",
        ],
        "tests": ["__init__.py"],
    },
    "venv": [],
}

# Caminho raiz do projeto
root_path = "C:\\AutoNoCode"

def check_structure(expected_structure: Dict[str, Any], root_path: str) -> List[str]:
    """
    Verifica a estrutura do projeto conforme definido em expected_structure.

    Parameters:
        expected_structure (Dict[str, Any]): Dicionário contendo a estrutura esperada do projeto.
        root_path (str): Caminho raiz do projeto.

    Returns:
        List[str]: Lista de arquivos ou diretórios faltantes.
    """
    missing_files = []
    for main_directory, sub_structure in expected_structure.items():
        main_dir_path = os.path.join(root_path, main_directory)
        if isinstance(sub_structure, dict):
            for sub_directory, files in sub_structure.items():
                dir_path = os.path.join(main_dir_path, sub_directory.replace("/", os.sep))
                if not os.path.exists(dir_path):
                    missing_files.append(f"Directory missing: {dir_path}")
                for file in files:
                    file_path = os.path.join(dir_path, file)
                    if not os.path.exists(file_path):
                        missing_files.append(f"File missing: {file_path}")
        elif isinstance(sub_structure, list):
            if not os.path.exists(main_dir_path):
                missing_files.append(f"Directory missing: {main_dir_path}")
            for file in sub_structure:
                file_path = os.path.join(main_dir_path, file)
                if not os.path.exists(file_path):
                    missing_files.append(f"File missing: {file_path}")
    return missing_files
