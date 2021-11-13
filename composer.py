# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.

import time

from camera import Camera
from controller import ODOP
from preferences import *



class Composer:

    def __init__ (self, odop: ODOP, camera: Camera, vertical_shots_nb: int, horizontal_shots_nb: int, vertical_angle_min: float = X_ANGLE_MIN, vertical_angle_max: float = X_ANGLE_MAX):
        self.odop = odop
        self.camera = camera
        self.vertical_shots_nb = vertical_shots_nb
        self.horizontal_shots_nb = horizontal_shots_nb
        self.vertical_angle_min = vertical_angle_min
        self.vertical_angle_max = vertical_angle_max

        self.x_step_deg = (X_ANGLE_MAX - X_ANGLE_MIN) / (vertical_shots_nb - 1)
        self.y_step_deg = 360 / horizontal_shots_nb


    def run (self) -> tuple:
        print('\nStarting run')

        # Move swing to lowest position
        success, val = self.odop .move_absolute ('x', self.vertical_angle_min)
        if not success: return False, val

        # Run through vertical steps (swing rotation)
        for vertical_shot_id in range (self.vertical_shots_nb + 1):
            print(f'\tCurrent vAngle is {self.odop.get_angle("x")}')

            # Reset Y-axis angle
            print('\tResetting hAngle. Was {}'.format(self.odop.get_angle('y')))
            self.odop .set_angle ('y', 0.)
            #success, val = self.odop .execute (command='move_abs y 0', time_window=60., readback='move_abs y: success')
            #if not success: return False, val

            # Run through horizontal steps (turntable rotation)
            for horizontal_shot_id in range (self.horizontal_shots_nb):
                print(f'\t\tCurrent hAngle is {self.odop.get_angle("y")}')

                # Build file name
                filepath = SESSION_PATH + FILENAME_TEMPLATE .format(vertical_shot_id, self.odop.get_angle('x'), horizontal_shot_id, self.odop.get_angle('y'))
                print(f'\t\tRequesting shot: {filepath}')

                # Take shot
                time.sleep(DELAY_BEFORE_SHOT)
                self.camera .capture(filepath=filepath)
                time.sleep(DELAY_AFTER_SHOT)

                # Move on Y-axis (turntable)
                self.odop .move_relative ('y', self.y_step_deg)

            # Move on X-axis (swing)
            success, val = self.odop .move_relative ('x', self.x_step_deg)
            if not success: return False, val

        print('Run success')
        return True, ''
