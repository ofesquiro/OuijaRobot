import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json

# Ensure the NLTK stopwords package is downloaded
nltk.download('punkt')  # first-time use only
nltk.download('wordnet')  # first-time use only
nltk.download('stopwords')  # first-time use only


# Reading the file and converting it to lowercase
f = open('chatbot_es.txt', 'r', errors='ignore')  # Make sure this file contains Spanish text
raw = f.read()
raw = raw.lower()

# Tokenizing the text
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

# Lemmatizer
lemmer = nltk.stem.WordNetLemmatizer()

# Get the Spanish stop words from NLTK
spanish_stop_words = stopwords.words('spanish')

# Greeting inputs and responses in Spanish
GREETING_INPUTS = ("hola", "buenos dias", "buenas tardes", "saludos", "que tal", "hey",)
GREETING_RESPONSES = ["hola", "hey", "*asiente*", "hola, como estas?", "buen dia", "Me alegra que estes hablando conmigo!"]

# Initialize tokens (make sure these are reset for the example data)
sent_tokens = [
    'un chatbot (también conocido como talkbot, chatterbot, bot, im bot, agente interactivo o entidad conversacional artificial) es un programa de computadora o una inteligencia artificial que lleva a cabo una conversación a través de métodos auditivos o textuales.',
    'tales programas a menudo están diseñados para simular de manera convincente cómo se comportaría un humano como compañero de conversación, pasando así la prueba de Turing.'
]
word_tokens = ['un', 'chatbot', '(', 'también', 'conocido']

# Greeting function
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Lemmatization functions
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation + '¿¡')

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Save conversation log to a file
def save_conversation(user_input, bot_response, successful):
    conversation_log = load_conversation_log()
    conversation_log.append({"user": user_input, "bot": bot_response, "successful": successful})
    with open("chat_log.json", "w") as log_file:
        json.dump(conversation_log, log_file, indent=4)
    

def load_conversation_log():
    try:
        with open("chat_log.json", "r") as log_file:
            return json.load(log_file)
    except FileNotFoundError:
        return []

# Response generation function
def response(user_response):
    log = load_conversation_log()
    user_responses = [line for line in log if line.startswith("Usuario: ")]
    bot_responses = [line for line in log if line.startswith("ROBO: ")]

    # Tokenizar las respuestas del usuario y del bot
    user_tokens = [nltk.word_tokenize(line[8:]) for line in user_responses]
    bot_tokens = [nltk.word_tokenize(line[6:]) for line in bot_responses]

    # Crear un vector de características para cada respuesta del usuario y del bot
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=spanish_stop_words)
    user_tfidf = TfidfVec.fit_transform([" ".join(tokens) for tokens in user_tokens])
    bot_tfidf = TfidfVec.transform([" ".join(tokens) for tokens in bot_tokens])

    # Calcular la similitud entre la respuesta del usuario y las respuestas del bot
    sims = cosine_similarity(user_tfidf[-1], bot_tfidf)

    # Seleccionar la respuesta del bot más similar
    idx = sims.argsort()[0][-1]
    bot_response = bot_responses[idx][6:]

    # Verificar si el chatbot puede responder a la pregunta
    if sims.max() < 0.5:
        bot_response = "Lo siento, no entiendo. Puedes reformular la pregunta?"
        successful = False
    else:
        successful = True

    # Guardar la conversación
    save_conversation(user_response, bot_response, successful)

    return bot_response

def chat():
    flag = True
    print("ROBO: Me llamo Robo. Responderé a tus preguntas sobre los chatbots. Si quieres salir, escribe 'adiós'.")
    while(flag == True):
        user_response = input()
        user_response = user_response.lower()
        if(user_response != 'adiós'):
            if(user_response == 'gracias' or user_response == 'muchas gracias'):
                flag = False
                print("ROBO: De nada.")
            else:
                if(greeting(user_response) != None):
                    bot_response = greeting(user_response)
                    print("ROBO: " + bot_response)
                    save_conversation(user_response, bot_response, flag)  # Save the conversation
                else:
                    print("lo siento, tengo down y no puedo responder a eso")
                    save_conversation(user_response, "" + "lo siento, tengo down y no puedo responder a eso", flag == False)  # Save the conversation
                    return flag     

def save_BadResponse(user_input, bot_response):
    conversation_log = load_conversation_log()
    conversation_log.append({"user": user_input, "bot": bot_response, "successful": False})
    with open("bad_response_log.json", "w") as log_file:
        json.dump(conversation_log, log_file, indent=4)
    

def load_BadResponse_log():
    try:
        with open("bad_response_log.json", "r") as log_file:
            return json.load(log_file)
    except FileNotFoundError:
        return []
    

def main():
    chat()
    bad_response_log = load_BadResponse_log()
main()