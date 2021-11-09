import time

from controller import ODOP
from preferences import *


"""
success = odop.execute ('status', b'Status ok\r\n')
print(success)

success = odop.execute ('angle x 10', b'angle_x: success\r\n', 20.)
print(success)

odop.read()
"""




class Composer:

    def __init__ (self, odop: ODOP, vertical_shots_nb: int, horizontal_shots_nb: int):
        self.odop = odop
        self.vertical_shots_nb = vertical_shots_nb
        self.horizontal_shots_nb = horizontal_shots_nb

        x_step_deg = (X_ANGLE_MAX - X_ANGLE_MIN) / (vertical_shots_nb - 1)
        y_step_deg = 360 / horizontal_shots_nb

    def run (self):

        for vertical_shot_id in range (self.vertical_shots_nb + 1):
            #print("\tCurrent vAngle is {}".format(currentVerticalAngle))

            # Reset Y-axis angle
            #print("\tReseting hAngle. Was {}".format(currentHorizontalAngle))
            #currentHorizontalAngle = 0
            self.odop .move_absolute ('y', 0)

            for horizontal_shot_id in range (self.horizontal_shots_nb):
                #print("\t\tCurrent hAngle is {}".format(currentHorizontalAngle))

                # Build file name
                file_path = SESSION_PATH + FILENAME_TEMPLATE.format(vertical_shot_id, currentVerticalAngle, horizontal_shot_id, currentHorizontalAngle)
                print("\t\tRequesting shot: " + fileLocationAndName)

                # Take shot
                #takePhoto(fileLocationAndName)

                # Move on Y-axis
                self.odop .move_relative ('y', self.y_step_deg)

            # Move on X-axis
            self.odop .move_relative ('x', self.x_step_deg)
