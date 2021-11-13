# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import time

from camera import Camera, CameraPlaceholder
from controller import ODOP
from composer import Composer
from preferences import *


if __name__ == '__main__':

    # Initialise camera
    camera = CameraPlaceholder()  # Camera()
    while not camera.ready():
        time.sleep(0.1)
        camera.update_status()
    

    # Initialise ODOP
    odop = ODOP()
    while not odop.ready():
        time.sleep(0.1)


    # Calibrate ODOP
    print('\nCalibrating ODOP')
    success, msg = odop.estimate_zero()
    if not success: raise InterruptedError(f'estimate_zero failure - {msg}')
    success, msg = odop.adjust_position('x')
    if not success: raise InterruptedError(f'manual calibration failure - {msg}')
    odop.set_zero()


    # Initialise composer
    composer = Composer(
        odop=odop,
        camera=camera,
        vertical_shots_nb=10, #6,
        horizontal_shots_nb=36 #4
    )

    input(f'\nComposer initialised. Press any key to begin run.\n{RUN_MESSAGE}')

    # Run composer
    success, msg = composer.run()
    if not success: raise InterruptedError(f'run failure - {msg}')
