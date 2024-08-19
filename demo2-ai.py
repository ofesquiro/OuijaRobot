import nltk
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json
import collections from Counter
# Ensure the NLTK resources are downloaded
nltk.download('punkt')  # For tokenization
nltk.download('wordnet')  # For lemmatization
nltk.download('stopwords')  # For stopwords

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

# Save conversation log to a file


def save_conversation(user_input, bot_response, successful):
    conversation_log = load_conversation_log()
    conversation_log.append({"user": user_input, "bot": bot_response, "successful": successful})
    with open("chat_log.json", "w") as log_file:
        json.dump(conversation_log, log_file, indent=4)
    



# Response generation function
def response(user_response):
    log = load_conversation_log()
    user_responses = [line["user"] for line in log]
    bot_responses = [line["bot"] for line in log]
    # Tokenizar las respuestas del usuario y del bot
    user_tokens = [nltk.word_tokenize(line) for line in user_responses]
    bot_tokens = [nltk.word_tokenize(line) for line in bot_responses]
    # Crear un vector de características para cada respuesta del usuario y del bot
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=spanish_stop_words)
    user_tfidf = TfidfVec.fit_transform([" ".join(tokens) for tokens in user_tokens])
    bot_tfidf = TfidfVec.transform([" ".join(tokens) for tokens in bot_tokens])
    # Calcular la similitud entre la respuesta del usuario y las respuestas del bot
    sims = cosine_similarity(user_tfidf[-1], bot_tfidf)
    # Seleccionar la respuesta del bot más similar
    idx = sims.argsort()[0][-1]
    bot_response = bot_responses[idx]
    # Verificar si el chatbot puede responder a la pregunta
    if sims.max() < 0.5:
        bot_response = "Lo siento, no entiendo. Puedes reformular la pregunta?"
        successful = False
    else:
        successful = True
    # Guardar la conversación
    save_conversation(user_response, bot_response, successful)
    return bot_response


def analyze_response():
    conversation_log : any | list = load_conversation_log()
    for line in conversation_log:
        print(line["user"])
        print(line["bot"])
        print(line["successful"])
        print()


def chat():
    flag = True
    print("ROBO: Me llamo Robo. Responderé a tus preguntas sobre los chatbots. Si quieres salir, escribe 'adiós'.")
    while flag:
        user_response = input()
        user_response = user_response.lower()
        if user_response != 'adiós':
            if user_response in ['gracias', 'muchas gracias']:
                flag = False
                print("ROBO: De nada.")
            else:
                if greeting(user_response) is not None:
                    bot_response = greeting(user_response)
                    print("ROBO: " + bot_response)
                    save_conversation(user_response, bot_response, True)  # Save the conversation
                else:
                    bot_response = "Lo siento, no puedo responder a eso."
                    print("ROBO: " + bot_response)
                    save_conversation(user_response, bot_response, False)  # Save the conversation  


def main():
    chat()


main()
