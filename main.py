# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import time

from controller import ODOP
from composer import Composer



if __name__ == '__main__':
    
    # Initialise ODOP
    odop = ODOP()

    while not odop.ready:
        time.sleep(0.1)

    # Initialise composer
    composer = Composer(
        odop=odop,
        vertical_shots_nb=6,
        horizontal_shots_nb=4
    )

    # Run composer
    composer.run()

#add calibration in protocol
