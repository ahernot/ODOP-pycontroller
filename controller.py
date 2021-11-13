# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import serial  # pip install pyserial
import time

from preferences import *

#TODO: tunable parameters for estimate_zero -200, +25
#TODO: python needs to print whatever the controller sends through serial
#TODO: tune time_window for move commands, AND FOR ABSOLUTE COMMANDS IN PARTICULAR
#TODO: get_version and get_status


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

    def execute (self, command: str, time_window = 2., readback = b'', fatal = b'') -> int:
        """
        0 for readback==readback
        1 for no readback even though readback specified
        2 for fatal
        """

        # Send command
        print(f'\nExecuting {command}')
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
                    return 0
                if fatal and data == fatal:  # Exit loop with failure
                    return 2

        if readback: return 1
        else: return 0  # True if readback unspecified


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
        self.__angles = {'x': 0., 'y': 0.}

    # def get_version (self): self.execute ('version')

    def get_status (self):
        val = self.execute (command='status', time_window=2., readback=b'Status ok\r\n')
        if val == 0: return True, ''
        else: return False, 'unable to verify status'

    def get_angle (self, axis: str) -> float:
        if axis not in ('x', 'y'): return None
        return self.__angles [axis]


    # Calibration
    def estimate_zero (self) -> tuple:
        #self.execute ('estimate_zero', b'estimate_zero: success', time_window=120.)  # 2min

        # Move to bottom of range
        val = self.execute (
            command='move_rel x -200',
            time_window=2., #120., ############################# DEBUG
            readback=b'move_rel x: limit reached\r\n',
            fatal=b'move_rel x: success\r\n'
        )
        print(val)
        #if val != 0: return False, 'unable to reach minimum'  # Exit if didn't find end stop ############################# DEBUG

        # Move up to estimate zero position
        success, msg = self.move_relative ('x', 25.)
        return success, msg


    def set_zero (self) -> bool:
        val = self.execute (command='set_zero', time_window=2., readback=b'set_zero: success\r\n')
        return val == 0


    # Motion
    def move_relative (self, axis: str, value: float) -> tuple:

        # Assert arguments
        axis = axis.lower()
        if axis not in ('x', 'y'): return False

        # Log movement
        self.__angles [axis] += value

        # Send command
        val = self.execute (
            command=f'move_rel {axis} {float(value)}',
            time_window=min(max(abs(2*value), 2), 60),  # no more than 60sec
            readback=bytes(f'move_rel {axis}: success\r\n', 'utf-8'),
            fatal=bytes(f'move_rel {axis}: limit reached\r\n', 'utf-8')
        )

        # Process output
        if   val == 0: return True, ''
        elif val == 2: return False, 'limit reached'
        else:          return False, 'timeout'


    def move_absolute (self, axis: str, value: float) -> tuple:

        # Assert arguments
        axis = axis.lower()
        if axis not in ('x', 'y'): return False

        # Log movement
        self.__angles [axis] = value

        # Send command
        val = self.execute (
            command=f'move_abs {axis} {float(value)}',
            time_window=30.,
            readback=bytes(f'move_abs {axis}: success\r\n', 'utf-8'),
            fatal=bytes(f'move_abs {axis}: limit reached\r\n', 'utf-8')
        )

        # Process output
        if   val == 0: return True, ''
        elif val == 2: return False, 'limit reached'
        else:          return False, 'timeout'
