import serial

arduino = serial.Serial('COM3', 9600, timeout=1)

def leer(mensaje : str):
    while True:
        try:
            arduino.write(mensaje.encode())
            arduino.close()
        except KeyboardInterrupt:
            break
