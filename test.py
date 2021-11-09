import serial  # pip install pyserial
import time

PORT = '/dev/cu.usbmodem101'
BAUD_RATE = 9600
arduino = serial.Serial(port=PORT, baudrate=BAUD_RATE, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data




def send(command, result):
    x
    


while True:

    time_start = time.time()  # in seconds
    print(time_start)
    while time.time() < time_start + 2:
        data = arduino.readline()
        if data:
            print(data)

    print ("out of first read loop")

    value = write_read("status")  # need to wait for confirmation "Status ok"
    if value:
        print(value)

    print("entering feedback read loop")

    while True:
        data = arduino.readline()
        if data:
            print(data)
