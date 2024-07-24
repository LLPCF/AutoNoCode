import os
from dotenv import load_dotenv
from datetime import datetime
import subprocess

# Carregar variáveis de ambiente do arquivo .env
env_path = 'C:/AutoNoCode/env/.env'
load_dotenv(dotenv_path=env_path)

# Configurações do repositório e do commit a partir das variáveis de ambiente
REPO_PATH = os.getenv('REPO_PATH')
REPO_URL = os.getenv('REPO_URL')
GIT_USERNAME = os.getenv('GIT_USERNAME')
GIT_EMAIL = os.getenv('GIT_EMAIL')
COMMIT_MESSAGE = 'Auto commit'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def setup_repo():
    import git  # Importação dentro da função para evitar problemas de importação circular
    # Configurar informações de usuário
    repo = git.Repo(REPO_PATH)
    with repo.config_writer() as git_config:
        git_config.set_value('user', 'name', GIT_USERNAME)
        git_config.set_value('user', 'email', GIT_EMAIL)
    return repo

def remove_lock_file(repo_path):
    lock_file_path = os.path.join(repo_path, '.git', 'index.lock')
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)
        print(f'Removido o arquivo de bloqueio: {lock_file_path}')

def install_pre_commit_hooks(repo_path):
    # Executar o comando para instalar os hooks de pre-commit
    subprocess.run(['pre-commit', 'install'], cwd=repo_path)
    subprocess.run(['pre-commit', 'install-hooks'], cwd=repo_path)

def auto_commit(repo_path):
    import git  # Importação dentro da função para evitar problemas de importação circular
    repo = setup_repo()
    remove_lock_file(repo_path)  # Remover arquivo de bloqueio se existir
    install_pre_commit_hooks(repo_path)  # Instalar hooks de pre-commit
    # Adicionar todos os arquivos modificados ao commit
    repo.git.add(A=True)
    # Verificar se há mudanças a serem commitadas
    if repo.is_dirty(untracked_files=True):
        # Realizar o commit
        repo.index.commit(COMMIT_MESSAGE)
        # Realizar o push para o repositório remoto
        origin = repo.remote(name='origin')
        origin.push()
        print(f'Commit realizado em {datetime.now()}')
    else:
        print('Nenhuma mudança para commit')

def main():
    import git  # Importação dentro da função para evitar problemas de importação circular
    # Verificar se o repositório está clonado
    if not os.path.exists(REPO_PATH):
        # Clonar o repositório se não estiver presente
        git.Repo.clone_from(REPO_URL, REPO_PATH)
    
    auto_commit(REPO_PATH)

if __name__ == '__main__':
    main()
