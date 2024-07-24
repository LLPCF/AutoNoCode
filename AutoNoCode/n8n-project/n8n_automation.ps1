# Carregar variáveis de ambiente do arquivo .env
$envFilePath = "C:/AutoNoCode/env/.env"
if (Test-Path $envFilePath) {
    Get-Content $envFilePath | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

# Verificar se a chave da API está carregada
$apiKey = [System.Environment]::GetEnvironmentVariable('N8N_API_KEY')
if (-not $apiKey) {
    Write-Error "Chave da API do n8n não encontrada. Certifique-se de que 'N8N_API_KEY' está definido no arquivo .env."
    Exit
}

# URL da API do n8n
$apiUrl = "http://localhost:5678/api/v1"

# Executar o workflow
try {
    Invoke-RestMethod -Uri "$apiUrl/workflows" -Headers @{
        "X-N8N-API-KEY" = $apiKey
        "Content-Type" = "application/json"
    } -Method Post -Body (Get-Content -Raw -Path "C:\AutoNoCode\n8n-workflows\auto_git_workflow.json")
    Write-Output "Workflow executado com sucesso."
} catch {
    Write-Error "Erro ao executar o workflow: $_"
}
