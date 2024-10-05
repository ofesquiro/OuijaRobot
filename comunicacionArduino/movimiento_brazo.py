from gpiozero import Servo
from time import sleep
from socket import socket

# Define the angles for each letter
angles : dict[str, tuple[int, int, int, int]] = {
    'a': (1, 1, 1, 1),
    'b': (2, 2, 2, 2),
    'c': (3, 3, 3, 3),
    'd': (4, 4, 4, 4),
    'e': (5, 5, 5, 5),
    'f': (6, 6, 6, 6),
    'g': (7, 7, 7, 7),
    'h': (8, 8, 8, 8),
    'i': (9, 9, 9, 9),
    'j': (10, 10, 10, 10),
    'k': (11, 11, 11, 11),
    'l': (12, 12, 12, 12),
    'm': (13, 13, 13, 13),
    'n': (14, 14, 14, 14),
    'o': (15, 15, 15, 15),
    'p': (16, 16, 16, 16),
    'q': (17, 17, 17, 17),
    'r': (18, 18, 18, 18),
    's': (19, 19, 19, 19),
    't': (20, 20, 20, 20),
    'u': (21, 21, 21, 21),
    'v': (22, 22, 22, 22),
    'w': (23, 23, 23, 23),
    'x': (24, 24, 24, 24),
    'y': (25, 25, 25, 25),
    'z': (26, 26, 26, 26),
    'si': (27, 27, 27, 27),
    'no': (28, 28, 28, 28)
}


# Initialize the servos
servo1 : Servo = Servo(17)  # GPIO pin 17
servo2 : Servo = Servo(18)  # GPIO pin 18
servo3 : Servo = Servo(27)  # GPIO pin 27
servo4 : Servo = Servo(22)  # GPIO pin 22


def move_servos(letter):
    if letter in angles:
        angle1, angle2, angle3, angle4 = angles[letter]
        servo1.value = angle1 / 180.0 - 1
        servo2.value = angle2 / 180.0 - 1
        servo3.value = angle3 / 180.0 - 1
        servo4.value = angle4 / 180.0 - 1
        sleep(1)  # Wait for 1 second


def main():
    input_string = input("Enter a string: ").lower()
    for letter in input_string:
        move_servos(letter)


def _main():
    # Set up the server
    host = '0.0.0.0'  # Listen on all interfaces
    port = 65432      # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                input_string = data.decode('utf-8').lower()
                for letter in input_string:
                    move_servos(letter)


if __name__ == "__main__":
    main()