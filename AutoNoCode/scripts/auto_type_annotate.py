import logging
import logging
import logging
import logging
import logging
import logging
import logging
import logging
import logging
logger = logging.getLogger(__name__)
import os
import re
from typing import List, Any

def change_directory_to_project_root(project_dir: str) -> None:
    """
    Muda o diretório atual para o diretório raiz do projeto.

    Parameters:
        project_dir (str): O caminho do diretório do projeto.
    """
    os.chdir(project_dir)

def find_untyped_functions(content: str) -> List[str]:
    """
    Encontra funções que não possuem anotações de tipo no conteúdo fornecido.

    Parameters:
        content (str): O conteúdo do arquivo.

    Returns:
        List[str]: Uma lista de funções que não possuem anotações de tipo.
    """
    untyped_functions = []
    lines = content.split('\n')
    for line in lines:
        match = re.search(r"def (\w+)\(", line)
        if match:
            func_name = match.group(1)
            if "->" not in line:
                untyped_functions.append(func_name)
    return untyped_functions

def add_type_annotations(content: str) -> str:
    """
    Adiciona anotações de tipo às funções sem anotações no conteúdo fornecido.

    Parameters:
        content (str): O conteúdo do arquivo.

    Returns:
        str: O conteúdo com anotações de tipo adicionadas.
    """
    lines = content.split('\n')
    new_content = []
    for line in lines:
        match = re.search(r"def (\w+)\((.*?)\):", line)
        if match and "->" not in line:
            # Adiciona uma anotação básica de tipo para parâmetros e retorno
            params = match.group(2)
            params_annotated = re.sub(r'(\w+)', r'\1: Any', params)
            annotated_line = f"def {match.group(1)}({params_annotated}) -> Any:"
            new_content.append(annotated_line)
        else:
            new_content.append(line)
    return '\n'.join(new_content)

def process_directory(project_dir: str) -> None:
    """
    Processa o diretório do projeto, adicionando anotações de tipo aos arquivos Python.

    Parameters:
        project_dir (str): O caminho do diretório do projeto.
    """
    change_directory_to_project_root(project_dir)
    
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                try:
                    new_content = add_type_annotations(content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Processed {file_path}")
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))  # Define o diretório do projeto
    process_directory(project_dir)
