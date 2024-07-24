# Filename: common_utils.py
# Date: 2024-07-01
# Root project folder: AutoNoCode

"""
Funções utilitárias comuns.
"""

import logging
import os
import shutil
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def backup_directory(src: str, backup: str) -> Union[bool, None]:
    """
    Faz o backup do diretório src no diretório backup.

    Args:
        src (str): Diretório de origem.
        backup (str): Diretório de backup.

    Returns:
        Union[bool, None]: True se o backup for bem-sucedido, None caso contrário.
    """
    try:
        if os.path.exists(backup):
            shutil.rmtree(backup)
        shutil.copytree(src, backup)
        logger.info("Backup do diretório %s criado em %s", src, backup)
        return True
    except Exception as e:
        logger.error("Erro ao criar backup: %s", e)
        return None
