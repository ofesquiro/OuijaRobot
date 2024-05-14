import speech_recognition as sr
import pygame

RECOGNIZER = sr.Recognizer()
def capture_voice_input():
    with sr.Microphone() as source:
        print("listening...")
        try:
            audio = RECOGNIZER.listen(source,timeout=2)
        except sr.WaitTimeoutError:
            pass
    return audio



def convert_voice_to_text(audio):
    try:
        if(audio == None):
            return ""
        print("converting...")
        text = RECOGNIZER.recognize_sphinx(audio,language="es-ES")
        print("text2 dice: " + text)

    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text
def isBool(text):
    if text=="EN PELOTAS MUY EN BOLAS":
        play_music()
def play_music():
    print("playing la vida loca (bal)")
    file_path = "/home/alumno/Documentos/OuijaRobot/src/livinLaVidaLoca.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
def run():
    audio = capture_voice_input()
    text = convert_voice_to_text(audio)
    isBool(text)

def main():
    run()
main()

