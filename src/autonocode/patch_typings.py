# Path: C:\AutoNoCode\src\patch_typings.py

"""
Filename: patch_typings.py
Date: 2024-07-02
Root project folder: AutoNoCode
"""

import logging
import os
import shutil
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def patch_directory(src_directory: str, backup_directory: str) -> Union[bool, None]:
    """
    Copia o diretório de origem para o diretório de backup e aplica anotações de tipo.

    Args:
        src_directory (str): O caminho do diretório de origem.
        backup_directory (str): O caminho do diretório de backup.

    Returns:
        bool: Retorna True se a cópia for bem-sucedida, caso contrário, False.

    Raises:
        FileNotFoundError: Se o diretório de origem não existir.
        ValueError: Se o diretório de backup for inválido.
    """
    if not os.path.exists(src_directory):
        raise FileNotFoundError(f"Source directory {src_directory} does not exist.")

    if not backup_directory:
        raise ValueError("Backup directory must be a valid path.")

    try:
        shutil.copytree(src_directory, backup_directory)
        # Lógica adicional para aplicar anotações de tipo no diretório pode ser adicionada aqui
        return True
    except Exception as e:
        logger.error(f"An error occurred while patching the directory: {e}")
        return None
