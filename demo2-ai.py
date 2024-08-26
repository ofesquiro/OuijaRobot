
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json
import os
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
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
    if os.path.exists("chat_log.json"):
        with open("chat_log.json", "r") as log_file:
            return json.load(log_file)
    else:
        return []


LOG = load_conversation_log()

def train():
    X = [entry['user'] for entry in LOG]
    y = [entry['bot'] for entry in LOG]

    # Vectorizar las preguntas usando TF-IDF
    vectorizer = TfidfVectorizer()
    X_vect = vectorizer.fit_transform(X)

    # Entrenar el clasificador KNN
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(X_vect, y)


# Response generation function
def response(user_response):
    log = load_conversation_log()
    user_responses = [line["user"] for line in log]
    bot_responses = [line["bot"] for line in log]
    train()
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
    if sims.max() < 0.5:
        bot_response = "Lo siento, no entiendo. Puedes reformular la pregunta?"
        successful = False
        save_bad_response(user_response, bot_response)  # Save the bad response
    else:
        idx = sims.argsort()[0][-1]
        bot_response = bot_responses[idx]
        successful = True

    # Guardar la conversación
    save_conversation(user_response, bot_response, successful)

    return bot_response

flag = True
print("ROBO: Me llamo Robo. Responderé a tus preguntas sobre los chatbots. Si quieres salir, escribe 'adiós'.")

while flag:
    user_response = input().lower()
    if user_response != 'adiós':
        if user_response in ('gracias', 'muchas gracias'):
            flag = False
            print("ROBO: De nada.")
        else:
            if greeting(user_response) is not None:
                bot_response = greeting(user_response)
                print("ROBO: " + bot_response)
                save_conversation(user_response, bot_response, True)  # Save the conversation
            else:
                bot_response = response(user_response)
                if bot_response == "Lo siento, no entiendo. Puedes reformular la pregunta?":
                    print("ROBO: " + bot_response)
                    print("ROBO: No entiendo la pregunta. Por favor, reformúlala.")
                else:
                    print("ROBO: " + bot_response)
    else:
        flag = False
        print("ROBO: ¡Adiós! Cuídate.")
