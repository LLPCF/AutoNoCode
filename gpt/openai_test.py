import openai
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
dotenv_path = r"C:\AutoNoCode\env\.env"
print(f"Loading .env file from {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)

# Obter a chave da API do OpenAI a partir das variáveis de ambiente
api_key = os.getenv("GPT-PS-KEY")
print(f"API key loaded: {'Yes' if api_key else 'No'}")

if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

openai.api_key = api_key
print(f"API key set successfully: {openai.api_key}")

# Enviar uma solicitação para a API OpenAI usando um modelo disponível
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Substitua pelo modelo disponível listado anteriormente
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Diga que isso é um teste!"}
        ]
    )
    print(response.choices[0].message["content"].strip())
except Exception as e:
    print(f"An error occurred: {e}")
