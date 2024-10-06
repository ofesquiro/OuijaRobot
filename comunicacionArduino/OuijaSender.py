from socket import socket, AF_INET, SOCK_STREAM
from typing import Literal
# 


def send_string_to_raspberry(string : str):
    print(f"Message sent to board: {string}")

"""
def send_string_to_raspberry(string : str):
    HOST : Literal ["raspberry_pi_ip"] = 'raspberry_pi_ip'  # Replace with the Raspberry Pi's IP address
    PORT : Literal[65432] = 65432              # Port to connect to

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(string.encode('utf-8'))
        print(f"Sent: {string}")

    


"""
