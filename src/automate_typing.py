"""
Módulo de tipagem automática.
"""

import logging

logger = logging.getLogger(__name__)

def backup_directory(src: str, backup: str) -> bool:
    """
    Realiza o backup do diretório especificado.

    Args:
        src (str): Diretório de origem.
        backup (str): Diretório de backup.

    Returns:
        bool: True se o backup for bem-sucedido, caso contrário False.
    """
    try:
        if os.path.exists(backup):
            shutil.rmtree(backup)
        shutil.copytree(src, backup)
        logger.info("Backup do diretório %s criado em %s", src, backup)
        return True
    except OSError as error:
        logger.error("Erro ao criar o backup: %s", error)
        return False
