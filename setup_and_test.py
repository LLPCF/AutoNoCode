import os
import shutil
import subprocess


def create_directories() -> None:
    os.makedirs('src', exist_ok=True)
    os.makedirs('tests', exist_ok=True)

def create_patch_typings_py() -> None:
    content = '''\
# Path: C:\\AutoNoCode\\src\\patch_typings.py
# Filename: patch_typings.py
# Date: 2024-07-02
# Root project folder: AutoNoCode

import os
import shutil
import logging
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
        Union[bool, None]: Retorna True se a cópia for bem-sucedida, None caso contrário.

    Raises:
        FileNotFoundError: Se o diretório de origem não existir.
        ValueError: Se o diretório de backup for inválido.
    """
    if not os.path.exists(src_directory):
        raise FileNotFoundError(f"Source directory {src_directory} does not exist.")

    if not backup_directory:
        raise ValueError("Backup directory must be a valid path.")

    try:
        if os.path.exists(backup_directory):
            shutil.rmtree(backup_directory)
        shutil.copytree(src_directory, backup_directory)
        logger.info(f"Backup do diretório {src_directory} criado em {backup_directory}")
        return True
    except Exception as e:
        logger.error(f"An error occurred while patching the directory: {e}")
        return None
'''
    with open('src/patch_typings.py', 'w') as f:
        f.write(content)

def create_test_patch_typings_py() -> None:
    content = '''\
# Path: C:\\AutoNoCode\\tests\\test_patch_typings.py
# Filename: test_patch_typings.py
# Date: 2024-07-02
# Root Project Folder: AutoNoCode

import os
import shutil
import unittest
from typing import Optional

# Ensure the correct import path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from patch_typings import patch_directory

class TestPatchTypings(unittest.TestCase):
    src_directory: str
    backup_directory: str

    def setUp(self) -> None:
        """
        Configura os diretórios de teste antes de cada teste.
        """
        self.src_directory = 'test_src'
        self.backup_directory = 'test_backup'

        # Cria o diretório de origem para os testes
        os.makedirs(self.src_directory, exist_ok=True)
        with open(os.path.join(self.src_directory, 'test.txt'), 'w') as f:
            f.write('This is a test file.')

    def tearDown(self) -> None:
        """
        Limpa os diretórios de teste após cada teste.
        """
        if os.path.exists(self.src_directory):
            shutil.rmtree(self.src_directory)
        if os.path.exists(self.backup_directory):
            shutil.rmtree(self.backup_directory)

    def test_patch_directory(self) -> None:
        """
        Testa a função patch_directory para garantir que ela copia o diretório corretamente.
        """
        result: Optional[bool] = patch_directory(self.src_directory, self.backup_directory)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.backup_directory))
        self.assertTrue(os.path.isfile(os.path.join(self.backup_directory, 'test.txt')))

    def test_patch_directory_src_not_exists(self) -> None:
        """
        Testa a função patch_directory quando o diretório de origem não existe.
        """
        shutil.rmtree(self.src_directory)
        with self.assertRaises(FileNotFoundError):
            patch_directory(self.src_directory, self.backup_directory)

    def test_patch_directory_invalid_backup(self) -> None:
        """
        Testa a função patch_directory quando o diretório de backup é inválido.
        """
        with self.assertRaises(ValueError):
            patch_directory(self.src_directory, '')

if __name__ == '__main__':
    unittest.main()
'''
    with open('tests/test_patch_typings.py', 'w') as f:
        f.write(content)

def create_pytest_ini() -> None:
    content = '''\
# Path: C:\\AutoNoCode\\pytest.ini
# Filename: pytest.ini
# Date: 2024-07-02
# Root project folder: AutoNoCode

[pytest]
norecursedirs = node_modules src_backup
testpaths = tests
addopts = --ignore=tests/test_output.txt
pythonpath = src
'''
    with open('pytest.ini', 'w') as f:
        f.write(content)

def create_pyproject_toml() -> None:
    content = '''\
# C:\\AutoNoCode\\pyproject.toml
[tool.poetry]
name = "autonocode"
version = "0.1.0"
description = "AutoNoCode Project"
authors = ["LLPCF <95063971+LLPCF@users.noreply.github.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"

[tool.poetry.dev-dependencies]
pytest = "^8.2.2"
mypy = "^1.10.1"
autopep8 = "^2.3.1"
isort = "^5.13.2"
pyannotate = "^1.2.0"
gitpython = "^3.1.43"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
norecursedirs = "node_modules test_output.txt"
testpaths = ["tests"]

[tool.pyright]
include = ["src", "tests"]
exclude = ["**/node_modules", "**/__pycache__", "src_backup"]
strict = ["src", "tests"]
typeCheckingMode = "strict"
reportMissingImports = true
reportGeneralTypeIssues = true
'''
    with open('pyproject.toml', 'w') as f:
        f.write(content)

def install_dependencies() -> None:
    subprocess.run(['poetry', 'install'], check=True)

def run_tests() -> None:
    subprocess.run(['poetry', 'run', 'pytest'], check=True)

def main() -> None:
    create_directories()
    create_patch_typings_py()
    create_test_patch_typings_py()
    create_pytest_ini()
    create_pyproject_toml()
    install_dependencies()
    run_tests()

if __name__ == '__main__':
    main()
