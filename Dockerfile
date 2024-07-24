# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instala Node.js e npm
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs npm

# Verifica as instalações do Node.js e npm
RUN node -v && npm -v

# Instala @ffmpeg-installer/ffmpeg usando npm
RUN npm install -g @ffmpeg-installer/ffmpeg

# Copia o conteúdo do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Define o comando padrão a ser executado quando o contêiner inicia
CMD ["python", "backend/app/app.py"]
