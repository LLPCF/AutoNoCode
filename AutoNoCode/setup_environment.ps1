# setup_environment.ps1
# Filename: setup_environment.ps1
# Date: 2024-07-02
# Root project folder: C:\AutoNoCode

# Remover o ambiente virtual existente, se houver
if (Test-Path -Path .\env) {
    Remove-Item -Recurse -Force .\env
    Write-Output "Existing virtual environment removed."
}

# Verificar a estrutura do projeto
Write-Output "Checking project structure..."
python .\check_structure.py

# Criar um novo ambiente virtual
Write-Output "Creating virtual environment..."
python -m venv env
Write-Output "Virtual environment created successfully."

# Ativar o ambiente virtual
Write-Output "Activating virtual environment..."
.\env\Scripts\Activate.ps1
Write-Output "Virtual environment activated."

# Atualizar pip
Write-Output "Upgrading pip..."
python -m pip install --upgrade pip
Write-Output "pip upgraded successfully."

# Instalar as dependências a partir do requirements.txt
Write-Output "Installing requirements..."
try {
    python -m pip install -r requirements.txt
    Write-Output "Requirements installed successfully."
} catch {
    Write-Output "Failed to install requirements."
    Exit
}

# Executar o script de manutenção
Write-Output "Running maintenance script..."
python .\scripts\maintenance.py

Write-Output "Maintenance script executed successfully."
Write-Output "Environment setup complete."
