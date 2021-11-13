# Copyright (C) 2021 SmartPixels & Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import os
import subprocess

from preferences import *



def process_exists(process_name):
    #output = ""
    output = subprocess.Popen('tasklist /FI "imagename eq {process_name}"' , stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE) .communicate()[0]
    
    # Check in last line for process name
    last_line = bytes(output)
    last_line = output.split(bytes('\r\n', 'utf-8'))
    try:
        last_line = last_line[3].lower()
    except:
        return False
        
    print(f'last line: {last_line}')

    # Because Fail message could be translated
    pname = bytes(process_name, 'utf-8')
    if (pname.lower() in last_line):
        return True
    else:
        return False


class Camera:

    def __init__ (self):
        self.__ready = False
        self.update_status()

    def update_status (self):
        # if (process_exists(dgccMainEXE)):
        #     self.__ready = True
        # else:
        #     print('DGCC is not running. Please launch the app and then run Camera.update_status()')
        #     self.__ready = False

        self.__ready = True  # override (process_exists doesn't work)

    def ready (self):
        return self.__ready

    def capture (self, filepath: str):
        command = f'"{dgccTool}" {dgccSnapCommand} {filepath}'
        os.system(command)
        return True


class CameraPlaceholder:

    def __init__ (self):
        self.__ready = True
    
    def update_status (self):
        pass

    def ready (self):
        return self.__ready

    def capture (self, filepath: str):
        if DEBUG_VERBOSE: print('Capturing')
        return True
