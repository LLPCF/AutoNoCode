import openai
import subprocess
import os
from dotenv import load_dotenv

# Caminho absoluto para o arquivo .env
dotenv_path = os.path.join('C:\\AutoNoCode\\env', '.env')

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path)

# Obter a chave da API do OpenAI a partir das variáveis de ambiente
openai.api_key = os.getenv('GPT-PS-KEY')

def executar_comando_powershell(comando):
    try:
        resultado = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)
        return resultado.stdout
    except Exception as e:
        return str(e)

def obter_resposta_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return str(e)

def main():
    while True:
        user_input = input("Digite sua solicitação para o GPT: ")
        if user_input.lower() in ["sair", "exit"]:
            break

        resposta_gpt = obter_resposta_gpt(user_input)
        print(f"GPT: {resposta_gpt}")

        if "powershell" in user_input.lower() or "PowerShell" in resposta_gpt:
            comando_powershell = resposta_gpt
            resultado = executar_comando_powershell(comando_powershell)
            print(f"Resultado do PowerShell: {resultado}")

if __name__ == "__main__":
    main()
