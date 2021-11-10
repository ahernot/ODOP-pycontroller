# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import serial  # pip install pyserial
import time

from preferences import *


#TODO: python needs to print whatever the controller sends through serial


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
        print(f'\nexecuting {command}')

        # Send command
        self.controller .write(bytes(command, 'utf-8'))
        time.sleep(0.05)

        # Process readback
        time_start = time.time()  # in seconds
        while time.time() < time_start + time_window:
            data = self.controller .readline()
            if not readback:
                return True
            elif data and data == readback:
                return True
        
        return False


    def read (self, time_window: float = 2.):
        buffer = list()
        time_start = time.time()  # in seconds
        while time.time() < time_start + time_window:
            data = self.controller .readline()
            if data: buffer.append(data)
        return buffer


class ODOP (Controller):

    def __init__ (self, baud_rate: int = BAUD_RATE, port = PORT, ready_msg = READY_MSG, time_init_max = TIME_INIT_MAX):
        super(ODOP, self).__init__ (baud_rate, port, ready_msg, time_init_max)
        self.__angles = {'x': 0, 'y': 0}

    # def get_version (self): self.execute ('version')  # issue: doesn't print version
    def get_status (self): self.execute ('status', b'Status ok')

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
        return self.execute (command=f'move_rel {axis} {float(value)}', readback=f'move_rel {axis}: success', time_window=max(2*value, 2))

    def move_absolute (self, axis: str, value: float):
        axis = axis.lower()
        if axis not in ('x', 'y'): return False
        self.__angles [axis] = value
        return self.execute (command=f'move_abs {axis} {float(value)}', readback=f'move_abs {axis}: success', time_window=max(2*value, 2))
    