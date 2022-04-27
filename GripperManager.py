try:
    import Jetson.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    open_gripper = 11
    close_gripper = 13
    GPIO.setup(open_gripper, GPIO.OUT)
    GPIO.setup(close_gripper, GPIO.OUT)
except Exception:
    print("Not running on jetson, gripper functionality will throw error")

prevCommand = False  # Holds the state of the previous command
gripperState = False  # Holds the actual state of the grippers
prevCommandC = False  # Holds the state of the previous command
gripperStateC = False  # Holds the actual state of the grippers


def openGripper(isActivated: bool) -> bool:
    """
    Reads the stream from the socket and activates the gripper only on the first change to true
    @param isActivated: the boolean that is sended from the controller
    @return: the actual state of the gripper
    """
    global prevCommand, gripperState, open_gripper
    if isActivated and not prevCommand:  # passes only the first true signal of the stream
        print("Oppening Gripper")
        GPIO.output(open_gripper, GPIO.HIGH)
        GPIO.output(open_gripper, GPIO.LOW)
        prevCommand = isActivated  # updating for the next iteration
    return True


def closeGripper(isActivated: bool) -> bool:
    """
    Reads the stream from the socket and activates the gripper only on the first change to true
    @param isActivated: the boolean that is sended from the controller
    @return: the actual state of the gripper
    """
    global prevCommandC, gripperStateC, close_gripper
    if isActivated and not prevCommandC:  # passes only the first true signal of the stream
        print("Closing gripper")
        GPIO.output(close_gripper, GPIO.HIGH)
        GPIO.output(close_gripper, GPIO.LOW)
        prevCommandC = isActivated
    return True


def clearPort():
    """
    Sets the pin to its default estate
    @return: void
    """
    print("Clearing gpio port")
    GPIO.cleanup()
