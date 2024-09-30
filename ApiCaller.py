import requests
import json

class Usage():
    prompt_tokens : int
    completion_tokens : int
    total_tokens : int


class Choices():
    text : str
    usage : Usage

class ResponseStruct():
    id: str
    object: str
    created: int
    model: str
    choices: dict[Choices]

# Configura tus credenciales
api_key = '88027e88e840432a9a4a4dd479076cae'
endpoint = 'https://lapo.openai.azure.com/'  # Reemplaza con tu endpoint

# Define la ruta de la API
model = "gpt-" # o el modelo que estés usando
api_version = "2023-05-15"  # Verifica la versión más reciente en la documentación

# Define la URL de la API
url = f"{endpoint}/openai/deployments/{model}/completions?api-version={api_version}"

# Configura los encabezados
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key,
}
mensaje_inicial : str = "Que hora es"
# Cuerpo de la solicitud
data = {
    "prompt": mensaje_inicial,
    "max_tokens": 50,
}

# Realiza la solicitud
response = requests.post(url, headers=headers, json=data)

# Procesa la respuesta
if response.status_code == 200:
    response_data : ResponseStruct = response.json()
    print("Respuesta de la API:", response_data)
else:
    print("Error en la solicitud:", response.status_code, response.text)


"""
formato de respuesta 

Respuesta de la API: {
    'id': 'cmpl-ADCLkcDhXG9gtlTEC949L66H7drG9', 
    'object': 'text_completion', 
    'created': 1727709100, 
    'model': 'gpt-35-turbo', 
    'choices': [
        {
            'text': '', 'index': 0, 'finish_reason': 'length', 'logprobs': None}],
          'usage': {'prompt_tokens': 106, 'completion_tokens': 50, 'total_tokens': 156}
        }
    ]

"""