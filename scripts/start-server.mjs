// start-server.mjs

import { exec } from 'child_process';
import { fileURLToPath } from 'url';
import path from 'path';

// Converte a URL do módulo em um caminho de arquivo
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Função para iniciar o servidor
function startServer() {
    console.log('Iniciando o servidor...');

    // Definindo o caminho do diretório do projeto
    const projectDir = path.resolve(__dirname, '..');

    // Comando para iniciar o servidor com o PYTHONPATH
    const command = `set PYTHONPATH=${projectDir} && uvicorn backend.app.main:app --reload`;

    // Executando o comando
    const serverProcess = exec(command, { shell: true });

    // Adicionando logs adicionais para verificar a execução
    serverProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    serverProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    serverProcess.on('error', (err) => {
        console.error(`Erro ao iniciar o servidor: ${err.message}`);
    });

    serverProcess.on('close', (code) => {
        console.log(`Processo de servidor encerrado com código ${code}`);
    });
}

// Iniciando o servidor
startServer();
