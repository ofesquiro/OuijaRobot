import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

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
GREETING_INPUTS = ("hola", "buenos días", "buenas tardes", "saludos", "qué tal", "hey",)
GREETING_RESPONSES = ["hola", "hey", "*asiente*", "hola, ¿cómo estás?", "buen día", "¡Me alegra que estés hablando conmigo!"]

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

# Response generation function
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=spanish_stop_words)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf == 0):
        robo_response = robo_response + "¡Lo siento! No te entiendo."
    else:
        robo_response = robo_response + sent_tokens[idx]
    sent_tokens.remove(user_response)
    return robo_response

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
                print("ROBO: " + greeting(user_response))
            else:
                print("ROBO: ", end="")
                print(response(user_response))
    else:
        flag = False
        print("ROBO: ¡Adiós! Cuídate.")
