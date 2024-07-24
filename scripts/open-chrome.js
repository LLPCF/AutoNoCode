// C:\AutoNoCode\scripts\open-chrome.js

import { exec } from 'child_process';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const open = require('open');

// Função para abrir o navegador Chrome
async function openChrome(url) {
    await open(url, { app: { name: 'chrome' } });
}

// Inicia o servidor de desenvolvimento do Vue
const server = exec('npm run serve', { cwd: 'C:\\AutoNoCode\\frontend' });

// Monitora a saída do servidor e abre o navegador quando estiver pronto
server.stdout.on('data', async (data) => {
    console.log(data);
    if (data.includes('App running at')) {
        await openChrome('http://localhost:8080'); // Certifique-se de que a porta está correta
    }
});

server.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});

server.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
});
