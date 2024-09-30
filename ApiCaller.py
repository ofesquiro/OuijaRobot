import requests
import json



# Configura tus credenciales
api_key = '10af2bc76516412fac750726fa076f73'
endpoint = 'https://perloo.openai.azure.com/'  # Reemplaza con tu endpoint

# Define la ruta de la API
model = "gpt-4o-mini (version:2024-07-18)" 
api_version = "2023-05-15" 

# Define la URL de la API
url = f"{endpoint}/openai/deployments/{model}/completions?api-version={api_version}"
CONSIGNA : str = "tenes que asumir el rol de un espiritu que fue invocado en una Ouija y tenes que responder las preguntas de los jugadores de forma misteriosa, enigmatica y no muy extensa"

def enviar_request(prompt: str):
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key,
    }
    data = {
        "prompt": prompt,
        "max_tokens": 50,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data  = response.json()
        response_text = response_data.get('choices')[0].get('text')
        print("Respuesta de la API:", response_text)
    else:
        print("Error en la solicitud:", response.status_code, response.text)


def main():
    enviar_request(CONSIGNA)
    while True:
        prompt = input("Ingrese un texto: ")
        if prompt == "exit":
            break
        enviar_request(prompt)

main()
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