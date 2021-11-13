# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import time

from camera import Camera, CameraPlaceholder
from controller import ODOP
from composer import Composer


# ADD PREFERENCE FOR TIME TO WAIT FOR SHOT


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
    success, msg = odop.estimate_zero()
    if not success: raise InterruptedError(f'estimate_zero failure - {msg}')

    print('\nInput relative adjustments (in deg). Type \'go\' to set zero.')
    while True:
        command = input('$ ')  # need to input '3' for 'move_rel x 3'
        if command == 'go': break
        odop.move_relative('x', float(command))
    
    odop.set_zero()
    # print('\n')

    # Initialise composer
    composer = Composer(
        odop=odop,
        camera=camera,
        vertical_shots_nb=10, #6,
        horizontal_shots_nb=36 #4
    )

    input('\nComposer initialised. Press any key to begin run.')

    # Run composer
    success, msg = composer.run()
    if not success: raise InterruptedError(f'run failure - {msg}')
