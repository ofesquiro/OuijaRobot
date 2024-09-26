import Categorias as c
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json
import datetime
import random
from fuzzywuzzy import fuzz
import pygame
import nltk
# nltk.download('punkt')
palabras_clave = {
    c.Categorias.EXISTENCIALES: ["existencia", "vida", "muerte", "sentido", "morir","despues de la muerte"],
    c.Categorias.EMOCIONALES: ["felicidad", "tristeza", "enojo", "amor", "miedo"],
    c.Categorias.SOCIALES: ["amistad", "familia", "trabajo", "relaciones"],
    c.Categorias.FISICAS: ["salud", "ejercicio", "dieta", "enfermedad"],
    c.Categorias.ECONOMICAS: ["dinero", "trabajo", "ahorro", "inversion"],
    c.Categorias.POLITICAS: ["politica", "gobierno", "elecciones", "leyes"],
    c.Categorias.RELIGIOSAS: ["religion", "dios", "espiritualidad", "fe"],
    c.Categorias.CULTURALES: ["cultura", "tradiciones", "arte", "musica"],
    c.Categorias.SALUDOS: ["hola", "buen dia", "buenas tardes", "buenas noches", "adios", "saludos", "Hola", "Saludos", "Buen dia", "Holi", "Holo"],
    c.Categorias.SALUDOSCONPREGUNTA: ["como estas", "como te encuentras", "que tal", "como va todo", "como estas hoy", "Como estas?", "Hola como estas", "Como andas", "Saludos Como te va", "Como anda todo", "Hola que contas"],
    c.Categorias.HORA: ["hora", "que hora es", "hora actual"],
    c.Categorias.DIA: ["hoy es", "qué día es"],
    c.Categorias.MES: ["qué mes es", "estamos en", "mes"],
    c.Categorias.PREPREGUNTA: ["tengo una pregunta", "una pregunta", "consulta"],
    c.Categorias.ERROR: ["pregunta no entendida", "no entendiste", "no comprendes", "dijiste cualquiera", "no entendi", "mi pregunta", "esta mal"]
}
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
def save_conversation(user_input : str, bot_response : str, successfully : bool, categoria : c.Categorias):
    conversation_log = load_conversation_log()
    conversation_log.append({
        "Usuario": user_input, 
        "ROBO": bot_response, 
        "successfully": successfully,
        "categoria": str(categoria)  # Convertir a string
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

# Function to cegorize a user input
def categorizar_pregunta(pregunta : str) -> set[c.Categorias]:
    pregunta = pregunta.lower()
    categorias_encontradas = set()
    
    # Verifica palabras clave para día y mes primero
    for categoria, keywords in palabras_clave.items():
        for palabra in keywords:
            if palabra in pregunta:
                categorias_encontradas.add(categoria)

    # Si no se encuentran categorías, busca la más similar
    if not categorias_encontradas:
        for cegoria, keywords in palabras_clave.items():
            for keyword in keywords:
                if fuzz.partial_ratio(pregunta, keyword) >= 85:
                    categorias_encontradas.add(cegoria)

    else:
        categorias_asignadas = ", ".join([str(categoria.name) for categoria in categorias_encontradas])
        print(f"Pregunta asignada a la(s) categoría(s): {categorias_asignadas}")
        categoria : c.Categorias = c.parse_string_to_enum(categorias_asignadas)
        return categoria

# Choose response based on cegory
# Choose response based on cegory
def elegir_respuesta_por_categoria(categoria : c.Categorias):
    if categoria not in respuestas_predefinidas:
        return "Ok"
    
    respuestas = respuestas_predefinidas[categoria]
    
    if categoria == "HORA":
        # Manejo específico para la cegoría HORA
        hora_actual = obtener_fecha_hora("hora")  # Obtener la hora como número
        respuesta_elegida = random.choice(respuestas).format(hora=hora_actual)
        
    elif categoria == "DIA":
        # Manejo específico para la cegoría DIA
        dia_actual = obtener_fecha_hora("dia")  # Obtener el nombre del día
        respuesta_elegida = random.choice(respuestas).format(dia=dia_actual)
        
    elif categoria == "MES":
        # Manejo específico para la cegoría MES
        mes_actual = obtener_fecha_hora("mes")  # Obtener el nombre del mes
        respuesta_elegida = random.choice(respuestas).format(mes=mes_actual)
        
    else:
        respuesta_elegida = random.choice(respuestas)
    
    return respuesta_elegida

#
# Update respuestas.json file with new cegories
def update_respuestas_file():
    respuestas_predefinidas_str_keys = {k if isinstance(k, str) else k.name: v for k, v in respuestas_predefinidas.items()}
    with open("respuestas.json", "w") as file:
        json.dump(respuestas_predefinidas_str_keys, file, indent=4)


# Function to display unsuccessful conversations with cegories
def find_unsuccessful_responses():
    conversation_log = load_conversation_log()
    unsuccessful_responses = [entry for entry in conversation_log if entry.get('successfully') == False]
    
    if unsuccessful_responses:
        print("Las siguientes preguntas no fueron entendidas por el bot y sus cegorías asociadas:")
        for entry in unsuccessful_responses:
            print(f"Usuario: {entry['Usuario']} | categoría: {entry['categoria']}")
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
        categoria : set[c.Categorias] = categorizar_pregunta(user_input)
        response_text : str = elegir_respuesta_por_categoria(categoria)
        print("ROBO:", response_text)
        save_conversation(user_input, response_text, flag, categoria)
