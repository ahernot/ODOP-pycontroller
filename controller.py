# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import serial  # pip install pyserial
import time

from preferences import *


#TODO: python needs to print whatever the controller sends through serial
#TODO: tune time_window for move commands, AND FOR ABSOLUTE COMMANDS IN PARTICULAR


class Controller:

    def __init__ (self, baud_rate: int = BAUD_RATE, port = PORT, ready_msg = READY_MSG, time_init_max = TIME_INIT_MAX):
        self.controller = serial.Serial(port=PORT, baudrate=BAUD_RATE, timeout=.1)
        self.ready_msg = ready_msg
        self.__ready = False
        self.time_init = time.time()
        self.time_init_max = time_init_max

        if not self.__ready:
            self.__check_ready()
    
    def __check_ready (self):
        while True:
            data = self.controller .readline()
            if data: print(data.decode('utf-8'))  ##################PRINT
            if data == self.ready_msg:
                self.__ready = True
                break
            if time.time() > self.time_init + self.time_init_max:
                print('Error: controller not ready')
                break
    
    def ready (self):
        return self.__ready

    def execute (self, command: str, time_window = 2., readback = b'', fatal = b''):
        print(f'\nExecuting {command}')

        # Send command
        self.controller .write(bytes(command, 'utf-8'))
        time.sleep(0.05)

        # Process readback
        time_start = time.time()  # in seconds
        # print(f'{int(time_start)} - waiting till {int(time_start + time_window)} ({time_window} seconds)')
        while time.time() < time_start + time_window:
            # Read data
            data = self.controller .readline()
            
            if data:
                print(data) #.decode('utf-8')[:-1])  ##################PRINT
                if readback and data == readback:  # Exit loop with success
                    return True
                if fatal and data == fatal:  # Exit loop with failure
                    return False
        
        return not (not readback)


    def read (self, time_window: float = 2.):
        buffer = list()
        time_start = time.time()  # in seconds
        while time.time() < time_start + time_window:
            data = self.controller .readline()
            if data: buffer.append(data)
        print(buffer.decode('utf-8')) ##################PRINT
        return buffer


class ODOP (Controller):

    def __init__ (self, baud_rate: int = BAUD_RATE, port = PORT, ready_msg = READY_MSG, time_init_max = TIME_INIT_MAX):
        super(ODOP, self).__init__ (baud_rate, port, ready_msg, time_init_max)
        self.__angles = {'x': 0, 'y': 0}

    # def get_version (self): self.execute ('version')  # issue: doesn't print version
    def get_status (self):
        self.execute (command='status', time_window=2., readback=b'Status ok\r\n')

    def get_angle (self, axis: str):
        if axis not in ('x', 'y'): return None
        return self.__angles [axis]

    # Calibration
    def estimate_zero (self):
        #self.execute ('estimate_zero', b'estimate_zero: success', time_window=120.)  # 2min

        # Move to bottom of range
        success = self.execute (
            command='move_rel x -200',
            time_window=120.,
            readback=b'move_rel x: limit reached\r\n',
            fatal=b'move_rel x: success\r\n'
        )
        if not success: return False, 'unable to reach minimum'  # Exit if didn't find end stop
        #if success: return False, '' ########################### FOR TESTS ONLY

        # Move up to estimate zero position
        success, msg = self.move_relative ('x', 25.)
        return success

    def set_zero (self):
        return self.execute (command='set_zero', time_window=2., readback=b'set_zero: success\r\n')

    # Motion
    def move_relative (self, axis: str, value: float):
        axis = axis.lower()
        if axis not in ('x', 'y'): return False
        self.__angles [axis] += value
        return self.execute (
            command=f'move_rel {axis} {float(value)}',
            time_window=min(max(abs(2*value), 2), 60),  # no more than 60sec
            readback=bytes(f'move_rel {axis}: success\r\n', 'utf-8'),
            fatal=bytes(f'move_rel {axis}: limit reached\r\n', 'utf-8')
        )  

    def move_absolute (self, axis: str, value: float):
        axis = axis.lower()
        if axis not in ('x', 'y'): return False
        self.__angles [axis] = value
        return self.execute (
            command=f'move_abs {axis} {float(value)}',
            time_window=30.,
            readback=bytes(f'move_abs {axis}: success\r\n', 'utf-8'),
            fatal=bytes(f'move_abs {axis}: limit reached\r\n', 'utf-8')
        )
    