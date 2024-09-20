import Categorias
import nltk
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json
from enum import Enum
import Levenshtein
from fuzzywuzzy import fuzz



cat = Categorias

# Mapeo de palabras clave a categorías
palabras_clave = {
    cat.Categorias.EXISTENCIALES: ["existencia", "vida", "muerte", "sentido"],
    cat.Categorias.EMOCIONALES: ["felicidad", "tristeza", "enojo", "amor", "miedo"],
    cat.Categorias.SOCIALES: ["amistad", "familia", "trabajo", "relaciones"],
    cat.Categorias.FISICAS: ["salud", "ejercicio", "dieta", "enfermedad"],
    cat.Categorias.SEXUALES: ["sexo", "relaciones sexuales", "intimidad"],
    cat.Categorias.ECONOMICAS: ["dinero", "trabajo", "ahorro", "inversion"],
    cat.Categorias.POLITICAS: ["politica", "gobierno", "elecciones", "leyes"],
    cat.Categorias.RELIGIOSAS: ["religion", "dios", "espiritualidad", "fe"],
    cat.Categorias.CULTURALES: ["cultura", "tradiciones", "arte", "musica"],
    cat.Categorias.SALUDOS: ["hola", "buen dia", "buenas tardes", "buenas noches", "adis", "saludos", "como estas"],
    cat.Categorias.SALUDOSCONPREGUNTA: ["como estas", "como te encuentras", "que tal", "como va todo", "como estas hoy"],
}

# Reading the file and converting it to lowercase
with open('chatbot_es.txt', 'r', errors='ignore') as f:
    raw = f.read().lower()

# Tokenizing the text
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Lemmatizer
lemmer = nltk.stem.WordNetLemmatizer()

# Get the Spanish stop words from NLTK
spanish_stop_words = stopwords.words('spanish')

# Greeting inputs and responses in Spanish
GREETING_INPUTS = ("hola", "buenos dias", "buenas tardes", "saludos", "qué tal", "hey",)
GREETING_RESPONSES = ["hola", "hey", "*asiente*", "hola, como estas?", "buen dia", "¡Me alegra que estés hablando conmigo!"]

# Initialize tokens
sent_tokens = [
    'un chatbot (tambien conocido como talkbot, chatterbot, bot, im bot, agente interactivo o entidad conversacional artificial) es un programa de computadora o una inteligencia artificial que lleva a cabo una conversación a través de métodos auditivos o textuales.',
    'tales programas a menudo están diseñados para simular de manera convincente cómo se comportaría un humano como compañero de conversación, pasando así la prueba de Turing.'
]
word_tokens = ['un', 'chatbot', '(', 'tambien', 'conocido']

# Define successfully as a global variable
successfully = True

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

# Load predefined responses
with open("respuestas.json", "r") as f:
    respuestas_predefinidas = json.load(f)

# Function to choose a response based on category
def elegir_respuesta_por_categoria(categoria):
    respuestas = respuestas_predefinidas.get(categoria, ["Lo siento, no tengo una respuesta para eso."])
    return random.choice(respuestas)

# Save conversation log to a JSON file
def save_conversation(user_input, bot_response, successfully, categoria):
    conversation_log = load_conversation_log()
    conversation_log.append({
        "Usuario": user_input, 
        "ROBO": bot_response, 
        "successfully": successfully,
        "Categoria": categoria if isinstance(categoria, str) else categoria.name  # Convertir a string
    }) 
    with open("chat_log.json", "w") as log_file: 
        json.dump(conversation_log, log_file, indent=4)  


# Load conversation log from a JSON file
def load_conversation_log():
    try:
        with open("chat_log.json", "r") as log_file:
            return json.load(log_file)  
    except FileNotFoundError:
        return [] 

# Function to categorize a user input
def categorizar_pregunta(pregunta):
    pregunta = pregunta.lower()
    categorias_encontradas = set()
    
    # Verifica palabras clave primero
    for categoria, keywords in palabras_clave.items():
        for palabra in keywords:
            if palabra in pregunta:
                categorias_encontradas.add(categoria)

    # Si no se encuentran categorías, busca la más similar
    if not categorias_encontradas:
        for categoria, keywords in palabras_clave.items():
            for keyword in keywords:
                if fuzz.partial_ratio(pregunta, keyword) >= 70:  # Se ajusta el umbral
                    categorias_encontradas.add(categoria)

    if categorias_encontradas:
        categorias_asignadas = ", ".join([categoria.name for categoria in categorias_encontradas])
        print(f"Pregunta asignada a la(s) categoría(s): {categorias_asignadas}")
        # Actualiza respuestas
        for categoria in categorias_encontradas:
            categoria_str = categoria.name
            if categoria_str not in respuestas_predefinidas:
                respuestas_predefinidas[categoria_str] = ["Lo siento, no tengo una respuesta para esto."]
        update_respuestas_file()
        return categorias_asignadas
    else:
        print("Pregunta no asignada a ninguna categoría.")
        return "Sin categoria"


    
def son_similares(palabra1, palabra2, umbral=0.5):
    distancia = Levenshtein.distance(palabra1, palabra2)
    longitud_maxima = max(len(palabra1), len(palabra2))
    similitud = 1 - (distancia / longitud_maxima)
    return similitud >= umbral



def encontrar_palabra_similar(pregunta, palabras_clave, umbral=0.5):  # Puedes ajustar el umbral aquí
    for palabra in palabras_clave:
        if son_similares(pregunta, palabra, umbral):
            return palabra
    return None


# Update respuestas.json file with new categories
def update_respuestas_file():
    respuestas_predefinidas_str_keys = {k if isinstance(k, str) else k.name: v for k, v in respuestas_predefinidas.items()}
    with open("respuestas.json", "w") as file:
        json.dump(respuestas_predefinidas_str_keys, file, indent=4)

# Response generation function
# Response generation function
def response(user_response):
    global successfully  
    successfully = True  
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=spanish_stop_words)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if req_tfidf == 0:
        robo_response = "Lo siento! No te entiendo."
        successfully = False  
    else:
        robo_response = sent_tokens[idx]
    sent_tokens.remove(user_response)
    return robo_response


# Function to display unsuccessful conversations with categories
def find_unsuccessful_responses():
    conversation_log = load_conversation_log()
    unsuccessful_responses = [entry for entry in conversation_log if entry.get('successfully') == False]
    
    if unsuccessful_responses:
        print("Las siguientes preguntas no fueron entendidas por el bot y sus categorías asociadas:")
        for entry in unsuccessful_responses:
            categoria = categorizar_pregunta(entry['Usuario'])
            print(f"- Pregunta: {entry['Usuario']}\n  Categoría(s): {categoria}\n")
    else:
        print("No se encontraron preguntas no entendidas por el bot.")

# Main loop
flag = True
print("ROBO: Me llamo Robo. Responderé a tus preguntas sobre los chatbots. Si quieres salir, escribe 'adios'.")
while flag:
    user_response = input()
    user_response = user_response.lower()
    if user_response == 'showme':
        find_unsuccessful_responses()  
    elif user_response != 'adios':
        if user_response in ['gracias', 'muchas gracias']:
            flag = False
            print("ROBO: De nada.")
        else:
            if greeting(user_response) is not None:
                bot_response = greeting(user_response)
                categoria = "SALUDOS"
                print("ROBO: " + bot_response)
                save_conversation(user_response, bot_response, successfully=True, categoria=categoria) 
            else:
                categoria = categorizar_pregunta(user_response)  
                bot_response = elegir_respuesta_por_categoria(categoria)
                print("ROBO: " + bot_response)
                save_conversation(user_response, bot_response, successfully, categoria=categoria)  
    else:
        flag = False
        print("ROBO: Adiós, que tengas un buen día!")
