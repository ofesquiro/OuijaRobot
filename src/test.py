import speech_recognition as sr
import pygame
import pyaudio as pa
RECOGNIZER = sr.Recognizer()
def capture_voice_input():
    with sr.Microphone() as source:
        audio = RECOGNIZER.listen(source)
    return audio



def convert_voice_to_text(audio):
    try:
        text = RECOGNIZER.recognize_google_cloud(audio)
        print("text2 dice: " + text)

    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text
def isBul(text):
    if text == "bool":
        file = "livinLaVidaLoca.mp3"
        print(1)
        play_music(file)
def play_music(file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

# Replace 'your_file.mp3' with the path to your MP3 file

def test():
    audio = capture_voice_input()
    text = convert_voice_to_text(audio)
    isBul(text)

def main():
    test()
main()

