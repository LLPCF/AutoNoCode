import os
from typing import Any, Dict

def analyze_types(directory: str) -> Dict[str, int]:
    """
    Analisa os tipos de arquivos em um diretório.

    Args:
        directory (str): O caminho do diretório a ser analisado.

    Returns:
        Dict[str, int]: Dicionário com informações sobre os tipos de arquivos.
    """
    file_types = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in file_types:
                file_types[file_ext] += 1
            else:
                file_types[file_ext] = 1
    return file_types

def main() -> None:
    directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "some_directory"))
    types_analysis = analyze_types(directory)
    print(types_analysis)

if __name__ == "__main__":
    main()
