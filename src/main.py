import speech_recognition as sr
import pygame
from Dictionary_manager import *



file_path : str = "/home/esquiro/Escritorio/OuijaRobot/src/main.py"

RECOGNIZER : sr.Recognizer = sr.Recognizer()


def capture_voice_input() -> sr.AudioData | None:
    with sr.Microphone() as source:
        print("listening...")
        try:
            audio: sr.AudioData = RECOGNIZER.listen(source, timeout=2)
        except sr.WaitTimeoutError:
            print("timeout")
            return None
        except sr.RequestError as e:
            print("Error; {0}".format(e))
            return None
    return audio


def convert_voice_to_text(audio: sr.AudioData) -> str:
    try:
        if audio is None:
            return ""
        print("converting...")
        text: str = RECOGNIZER.recognize_sphinx(audio_data=audio, language="es-ES")
        print("el texto dice: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text


def give_response(text) -> str:
    return text


def play(text) -> None:
    if text == "hola":
        play_music()
    
    
        
def play_music() -> None:
    print("playing la vida loca (bal)")
    pygame.mixer.init()
    pygame.mixer.music.load("src/livinLaVidaLoca.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def learning() -> None:
    exit = True
    while exit:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        play(text)
        feedback = input("es esto lo que quisiste decir? (s/n)")
        if (feedback == "n"):
            frase = input("que quisiste decir?")
            add_phrase(frase)
        exit = input("quieres salir? (s/n)") == "n"


def main() -> None:
    learning()


main()
