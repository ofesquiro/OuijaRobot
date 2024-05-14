import speech_recognition as sr
import pygame

file_path = "/home/alumno/Documentos/OuijaRobot/src/livinLaVidaLoca.mp3"
RECOGNIZER = sr.Recognizer()


def capture_voice_input():
    with sr.Microphone() as source:
        print("listening...")
        try:
<<<<<<< HEAD
            audio = RECOGNIZER.listen(source, timeout=2)
        except sr.WaitTimeoutError:
            print("timeout")
            return None
=======
            audio = RECOGNIZER.listen(source,timeout=2)
        except sr.WaitTimeoutError:
            pass
>>>>>>> 8a9519445e41027286922b47240332dca3a2fa8c
    return audio


def convert_voice_to_text(audio):
    try:
<<<<<<< HEAD
        if audio is None:
=======
        if(audio == None):
>>>>>>> 8a9519445e41027286922b47240332dca3a2fa8c
            return ""
        print("converting...")
        text = RECOGNIZER.recognize_sphinx(audio, language="es-ES")
        print("el texto dice: " + text)

    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text
<<<<<<< HEAD


def give_response(text):
    return text


def play_music():
    print("playing la vida loca (bal)")
=======
def isBool(text):
    if text=="EN PELOTAS MUY EN BOLAS":
        play_music()
def play_music():
    print("playing la vida loca (bal)")
    file_path = "/home/alumno/Documentos/OuijaRobot/src/livinLaVidaLoca.mp3 "
>>>>>>> 8a9519445e41027286922b47240332dca3a2fa8c
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def main():
    audio = capture_voice_input()
    text = convert_voice_to_text(audio)
    give_response(text)


main()
