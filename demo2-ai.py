import Categorias
import nltk
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json
from enum import Enum
import datetime
import random
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
    cat.Categorias.HORA: ["hora", "que hora es", "hora actual"],
    cat.Categorias.DIA: ["hoy es", "qué día es"],
    cat.Categorias.MES: ["qué mes es", "estamos en", "mes"],

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

GREETING_INPUTS = ("hola", "buenos dias", "buenas tardes", "saludos", "qué tal", "hey",)
GREETING_RESPONSES = ["hola", "hey", "*asiente*", "hola, como estas?", "buen dia", "¡Me alegra que estés hablando conmigo!"]

# Initialize tokens
sent_tokens = []
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

def obtener_fecha_hora(tipo):
    if tipo == "hora":
        return datetime.datetime.now().strftime("%H:%M:%S")
    elif tipo == "dia":
        return datetime.datetime.now().strftime("%A")  # Nombre del día
    elif tipo == "mes":
        return datetime.datetime.now().strftime("%B")  # Nombre del mes
    elif tipo == "dia_numero":
        return datetime.datetime.now().strftime("%d")  # Número del día
    elif tipo == "mes_numero":
        return datetime.datetime.now().strftime("%m")  # Número del mes

# Load predefined responses
with open("respuestas.json", "r") as f:
    respuestas_predefinidas = json.load(f)

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
    
    # Verifica palabras clave para día y mes primero
    for categoria, keywords in palabras_clave.items():
        for palabra in keywords:
            if palabra in pregunta:
                categorias_encontradas.add(categoria)

    # Si no se encuentran categorías, busca la más similar
    if not categorias_encontradas:
        for categoria, keywords in palabras_clave.items():
            for keyword in keywords:
                if fuzz.partial_ratio(pregunta, keyword) >= 70:
                    categorias_encontradas.add(categoria)

    if categorias_encontradas:
        categorias_asignadas = ", ".join([categoria.name for categoria in categorias_encontradas])
        print(f"Pregunta asignada a la(s) categoría(s): {categorias_asignadas}")
        return categorias_asignadas
    else:
        print("Pregunta no asignada a ninguna categoría.")
        return "Sin categoria"

# Choose response based on category
# Choose response based on category
def elegir_respuesta_por_categoria(categoria):
    if categoria not in respuestas_predefinidas:
        return "Lo siento, no tengo una respuesta para eso."
    
    respuestas = respuestas_predefinidas[categoria]
    
    if categoria == "HORA":
        # Manejo específico para la categoría HORA
        hora_actual = obtener_fecha_hora("hora")  # Obtener la hora como número
        respuesta_elegida = random.choice(respuestas).format(hora=hora_actual)
        
    elif categoria == "DIA":
        # Manejo específico para la categoría DIA
        dia_actual = obtener_fecha_hora("dia")  # Obtener el nombre del día
        respuesta_elegida = random.choice(respuestas).format(dia=dia_actual)
        
    elif categoria == "MES":
        # Manejo específico para la categoría MES
        mes_actual = obtener_fecha_hora("mes")  # Obtener el nombre del mes
        respuesta_elegida = random.choice(respuestas).format(mes=mes_actual)
        
    else:
        respuesta_elegida = random.choice(respuestas)
    
    return respuesta_elegida

#commit
# Update respuestas.json file with new categories
def update_respuestas_file():
    respuestas_predefinidas_str_keys = {k if isinstance(k, str) else k.name: v for k, v in respuestas_predefinidas.items()}
    with open("respuestas.json", "w") as file:
        json.dump(respuestas_predefinidas_str_keys, file, indent=4)

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
            print(f"Usuario: {entry['Usuario']} | Categoría: {entry['Categoria']}")
    else:
        print("No hay preguntas no entendidas en el log.")

# Main chatbot loop
# Bucle principal del chatbot
flag = True
print("ROBO: Hola, soy un chatbot. Pregúntame algo o escribe 'adios'.")
while flag:
    user_input = input("Usuario: ")
    
    if user_input.lower() == 'adios':
        print("ROBO: ¡Hasta luego!")
        flag = False
    else:
        categoria = categorizar_pregunta(user_input)
        response_text = elegir_respuesta_por_categoria(categoria)
        print("ROBO:", response_text)

        save_conversation(user_input, response_text, successfully, categoria)
