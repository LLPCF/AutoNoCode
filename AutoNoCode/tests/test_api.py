import requests

try:
    response = requests.post('http://localhost:5000/api/run-automation')
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Erro ao conectar à API: {e}")
