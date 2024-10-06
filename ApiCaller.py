
from requests import Response, RequestException, post
import re
from voiceParsing import run as run_microphone
from Api.Comparison import compare, Options
from comunicacionArduino.OuijaSender import send_string_to_raspberry
from asyncio import run as async_run 
# Configuration
API_KEY = "a133234471fa4fa8b2fae8a13f06310d"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}
ENDPOINT = "https://perloooo.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-15-preview"




def set_up() -> None:
    payload = {
    "messages": [
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "Sos un espiritu que fue invocado por el usuario a traves de una ouija y tenes que responder a unas preguntas que te haga."
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "hola"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "hola"
            }
        ]
        },
        {
        "role": "assistant",
        "content": [
            {
            "type": "text",
            "text": "Diga..."
            }
        ]
        }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800
    }
    try:
        response = post(ENDPOINT, headers=headers, json=payload)
        
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    return response.json()


def build_response(bytes : bytes) -> str:
    alternatives : dict[Options, str] = compare(bytes)
    string_list : list[str] = []
    for key, value in alternatives.items():
        string_list.append(value)
        
    return string_list
    
    
def from_json_to_string(json_str: bytes | None) -> str:
    try:
        pattern: str = r'"message":\{"content":"(.*?)","role":"(.*?)"\}'
        latin_version = json_str.decode('ISO-8859-1')
        optionLists : list[str] = build_response(json_str)
        print(optionLists)
        match = re.search(pattern, latin_version)
        content: str = ""
        if match:
            content = match.group(1)

        return content
    except Exception as e:
        print(e)
        return "No se pudo obtener la respuesta"
    
    
def make_question(prompt : str) -> Response:
    localpayload ={
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }
    try:
        res :Response = post(ENDPOINT, headers=headers, json=localpayload)
        res.raise_for_status()
    except RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    
    return res



async def run():
    set_up()
    while(True):
        prompt : str = await run_microphone()
        if prompt == "adios":
            break
        res : Response = make_question(prompt)
        json_res : bytes | None = res._content 
        final_response = from_json_to_string(json_res)
        send_string_to_raspberry(final_response)
        print("Bot: ",final_response)
        print("-------------------------------------------------")
        
        
async_run(run())




"""
modelo de respuesta
{
    'choices': 
        [
            {'content_filter_results': 
                {
                    'hate': {'filtered': False, 'severity': 'safe'},
                    'protected_material_code': {'filtered': False, 'detected': False}, 
                    'protected_material_text': {'filtered': False, 'detected': False}, 
                    'self_harm': {'filtered': False, 'severity': 'safe'}, 
                    'sexual': {'filtered': False, 'severity': 'safe'}, 
                    'violence': {'filtered': False, 'severity': 'safe'}}, 
                'finish_reason': 'stop', 
                'index': 0, 
                'logprobs': None, 
                'message': {'content': '▒Hola! ▒C▒mo puedo ayudarte hoy?', 'role': 'assistant'}
                }
            ], 
        'created': 1727812807, 
        'id': 'chatcmpl-ADdKRVVEF4daiN99LFbglFB8PXJBc', 
        'model': 'gpt-4o-mini', 
        'object': 'chat.completion', 
        'prompt_filter_results': [
            {'prompt_index': 0, 
             'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 
                                        'jailbreak': {'filtered': False, 'detected': False}, 
                                        'self_harm': {'filtered': False, 'severity': 'safe'},
                                        'sexual': {'filtered': False, 'severity': 'safe'}, 
                                        'violence': {'filtered': False, 'severity': 'safe'}}
             }
        ],
        'system_fingerprint': 'fp_878413d04d', 
        'usage': {'completion_tokens': 9, 'prompt_tokens': 8, 'total_tokens': 17}
}


def display_object_attributes(obj):
    attributes = dir(obj)
    # Filter out attributes that start with '__'
    non_special_attributes = [attr for attr in attributes if not attr.startswith('__')]
    
    for attr in non_special_attributes:
        try:
            # Use getattr to get the value of the attribute
            value = getattr(obj, attr)
            print(f"{attr}: {value}")
        except AttributeError:
            print(f"{attr}: (could not retrieve value)")



"""