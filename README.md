# ODOP pycontroller v1.0
Copyright (C) 2021 <a href="github.com/ahernot">Anatole Hernot (github.com/ahernot)</a>, Mines Paris (PSL Research University). All rights reserved.

<br><br>

## Description
Controller program for <a href="https://www.smartpixels.fr">SmartPixels</a>' Omni-Directional Object Pictures (ODOP) automated scanner.

<br><br>

## Operation
### 1. Unpowered calibration
* <strong>1.1.</strong> With the motors unpowered, position the swing on its lowest position.
* <strong>1.2.</strong> Mount the camera on the sliding platform.
* <strong>1.3.</strong> Adjust the camera's distance from the object by sliding the platform.
* <strong>1.4.</strong> Adjust the counterweights so that the camera lifts up lightly from the lowest resting point of the swing.
* <strong>1.5.</strong> Point the camera towards the intersection between the vertical axis (of the turntable) and the horizontal axis (of the swing).
* <strong>1.6.</strong> Mount the front horizontal wire (the one closest to the camera) onto the frame.
* <strong>1.7.</strong> Adjust the camera's horizontal inclination to match the wire's.

### 2. Powered calibration
* <strong>2.1.</strong> Turn on power to the motors.\
Create a new `ODOP` object.
* <strong>2.2.</strong> Run the calibration process (method `ODOP.calibrate()`).
    * <strong>2.2.1.</strong> Let the swing move to its lowest position and then back up to the specified calibration point.
    *  <strong>2.2.2.</strong> Mount the back horizontal wire onto the frame.
    * <strong>2.2.3.</strong> Enter manual rotation commands (e.g. "`-1.8`" for -1.8°) until the two wires overlap on the camera's screen.
    * <strong>2.2.4.</strong> Type "`go`" to validate and set the zero point. The camera should be horizontal wiht respect to the machine.
* <strong>2.3.</strong> Remove all calibration wires from the machine.

### 3. Composition
* 3.1. Specify the number of vertical and horizontal shots to be taken.\
Create a new `Composition` object. 
* 3.2. Run the composition. (method `Composition.run()`).

<br><br>

## Usage guidelines
* Time windows (in `Controller.execute()`) must be large enough to avoid backlogging commands. Otherwise, the completion success message of the previous command could trigger the end of the next one.
* ODOP needs to be recalibrated every time a new `ODOP` object is created, due to the fact that the locally-stored positional information is reset in `ODOP.__init__()`.

<br><br>

## Requirements
* Python 3 (tested with Python 3.9.0; should work with python 3.6.0 and newer)
* PySerial (run `pip install pyserial`)