import logging
import os
import subprocess
import sys
from typing import List
import git  # Certifique-se de ter o módulo gitpython instalado

logging.basicConfig(level=logging.INFO)

class AutoTyper:
    def __init__(self, repo_path: str) -> None:
        """
        Inicializa a classe AutoTyper.

        Args:
            repo_path (str): Caminho para o repositório Git.
        """
        self.repo_path = repo_path

    def run(self) -> None:
        """
        Executa o processo de backup, criação de branch e adição de anotações de tipo.
        """
        try:
            self.create_backup()
            self.create_git_branch()
            self.add_type_annotations()
        except Exception as e:
            logging.error(f"Erro durante o processo: {e}")
            sys.exit(1)

    def create_backup(self) -> None:
        """
        Cria um backup do diretório src.
        """
        logging.info("Criando backup do diretório src...")
        backup_command = 'cp -r src src_backup'
        result = subprocess.run(backup_command, shell=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, backup_command)

    def create_git_branch(self) -> git.Repo:
        """
        Cria um novo branch no repositório Git.

        Returns:
            git.Repo: Instância do repositório Git.
        """
        logging.info("Criando novo branch no repositório Git...")
        branch_name = 'add-type-annotations'
        repo = git.Repo(self.repo_path)
        if branch_name in repo.branches:
            logging.warning(f"A branch '{branch_name}' já existe. Continuando...")
        else:
            repo.git.checkout('-b', branch_name)
            logging.info(f"Criado branch: {branch_name}")
        return repo

    def add_type_annotations(self) -> None:
        """
        Adiciona anotações de tipo aos arquivos Python usando pyannotate.
        """
        logging.info("Adicionando anotações de tipo aos arquivos Python...")
        for root, _, files in os.walk('src'):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    logging.info(f"Adicionando anotações de tipo ao arquivo {file_path}")
                    annotate_command = f'pyannotate --type-info {file_path}.types --apply {file_path}'
                    result = subprocess.run(annotate_command, shell=True)
                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, annotate_command)

def main() -> None:
    """
    Função principal para executar o AutoTyper.
    """
    if len(sys.argv) < 2:
        logging.error("Por favor, forneça o caminho para o repositório.")
        sys.exit(1)

    repo_path = sys.argv[1]
    auto_typer = AutoTyper(repo_path)

    dry_run = '--dry-run' in sys.argv
    if dry_run:
        logging.info("Executando em modo de teste (dry run). Nenhuma alteração será feita.")
    else:
        auto_typer.run()

if __name__ == "__main__":
    main()
