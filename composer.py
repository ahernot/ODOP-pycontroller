import time

from controller import ODOP

odop = ODOP()

while not odop.ready:
    time.sleep(0.1)

success = odop.execute ('status', b'Status ok\r\n')
print(success)

success = odop.execute ('angle x 10', b'angle_x: success\r\n', 20.)
print(success)

odop.read()




for vShot in range(NUMBER_OF_VERTICAL_SHOTS):
    print("\tCurrent vAngle is {}".format(currentVerticalAngle));

    print("\tReseting hAngle. Was {}".format(currentHorizontalAngle));
    currentHorizontalAngle=0
    
    odopGoTo(currentVerticalAngle)
    for hShot in range(NUMBER_OF_HORIZONTAL_SHOTS):
        print("\t\tCurrent hAngle is {}".format(currentHorizontalAngle));
        
        #Build file name
        fileLocationAndName=SESSION_PATH + FILENAME_TEMPLATE.format(vShot,currentVerticalAngle,hShot,currentHorizontalAngle)
        print("\t\tRequesting shot:"+fileLocationAndName)
        #Take shot
        takePhoto(fileLocationAndName)

        #Rotate the H-table
        horizontalRelativeStep()
        currentHorizontalAngle=currentHorizontalAngle+angleBetweenHorizontalShots

    print("Done horizontal cycle")
    currentVerticalAngle=currentVerticalAngle+angleBetweenVerticalShots
    
print("Done vertical cycle")