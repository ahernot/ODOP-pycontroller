import time

from controller import ODOP
from composer import Composer
#from preferences import *

if __name__ == '__main__':
    
    odop = ODOP()

    while not odop.ready:
        time.sleep(0.1)

    composer = Composer (odop, 10, 36)
