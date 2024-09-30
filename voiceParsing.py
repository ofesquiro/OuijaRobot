import os
import wave
import json
import pyaudio
import soundfile as sf
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
import pygame



#MODEL_FILE_PATH = "/home/esquiro/Escritorio/OuijaRobot/vosk/model"
MODEL_FILE_PATH = "/home/esquiro/Escritorio/OuijaRobot/vosk/model"


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



async def translate() -> str:
    try:
        model = Model(MODEL_FILE_PATH)
        recognizer = KaldiRecognizer(model, 16000)
    except Exception as err:
        print (err)

    # Initialize PyAudio
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
   
def main():     
    text = translate()
    print(text)
    play(text)
    
    
main()


    