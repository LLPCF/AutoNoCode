# Caminho para o repositório local
$repositoryPath = "C:\AutoNoCode"

# Mensagem de commit
$commitMessage = "Seu commit message"

# Navegar para o diretório do repositório
Set-Location -Path $repositoryPath

# Configurar usuário Git (Substitua com seu nome e e-mail)
git config user.name "Seu Nome"
git config user.email "seuemail@example.com"

# Adicionar arquivos ao staging
git add .

# Realizar o commit
git commit -m $commitMessage

# Fazer o push das mudanças para o repositório remoto
git push
