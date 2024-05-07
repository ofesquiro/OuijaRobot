import speech_recognition as sr
from vosk import list_models, list_languages
from vosk.transcriber.transcriber import Transcriber
from vosk import KaldiRecognizer
from vosk import Model, SpkModel

RECOGNIZER = sr.Recognizer()
def capture_voice_input():
    with sr.Microphone() as source:
        audio = RECOGNIZER.listen(source)
    return audio



def convert_voice_to_text(audio):
    try:
        text2 = RECOGNIZER.recognize_vosk(audio, "es")
        text = RECOGNIZER.KaldiRecognizer(audio, "es")
        print("text2 dice: " + text2)

    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text


def test():
    audio = capture_voice_input()
    text = convert_voice_to_text(audio)
def main():
    test()
main()

