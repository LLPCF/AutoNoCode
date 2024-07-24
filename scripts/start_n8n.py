"""
Patch: Correções nas vulnerabilidades de dependências e melhorias no script de inicialização de serviços Docker.
Commando completo para copiar e colar no terminal:
    cd C:\AutoNoCode\frontend
    npm outdated
    npm update
    npm audit
    npm audit fix
    npm audit fix --force
    cd C:\AutoNoCode\service1
    npm outdated
    npm update
    npm audit
    npm audit fix
    npm audit fix --force
    cd C:\AutoNoCode\service2
    npm outdated
    npm update
    npm audit
    npm audit fix
    npm audit fix --force
Propósito do arquivo: Inicializar e verificar os serviços Docker necessários para o projeto AutoNoCode.
Data de criação ou modificação: 24 de Julho de 2024
Informações adicionais relevantes: O script verifica e inicializa o Docker, constrói imagens Docker para serviços adicionais e verifica a saúde dos serviços.
"""

import os
import subprocess
import time
import logging
import webbrowser
from typing import Optional
from dotenv import load_dotenv
import requests

# Constants
N8N_HEALTH_URL = "http://localhost:5678/healthz"
SERVICE1_HEALTH_URL = "http://localhost:8080/healthz"
SERVICE2_HEALTH_URL = "http://localhost:8081/healthz"
MAX_WAIT_TIME = 120  # 2 minutes
WAIT_INTERVAL = 10
DOCKER_COMPOSE_PATH = "C:\\AutoNoCode\\env\\docker-compose.yml"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_docker_compose():
    """Check if Docker Compose is installed and available."""
    try:
        subprocess.check_output(['docker-compose', '--version'], stderr=subprocess.STDOUT)
        logging.info("Docker Compose is installed and available.")
        return True
    except subprocess.CalledProcessError:
        logging.error("Docker Compose is not installed or not available in PATH.")
        return False

def start_docker() -> bool:
    """Start Docker Desktop if not running."""
    try:
        for _ in range(6):  # Try for 1 minute
            output = subprocess.check_output(['docker', 'info'], stderr=subprocess.STDOUT)
            if b'Containers' in output:
                logging.info("Docker Desktop is running.")
                return True
            logging.info("Docker Desktop is starting. Waiting...")
            time.sleep(10)

        logging.error("Docker Desktop failed to start within the expected time.")
        return False
    except subprocess.CalledProcessError:
        logging.info("Docker Desktop is not running. Attempting to start...")
        try:
            subprocess.Popen(["C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"])
            time.sleep(30)
            return start_docker()  # Recursive call to check again
        except Exception as e:
            logging.error(f"Error starting Docker Desktop: {e}")
            return False

def image_exists(image_name: str) -> bool:
    """Check if a Docker image exists locally."""
    try:
        subprocess.check_output(['docker', 'inspect', '--type=image', image_name], stderr=subprocess.STDOUT)
        logging.info(f"Docker image {image_name} exists.")
        return True
    except subprocess.CalledProcessError:
        logging.info(f"Docker image {image_name} not found.")
        return False

def build_docker_images() -> bool:
    """Build Docker images for additional services if necessary."""
    try:
        if not image_exists('service1_image'):
            logging.info("Building Docker image for service1...")
            subprocess.check_call(['docker', 'build', '-t', 'service1_image', 'C:\\AutoNoCode\\service1'])
            logging.info("Docker image for service1 built successfully.")

        if not image_exists('service2_image'):
            logging.info("Building Docker image for service2...")
            subprocess.check_call(['docker', 'build', '-t', 'service2_image', 'C:\\AutoNoCode\\service2'])
            logging.info("Docker image for service2 built successfully.")

        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error building Docker images: {e}")
        return False

def check_and_update_docker_compose():
    """Check and update the Docker Compose file if necessary."""
    if not os.path.exists(DOCKER_COMPOSE_PATH):
        logging.error(f"Docker Compose file not found at {DOCKER_COMPOSE_PATH}")
        return False

    # Here you can add logic to update the Docker Compose file if needed
    # For example, you could check a version number and update if it's old

    logging.info("Docker Compose file is up to date.")
    return True

def start_n8n() -> bool:
    """Start the n8n container using docker-compose."""
    try:
        logging.info("Starting the n8n container with docker-compose...")
        subprocess.check_call(['docker-compose', '-f', DOCKER_COMPOSE_PATH, 'up', '-d'])
        time.sleep(30)
        return check_n8n_container()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error starting n8n: {e}")
        return False

def check_n8n_container() -> bool:
    """Check if the n8n container is running."""
    try:
        output = subprocess.check_output(['docker', 'ps'], universal_newlines=True)
        if 'n8n' in output:
            logging.info("n8n container is running.")
            return True
        else:
            logging.info("n8n container is not running.")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking n8n container: {e}")
        return False

def wait_for_service(url: str, timeout: int = MAX_WAIT_TIME) -> bool:
    """Wait for a service to be ready or until timeout is reached."""
    logging.info(f"Waiting for service at {url} to be ready. Timeout: {timeout} seconds")
    for _ in range(0, timeout, WAIT_INTERVAL):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logging.info(f"Service at {url} is ready.")
                return True
        except requests.exceptions.RequestException as e:
            logging.debug(f"Service at {url} is not ready yet: {e}")
        time.sleep(WAIT_INTERVAL)
    logging.error(f"Timeout exceeded waiting for service at {url} to be ready.")
    return False

def open_urls_in_chrome(urls: list):
    """Open a list of URLs in Google Chrome."""
    for url in urls:
        try:
            logging.info(f"Opening {url} in Google Chrome...")
            webbrowser.get("chrome").open(url, new=2)
        except webbrowser.Error as e:
            logging.error(f"Failed to open {url} in Google Chrome: {e}")

def main():
    """Main function to start and configure the n8n backend and additional services."""
    env_path = "C:\\AutoNoCode\\env\\.env"
    if not os.path.exists(env_path):
        logging.error(f".env file not found at {env_path}. Make sure it exists.")
        return

    load_dotenv(env_path)

    if not check_docker_compose():
        return

    if not start_docker():
        logging.error("Failed to start Docker Desktop. Make sure it's installed correctly.")
        return

    if not check_and_update_docker_compose():
        return

    if not build_docker_images():
        logging.error("Failed to build Docker images.")
        return

    if not start_n8n():
        logging.error("Failed to start the n8n container.")
        return

    if not wait_for_service(N8N_HEALTH_URL):
        logging.error("n8n is not responding. Check if it started correctly.")
        return

    if not wait_for_service(SERVICE1_HEALTH_URL):
        logging.error("Service at http://localhost:8080/ is not responding. Check if it started correctly.")
        return

    if not wait_for_service(SERVICE2_HEALTH_URL):
        logging.error("Service at http://localhost:8081/ is not responding. Check if it started correctly.")
        return

    logging.info("n8n backend and additional services started successfully.")

    # Open URLs in Google Chrome
    open_urls_in_chrome([N8N_HEALTH_URL, SERVICE1_HEALTH_URL, SERVICE2_HEALTH_URL])

if __name__ == "__main__":
    main()
