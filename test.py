import speech_recognition as sr
import argparse
import logging
import sys
import os
from pathlib import Path
from vosk import list_models, list_languages
from vosk.transcriber.transcriber import Transcriber
parser = argparse.ArgumentParser(
        description = "Transcribe audio file and save result in selected format")
parser.add_argument(
        "--model", "-m", type=str,
        help="model path")
parser.add_argument(
        "--list-models", default=False, action="store_true",
        help="list available models")
parser.add_argument(
        "--list-languages", default=False, action="store_true",
        help="list available languages")
parser.add_argument(
        "--model-name", "-n", type=str,
        help="select model by name")
parser.add_argument(
        "--lang", "-l", default="en-us", type=str,
        help="select model by language")
parser.add_argument(
        "--input", "-i", type=str,
        help="audiofile")
parser.add_argument(
        "--output", "-o", default="", type=str,
        help="optional output filename path")
parser.add_argument(
        "--output-type", "-t", default="txt", type=str,
        help="optional arg output data type")
parser.add_argument(
        "--tasks", "-ts", default=10, type=int,
        help="number of parallel recognition tasks")
parser.add_argument(
        "--log-level", default="INFO",
        help="logging level")


# globales y constantes
EXIT_REQUEST = "salir"
RECOGNIZER = sr.Recognizer()
LANGUAGE_CODE = 'es-ES'
#KEY = "AIzaSyAqwPcs_F6cyNltsrZPGRQKRFakDX3d85"
def test():
    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.getLogger().setLevel(log_level)
    args.input = "audio.mp3"

    if args.list_models is True:
        list_models()
        return

    if args.list_languages is True:
        list_languages()
        return

    if not args.input:
        logging.info("Please specify input file or directory")
        sys.exit(1)

    if not Path(args.input).exists():
        logging.info("File/folder {args.input} does not exist, " \
                     "please specify an existing file/directory")
        sys.exit(1)

    transcriber = Transcriber(args)

    if Path(args.input).is_dir():
        task_list = [(Path(args.input, fn),
                      Path(args.output,
                           Path(fn).stem).with_suffix("." + args.output_type)) for fn in os.listdir(args.input)]
    elif Path(args.input).is_file():
        if args.output == "":
            task_list = [(Path(args.input), args.output)]
        else:
            task_list = [(Path(args.input), Path(args.output))]
    else:
        logging.info("Wrong arguments")
        sys.exit(1)

    transcriber.process_task_list(task_list)





def main():
    test()
main()


def capture_voice_input():
    with sr.Microphone() as source:
        audio = RECOGNIZER.listen(source)
    return audio


def convert_voice_to_text(audio):
    try:
        text2 = RECOGNIZER.recognize_vosk(audio, "es")
        print("text2 dice: " + text2)
        # text = RECOGNIZER.recognize_google(audio, LANGUAGE_CODE)
        # print("You said: " + text)

    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text

def exitProgram(text):
    return text == EXIT_REQUEST