# Program settings
SESSION_PATH = "c:\\tmp\\"
FILENAME_TEMPLATE = "odop-vI{}-vA{}-hI{}-hA{}.jpg"
ENABLE_DGCC = True

# DGCC settings
dgccPath = "C:\\Program Files (x86)\\digiCamControl\\"
dgccMainEXE = "CameraControl.exe"
dgccTool = dgccPath + "CameraControlRemoteCmd.exe"
dgccSnapCommand = " /c capture "

# Serial settings
PORT = '/dev/cu.usbmodem101'  # 'COM5'
BAUD_RATE = 9600
READY_MSG = 'Controller ready'  # Program waits for this message

# X-axis angular range (total range is divided by number of vertical shots)
X_ANGLE_MIN = -15.
X_ANGLE_MAX = 90.

# Delays
TIME_INIT_MAX = 60.  # in seconds
TIME_WINDOW_MIN = 2.  # Minimum time window to execute a command
TIME_WINDOW_MAX = 120.  # Maximum time window to execute a command (default for move_abs commands)
DELAY_BEFORE_SHOT = 1.
DELAY_AFTER_SHOT = 1.5

# Verbose
DEBUG_VERBOSE = False
STATUS_VERBOSE = True
RUN_MESSAGE = 'Make sure to remove all calibration cables before starting run.'



# Time windows must be wide enough to avoid having backlogged processes and the completion message of the previous process validating the next one
# Document that Y channel is used for xLimMax

# ODOP needs to be recalibrated every time a new ODOP() object is created, due to the fact that the locally-stored positional information is reset
