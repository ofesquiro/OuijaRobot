
import requests
from Response import Response as Res
from typing import List
import json
from Choice import Choice
from Content_filer_result import ContentFilterResults
from Prompt_filter_result import PromptFilterResults
from Filter_results import FilterResults
from Message import Message
from Usage import Usage
import re
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
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    return response.json()
def from_json(json_str: str) -> Res:
    try:
        pattern: str = r'"message":\{"content":"(.*?)","role":"(.*?)"\}'
        s = json_str.decode('ISO-8859-1')
        match = re.search(pattern, s)
        content: str = ""
        if match:
            content = match.group(1)

        data = json.loads(json_str)

        # Parse choices
        choices = []
        for choice_data in data['choices']:
            cfr = ContentFilterResults(
                hate=FilterResults(**choice_data['content_filter_results']['hate']),
                protected_material_code=FilterResults(**choice_data['content_filter_results'].get('protected_material_code', {'filtered': False, 'detected': False})),
                protected_material_text=FilterResults(**choice_data['content_filter_results'].get('protected_material_text', {'filtered': False, 'detected': False})),
                self_harm=FilterResults(**choice_data['content_filter_results']['self_harm']),
                sexual=FilterResults(**choice_data['content_filter_results']['sexual']),
                violence=FilterResults(**choice_data['content_filter_results']['violence']),
            )
            choice = Choice(
                content_filter_results=cfr,
                finish_reason=choice_data['finish_reason'],
                index=choice_data['index'],
                logprobs=choice_data['logprobs'],
                message=content
            )
            choices.append(choice)

        # Parse prompt_filter_results
        prompt_filter_results = []
        for pfr_data in data['prompt_filter_results']:
            cfr = ContentFilterResults(
                hate=FilterResults(**pfr_data['content_filter_results']['hate']),
                protected_material_code=FilterResults(**pfr_data['content_filter_results'].get('protected_material_code', {'filtered': False, 'detected': False})),
                protected_material_text=FilterResults(**pfr_data['content_filter_results'].get('protected_material_text', {'filtered': False, 'detected': False})),
                self_harm=FilterResults(**pfr_data['content_filter_results']['self_harm']),
                sexual=FilterResults(**pfr_data['content_filter_results']['sexual']),
                violence=FilterResults(**pfr_data['content_filter_results']['violence']),
            )
            pfr = PromptFilterResults(
                prompt_index=pfr_data['prompt_index'],
                content_filter_results=cfr
            )
            prompt_filter_results.append(pfr)

        usage = Usage(**data['usage'])

    except Exception as e:
        raise ValueError(f"Failed to parse JSON. Error: {e}")

    return Res(
        choices=choices,
        created=data['created'],
        response_id=data['id'],
        model=data['model'],
        object_type=data['object'],
        prompt_filter_results=prompt_filter_results,
        system_fingerprint=data['system_fingerprint'],
        usage=usage
    )

def make_question(prompt : str) -> requests.Response:
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
        res : requests.Response = requests.post(ENDPOINT, headers=headers, json=localpayload)
        res.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    
    return res



def main():
    set_up()
    while(True):
        prompt : str = input("Ingrese una pregunta: ")
        if prompt == "adios":
            break
        res : requests.Response = make_question(prompt)
        json_res = res._content 
        casted_res = from_json(json_res)
        final_response = casted_res.choices[0].message
        print(final_response)
        
        

            
main()




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