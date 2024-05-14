from enum import Enum, auto
#FILE_PATH = "C:\ ".strip()+"Users\Hp\AppData\Local\Programs\Python\Python312\Lib\site-packages\speech_recognition\pocketsphinx-data\es-ES\pronounciation-dictionary.dict"
FILE_PATH = "../models/es-ES/pronounciation-dictionary-copy.dict"


class LectureMode(Enum):
    read_only = "r"
    read_write = "r+"
    append = "a"
    write_only = "w"


def read_dictionary(open_mode,encoding='utf-8'):
    try:
        with open(FILE_PATH, open_mode, encoding=encoding) as file:
            return file
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


def add_phrase(text, pronunciation):
    file = read_dictionary(LectureMode.append.value)
    if correct_format_for_dictionary(text):
        dictionary_format_string = text + " " + pronunciation
        file.write(dictionary_format_string)
        content = file.read()
        print(content)


def remove_phrase(nonwanted_line):
    try:
        file = read_dictionary(LectureMode.read_write.value)
        file_lines = file.readlines()
        # Remove the string from the content
        modified_lines = [line for line in file_lines if line != nonwanted_line]
        # Write the modified content back to the file
        file.writelines(modified_lines)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)


def main():
    add_phrase("sango","s a n g o")
