import serial  # pip install pyserial
import time

from preferences import *



class Controller:

    def __init__ (self, baud_rate: int = BAUD_RATE, port = PORT, ready_msg = READY_MSG, time_init_max = TIME_INIT_MAX):
        self.controller = serial.Serial(port=PORT, baudrate=BAUD_RATE, timeout=.1)
        self.ready_msg = ready_msg
        self.ready = False
        self.time_init = time.time()
        self.time_init_max = time_init_max

        if not self.ready:
            self.__check_ready()
    
    def __check_ready (self):
        while True:
            data = self.controller .readline()
            if data == self.ready_msg:
                self.ready = True
                break
            if time.time() > self.time_init + self.time_init_max:
                print('Error: controller not ready')
                break

    def execute (self, command: str, readback = b'', time_window = 2.):
        # read_window in seconds
        print(f'\nexecuting {command}')

        # Send command
        self.controller .write(bytes(command, 'utf-8'))
        time.sleep(0.05)

        time_start = time.time()  # in seconds
        while time.time() < time_start + time_window:
            data = self.controller .readline()
            if data: print(data)

            if not readback:
                return True
            elif data and data == readback:
                return True
        
        return False


    def read (self, time_window: float = 2.):
        time_start = time.time()  # in seconds
        while time.time() < time_start + time_window:
            data = self.controller .readline()
            if data: print(data)


class ODOP (Controller):

    def __init__ (self, baud_rate: int = BAUD_RATE, port = PORT, ready_msg = READY_MSG, time_init_max = TIME_INIT_MAX):
        super(ODOP, self).__init__ (baud_rate, port, ready_msg, time_init_max)
        self.__angles = {'x': 0, 'y': 0}

    def get_version (self):
        pass

    def get_status (self):
        self.execute ('status', b'Status ok')

    def get_angle (self, axis: str):
        if axis not in ('x', 'y'): return None
        return self.__angles [axis]

    # Calibration
    def estimate_zero (self):
        self.execute ('estimate_zero', b'estimate_zero: success')
    def set_zero (self):
        return self.execute ('set_zero', b'set_zero: success')

    # Motion
    def move_relative (self, axis: str, value: float):
        axis = axis.lower()
        if axis not in ('x', 'y'): return False
        self.__angles [axis] += value
        return self.execute (command=f'angle {axis} {float(value)}', readback=f'angle_{axis}: success', time_window=max(2*value, 2))

    def move_absolute (self, axis: str, value: float):
        axis = axis.lower()
        if axis not in ('x', 'y'): return False
        self.__angles [axis] = value
        return self.execute (command=f'move {axis} {float(value)}', readback=f'move_{axis}: success', time_window=max(2*value, 2))
    