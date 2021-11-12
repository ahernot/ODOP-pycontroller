# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import time

from camera import Camera, CameraMac
from controller import ODOP
from composer import Composer



if __name__ == '__main__':

    # Initialise camera
    camera = CameraMac()  # Camera()
    while not camera.ready():
        time.sleep(0.1)
        camera.update_status()
    
    # Initialise ODOP
    odop = ODOP()
    while not odop.ready():
        time.sleep(0.1)

    # Calibrate ODOP
    success = odop.estimate_zero()  # remonter after no delay (after limit reached)
    # execute commands
    # then validate and set_zero()

    while True:
        command = input()
        if command == 'go': break
        odop.execute(command)
    
    odop.set_zero()
    print(odop.get_angle('x'))

    # Initialise composer
    composer = Composer(
        odop=odop,
        camera=camera,
        vertical_shots_nb=10, #6,
        horizontal_shots_nb=36 #4
    )

    # Run composer
    composer.run()
