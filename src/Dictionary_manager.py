from enum import Enum, auto


#FILE_PATH = "C:\ ".strip()+"Users\Hp\AppData\Local\Programs\Python\Python312\Lib\site-packages\speech_recognition\pocketsphinx-data\es-ES\pronounciation-dictionary.dict"
FILE_PATH = "/home/esquiro/Escritorio/OuijaRobot/models/es-ES/pronounciation-dictionary-copy.dict"


def read_dictionary(encoding='utf-8'):
    try:
        with open(FILE_PATH,"r", encoding=encoding) as file:
            return file.readlines()
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def correct_format_for_dictionary(text):
    defining_pronunciation = False
    index = 0
    for letter in text:
        if defining_pronunciation:
            if letter == " " and text[index + 1] == " ":
                return False
        if letter == " ":
            defining_pronunciation = True
        index += 1
    return True


def exists_phrase(text):
    fileLines = read_dictionary()
    for line in fileLines:
        if text in line:
            print("The phrase already exists in the dictionary.")
            return True
    return False


def split_text(text):
    splited = text.split(" ")
    return splited


def add_phrase(text):
    texts = split_text(text)
    for word in texts:
        pronunciation = input("pronunciation of " + word + ":")
        add_one_phrase(word, pronunciation)

def add_one_phrase(text, pronunciation):
     if correct_format_for_dictionary(text) and not exists_phrase(text):
        dictionary_format_string = text + " " + pronunciation
        with open(FILE_PATH, "a") as file:
            file.write( "\n"+dictionary_format_string + "\n")
    
def remove_phrase(nonwanted_line):
    try:
        file = read_dictionary()
        file_lines = file.readlines()
        # Remove the string from the content
        modified_lines = [line for line in file_lines if line != nonwanted_line]
        # Write the modified content back to the file
        file.writelines(modified_lines)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)