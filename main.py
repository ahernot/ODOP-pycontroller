import time

from controller import ODOP
#from preferences import *

if __name__ == '__main__':
    
    odop = ODOP()

    while not odop.ready:
        time.sleep(0.1)
    
    success = odop.execute ('status', b'Status ok\r\n')
    print(success)

    success = odop.execute ('angle x 10', b'angle_x: success\r\n', 20.)
    print(success)

    odop.read()
