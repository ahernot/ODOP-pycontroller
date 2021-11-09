# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

from controller import ODOP
from preferences import *



class Composer:

    def __init__ (self, odop: ODOP, vertical_shots_nb: int, horizontal_shots_nb: int):
        self.odop = odop
        self.vertical_shots_nb = vertical_shots_nb
        self.horizontal_shots_nb = horizontal_shots_nb

        self.x_step_deg = (X_ANGLE_MAX - X_ANGLE_MIN) / (vertical_shots_nb - 1)
        self.y_step_deg = 360 / horizontal_shots_nb

    def run (self):
        # Run through vertical steps (swing rotation)
        for vertical_shot_id in range (self.vertical_shots_nb + 1):
            print('\tCurrent vAngle is {}'.format(self.odop.get_angle('x')))

            # Reset Y-axis angle
            print('\tReseting hAngle. Was {}'.format(self.odop.get_angle('y')))
            self.odop .move_absolute ('y', 0)

            # Run through horizontal steps (turntable rotation)
            for horizontal_shot_id in range (self.horizontal_shots_nb):
                print('\t\tCurrent hAngle is {}'.format(self.odop.get_angle('y')))

                # Build file name
                filepath = SESSION_PATH + FILENAME_TEMPLATE .format(vertical_shot_id, self.odop.get_angle('x'), horizontal_shot_id, self.odop.get_angle('x'))
                print('\t\tRequesting shot: ' + filepath)

                # Take shot
                #takePhoto(filepath)

                # Move on Y-axis
                self.odop .move_relative ('y', self.y_step_deg)

            # Move on X-axis
            self.odop .move_relative ('x', self.x_step_deg)

        print('Run success')
