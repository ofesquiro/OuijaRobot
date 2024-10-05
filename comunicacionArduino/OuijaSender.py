from socket import socket, AF_INET, SOCK_STREAM

host = 'raspberry_pi_ip_address'  # Replace with the Raspberry Pi's IP address
port = 65432

with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b'hello world')