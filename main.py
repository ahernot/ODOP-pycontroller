# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import time

from camera import Camera
from controller import ODOP
from composer import Composer



if __name__ == '__main__':

    # Initialise camera
    camera = Camera()
    while not camera.ready():
        time.sleep(0.1)
        camera.update_status()
    
    # Initialise ODOP
    odop = ODOP()
    while not odop.ready():
        time.sleep(0.1)

    # Calibrate ODOP
    odop.estimate_zero()
    # execute commands
    # then validate and set_zero()

    # Initialise composer
    composer = Composer(
        odop=odop,
        vertical_shots_nb=6,
        horizontal_shots_nb=4
    )

    # Run composer
    composer.run()

