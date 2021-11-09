import time

from controller import ODOP
#from preferences import *

if __name__ == '__main__':
    
    odop = ODOP()

    while not odop.ready:
        time.sleep(0.1)

    print(odop.ready)

    x = odop.execute ('status')

    odop.read()
