import serial  # pip install pyserial
import time

from preferences import *



class ODOP:

    def __init__(self, baud_rate: int = BAUD_RATE, port = PORT, ready_msg = READY_MSG, time_init_max = TIME_INIT_MAX):
        self.controller = serial.Serial(port=PORT, baudrate=BAUD_RATE, timeout=.1)
        self.ready_msg = ready_msg
        self.ready = False
        self.time_init = time.time()
        self.time_init_max = time_init_max

        if not self.ready:
            self.__check_ready()
    
    def __check_ready(self):
        while True:
            data = self.controller .readline()
            if data == self.ready_msg:
                self.ready = True
                break
            if time.time() > self.time_init + self.time_init_max:
                print('Error: controller not ready')
                break

    def execute(self, command: str, output = b'', time_window = 2.):
        # read_window in seconds
        print(f'\nexecuting {command}')

        # Send command
        self.controller .write(bytes(command, 'utf-8'))
        time.sleep(0.05)

        time_start = time.time()  # in seconds
        while time.time() < time_start + time_window:
            data = self.controller .readline()
            if data: print(data)

            if not output:
                return True
            elif data and data == output:
                return True
        
        return False


    def read (self, time_window: float = 2.):
        time_start = time.time()  # in seconds
        while time.time() < time_start + time_window:
            data = self.controller .readline()
            if data: print(data)




