import serial



arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)


def send(message):
    arduino.write(bytes(message, 'UTF-8'))
def receive():
    data = arduino.readline()
    return data.decode('UTF-8')
    
    

if __name__ == "__main__":
    while True:
        send("hola")
        received = receive()
        while received != None and received != '':
            print(received)