import speech_recognition as sr
RECOGNIZER = sr.Recognizer()
def capture_voice_input():
    with sr.Microphone() as source:
        audio = RECOGNIZER.listen(source)
    return audio



def convert_voice_to_text(audio):
    pocketsphinx_model = sr.get_pocketsphinx_model()
    try:
        text2 = RECOGNIZER.recognize_vosk(audio, "es")
        text = RECOGNIZER.KaldiRecognizer(audio, "es")
        text3 = RECOGNIZER.recognize_sphinx(audio, pocketsphinx_model)
        print("text2 dice: " + text2)

    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text


def test():
    print(1)
def main():
    test()
main()

