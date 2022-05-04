# some digital pins supported by the jetson gpio library
open_gripper = 11
close_gripper = 13
runMotor = 29
stopMotor = 31
try:
    import Jetson.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(open_gripper, GPIO.OUT)
    GPIO.setup(close_gripper, GPIO.OUT)
    GPIO.setup(runMotor, GPIO.OUT)
    GPIO.setup(stopMotor, GPIO.OUT)
except Exception:
    print("Not running on jetson, gripper functionality will throw error")

prevCommand = False  # Holds the state of the previous command
def openGripper(isActivated: bool):
    """
    Reads the stream from the socket and activates the gripper only on the first change to true
    @param isActivated: the boolean that is sended from the controller
    @return: the actual state of the gripper
    """
    global prevCommand, open_gripper
    if isActivated and not prevCommand:  # passes only the first true signal of the stream
        print("Oppening Gripper")
        GPIO.output(open_gripper, GPIO.HIGH)
        GPIO.output(open_gripper, GPIO.LOW)
    prevCommand = isActivated  # updating for the next iteration

prevCommandC = False  # Holds the state of the previous command
def closeGripper(isActivated: bool):
    """
    Reads the stream from the socket and activates the gripper only on the first change to true
    @param isActivated: the boolean that is sended from the controller
    @return: the actual state of the gripper
    """
    global prevCommandC, close_gripper
    if isActivated and not prevCommandC:  # passes only the first true signal of the stream
        print("Closing gripper")
        GPIO.output(close_gripper, GPIO.HIGH)
        GPIO.output(close_gripper, GPIO.LOW)
    prevCommandC = isActivated

prevCommandRM = False
def runMotor(isActivated: bool):
    global prevCommandRM, runMotor
    if isActivated and not prevCommandRM:
        print("Running motor")
        GPIO.output(runMotor, GPIO.HIGH)
        GPIO.output(runMotor, GPIO.LOW)
    prevCommandRM = isActivated

prevCommandSM = False
def stopMotor(isActivated: bool):
    global prevCommandSM, stopMotor
    if isActivated and not prevCommandSM:
        print("Stoping motor")
        GPIO.output(stopMotor, GPIO.HIGH)
        GPIO.output(stopMotor, GPIO.LOW)
    prevCommandSM = isActivated

def clearPort():
    """
    Sets the pin to its default estate
    @return: void
    """
    print("Clearing gpio port")
    GPIO.cleanup()
