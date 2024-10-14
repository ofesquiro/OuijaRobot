import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import pygame
import os


#MODEL_FILE_PATH = "/home/esquiro/Escritorio/OuijaRobot/vosk/model"
MODEL_FILE_PATH : str = "/home/esquiro/Escritorio/OuijaRobot/model"
model : Model
recognizer : KaldiRecognizer
try:
    model = Model(MODEL_FILE_PATH)
    recognizer = KaldiRecognizer(model, 16000)
except Exception as err:
    print(err)

def play(text):
    if text == "hola":
        play_music()
    
       
def play_music():
    print("playing la vida loca")
    pygame.mixer.init()
    pygame.mixer.music.load("livinLaVidaLoca.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def translate() -> str:
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        print("listening...")
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            phrase = "Recognized Text: " + result_dict.get("text", "")
            stream.stop_stream()
            stream.close()
            p.terminate()
            return phrase 
   
    


    