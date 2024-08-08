import openai
import os
import pandas as pd
import time
#from dotenv import load_dotenv
key = "false-key" # se reemplaza con la api key correspondiente 
client = openai.Client(key=key)

def get_chat_response(prompt : str, model: str = "text-babbage-001") -> None:
    messages : list[dict[str, str]] = [{"role": "user", "content": prompt}]
    response : any = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=100
    )
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

def main ():
    prompt = "What is the capital of France?"
    get_chat_response(prompt)
main()



