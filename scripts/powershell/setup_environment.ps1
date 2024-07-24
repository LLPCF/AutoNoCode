# Patch C:\AutoNoCode\scripts\powershell\setup_environment.ps1
# Date: 2024-07-02
# Root project folder: C:\AutoNoCode

# Patch Details:
# This script is designed to set up the Python virtual environment for the AutoNoCode project.
# It performs the following steps:
# 1. Removes any existing virtual environment.
# 2. Checks the project structure.
# 3. Creates a new virtual environment.
# 4. Activates the new virtual environment.
# 5. Upgrades pip to the latest version.
# 6. Installs project dependencies from requirements.txt.
# 7. Runs the maintenance script.

# Changes in this patch:
# - Added try-catch blocks to handle potential errors gracefully.
# - Improved output messages for better clarity.
# - Ensured the script stops execution if critical steps fail.

# Remover o ambiente virtual existente, se houver
if (Test-Path -Path .\env) {
    try {
        Remove-Item -Recurse -Force .\env
        Write-Output "Existing virtual environment removed."
    } catch {
        Write-Output "Failed to remove existing virtual environment. Please try manually."
        Exit
    }
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
if (Test-Path -Path .\env\Scripts\Activate.ps1) {
    try {
        & .\env\Scripts\Activate.ps1
        Write-Output "Virtual environment activated."
    } catch {
        Write-Output "Failed to activate virtual environment."
        Exit
    }
} else {
    Write-Output "Activation script not found. Please check if the virtual environment was created correctly."
    Exit
}

# Atualizar pip
Write-Output "Upgrading pip..."
try {
    python -m pip install --upgrade pip
    Write-Output "pip upgraded successfully."
} catch {
    Write-Output "Failed to upgrade pip."
    Exit
}

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
try {
    python .\scripts\maintenance.py
    Write-Output "Maintenance script executed successfully."
} catch {
    Write-Output "Failed to execute maintenance script."
    Exit
}

Write-Output "Environment setup complete."
