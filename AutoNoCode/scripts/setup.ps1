# filename: setup.ps1
# date: 2024-06-30
# root project folder: C:\AutoNoCode

# Declaração de diretórios
$directories = @(
    'backend\app',
    'backend\tests',
    'frontend\src\components',
    'frontend\src\views',
    'n8n\workflows',
    'docs',
    'backend\app\services',
    'backend\app\controllers'
)

# Criar diretórios se não existirem
foreach ($dir in $directories) {
    if (-Not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
    }
}

# Declaração de arquivos e seus conteúdos
$filesContent = @{
    'backend\app\main.py' = @"
from fastapi import FastAPI, Depends, WebSocket
from fastapi_users import FastAPIUsers, models
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from app.controllers import (
    video_controller,
    admin_controller,
    stats_controller,
    upload_controller
)

DATABASE_URL = 'sqlite:///./test.db'

Base: DeclarativeMeta = declarative_base()

class User(models.BaseUser, Base):
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
user_db = SQLAlchemyUserDatabase(User, SessionLocal())

fastapi_users = FastAPIUsers(
    user_db,
    [models.UserDB, models.UserCreate, models.UserUpdate],
    models.BaseOAuthAccount,
)

app = FastAPI()

@app.on_event('startup')
async def on_startup():
    await fastapi_users.create_db_and_tables()

app.include_router(
    fastapi_users.get_register_router(),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_auth_router(),
    prefix='/auth/jwt',
    tags=['auth'],
)

app.include_router(video_controller.router, prefix='/videos', tags=['videos'])
app.include_router(admin_controller.router, prefix='/admin', tags=['admin'])
app.include_router(stats_controller.router, prefix='/stats', tags=['stats'])
app.include_router(upload_controller.router, prefix='/upload', tags=['upload'])

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message received: {data}')
"@

    'backend\app\models.py' = ""
    'backend\app\schemas.py' = ""
    'backend\app\services\__init__.py' = ""
    'backend\app\controllers\__init__.py' = ""
    'backend\tests\__init__.py' = ""
    'frontend\src\App.vue' = @"
<template>
  <router-view />
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* Adicione seu estilo aqui */
</style>
"@
    'frontend\src\main.js' = @"
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

createApp(App).use(store).use(router).mount('#app');
"@
    'frontend\package.json' = @"
{
  'name': 'autonocode-frontend',
  'version': '1.0.0',
  'private': true,
  'scripts': {
    'serve': 'vue-cli-service serve',
    'build': 'vue-cli-service build',
    'lint': 'vue-cli-service lint'
  },
  'dependencies': {
    'axios': '^0.21.1',
    'core-js': '^3.6.5',
    'vue': '^3.0.0',
    'vue-router': '^4.0.0',
    'vuex': '^4.0.0'
  },
  'devDependencies': {
    '@vue/cli-plugin-babel': '~4.5.0',
    '@vue/cli-service': '~4.5.0',
    'babel-eslint': '^10.1.0',
    'eslint': '^6.7.2',
    'eslint-plugin-vue': '^7.0.0'
  }
}
"@
    'frontend\Dockerfile' = @"
FROM node:14-alpine

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install

COPY . .

RUN yarn build

EXPOSE 80

CMD ['yarn', 'serve']
"@
    'n8n\Dockerfile' = @"
FROM n8nio/n8n

WORKDIR /home/node/.n8n

COPY data /home/node/.n8n
"@
    'docker-compose.yml' = @"
version: '3.8'

services:
  n8n:
    container_name: n8n
    image: n8nio/n8n
    restart: always
    ports:
      - '5678:5678'
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin
      - N8N_HOST=n8n
      - N8N_PORT=5678
    volumes:
      - ./n8n/data:/home/node/.n8n
      - ./n8n/workflows:/home/node/.n8n/workflows

  backend:
    build: ./backend
    restart: always
    ports:
      - '8000:8000'
    volumes:
      - ./backend/app:/app
    environment:
      - N8N_API_URL=http://n8n:5678

  frontend:
    build: ./frontend
    restart: always
    ports:
      - '8080:80'
    volumes:
      - ./frontend:/app
"@
    'Makefile' = @"
.PHONY: init migrate run-backend run-frontend test-backend docker-build docker-up docker-down

init:
    python -m venv venv
    source venv/bin/activate
    pip install -r backend/app/requirements.txt
    cd frontend
    yarn install

migrate:
    alembic upgrade head

run-backend:
    uvicorn backend.app.main:app --reload

run-frontend:
    cd frontend
    yarn serve

test-backend:
    pytest backend/tests

docker-build:
    docker-compose build

docker-up:
    docker-compose up

docker-down:
    docker-compose down
"@
    'README.md' = @"
# AutoNoCode

## Visão Geral
AutoNoCode é uma plataforma para gerar vídeos automaticamente usando técnicas avançadas de IA.

## Requisitos

- Docker
- Docker Compose
- Python 3.9+
- Node.js 14+
- PostgreSQL

## Configuração do Ambiente de Desenvolvimento

### Backend

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/AutoNoCode.git
    cd AutoNoCode
    ```

2. Configure e ative o ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Instale as dependências do backend:
    ```bash
    pip install -r backend/app/requirements.txt
    ```

4. Configure o banco de dados:
    ```bash
    docker-compose up -d db
    alembic upgrade head
    ```

5. Inicie o servidor backend:
    ```bash
    uvicorn backend.app.main:app --reload
    ```

### Frontend

1. Instale as dependências do frontend:
    ```bash
    cd frontend
    yarn install
    ```

2. Inicie o servidor frontend:
    ```bash
    yarn serve
    ```

### Executando com Docker Compose

1. Construa e inicie todos os serviços:
    ```bash
    docker-compose up --build
    ```

## Testes

### Backend

1. Execute os testes:
    ```bash
    pytest backend/tests
    ```

## Contribuição

1. Fork o repositório.
2. Crie uma nova branch: `git checkout -b minha-nova-funcionalidade`.
3. Faça suas alterações e commite-as: `git commit -m 'Adicionar nova funcionalidade'`.
4. Envie para a branch original: `git push origin minha-nova-funcionalidade`.
5. Crie um pull request.
"@
    'backend\requirements.txt' = @"
fastapi
uvicorn
sqlalchemy
psycopg2
fastapi-users
requests
pytest
"@
}

# Criar arquivos e adicionar conteúdo
foreach ($file in $filesContent.Keys) {
    $content = $filesContent[$file]
    Set-Content -Path $file -Value $content -Force
}

# Salvar o script setup na pasta scripts
$setupScriptPath = "scripts\setup.ps1"
Set-Content -Path $setupScriptPath -Value $setupScript -Force
