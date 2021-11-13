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


    def run (self):

        # Move swing to lowest position
        success = self.odop .move_absolute ('x', self.vertical_angle_min)
        if not success: return False

        # Run through vertical steps (swing rotation)
        for vertical_shot_id in range (self.vertical_shots_nb + 1):
            print('\tCurrent vAngle is {}'.format(self.odop.get_angle('x')))

            # Reset Y-axis angle
            #print('\tResetting hAngle. Was {}'.format(self.odop.get_angle('y')))
            #self.odop .move_absolute ('y', 0)
            #success = self.odop .execute ('move_abs y 0', b'move_abs y: success\r\n', 60.)
            #if not success: return False

            # Run through horizontal steps (turntable rotation)
            for horizontal_shot_id in range (self.horizontal_shots_nb):
                print('\t\tCurrent hAngle is {}'.format(self.odop.get_angle('y')))

                # Build file name
                filepath = SESSION_PATH + FILENAME_TEMPLATE .format(vertical_shot_id, self.odop.get_angle('x'), horizontal_shot_id, self.odop.get_angle('y'))
                print('\t\tRequesting shot: ' + filepath)

                time_now = time.time()
                print('waiting')
                while (time.time() < time_now + 2):
                    pass
                print('done waiting')

                # Take shot
                time.sleep(1.)
                self.camera .capture(filepath=filepath)
                time.sleep(1.)  #!!! WAIT FOR SUCCESS

                # Move on Y-axis (turntable)
                self.odop .move_relative ('y', self.y_step_deg)

            # Move on X-axis (swing)
            success = self.odop .move_relative ('x', self.x_step_deg)
            if not success: return False

        print('Run success')
        return True
