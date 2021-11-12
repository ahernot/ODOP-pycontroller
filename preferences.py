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
READY_MSG = b'Controller ready\r\n'

TIME_INIT_MAX = 60  # in seconds

# X-axis angular range
X_ANGLE_MIN = -15.
X_ANGLE_MAX = 90.
