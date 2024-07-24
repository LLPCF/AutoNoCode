# src/patch_typings.py
# Filename: patch_typings.py
# Date: 2024-07-01
# Root project folder: AutoNoCode

"""
Módulo para aplicar patches de tipagem.
"""

import logging
import os
import shutil
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def patch_directory(src: str, backup: str) -> Union[bool, None]:
    """
    Aplica patches de tipos a um diretório.

    Args:
        src (str): O caminho do diretório de origem.
        backup (str): O caminho do diretório de backup.

    Returns:
        Union[bool, None]: True se o patch for bem-sucedido, None caso contrário.
    """
    try:
        if not os.path.exists(src):
            raise FileNotFoundError(f"Source directory {src} does not exist.")
        if not backup:
            raise ValueError("Backup directory path is invalid.")

        if os.path.exists(backup):
            shutil.rmtree(backup)
        shutil.copytree(src, backup)
        logger.info("Backup do diretório %s criado em %s", src, backup)
        return True

    except Exception as e:
        logger.error("Erro ao fazer backup do diretório: %s", str(e))
        return None
