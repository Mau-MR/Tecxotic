"""
import Jetson.GPIO as GPIO
gripper_pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gripper_pin, GPIO.OUT)
"""

prevCommand = False  # Holds the state of the previous command
gripperState = False  # Holds the actual state of the grippers


def gripperManager(isActivated: bool) -> bool:
    """
    Reads the stream from the socket and activates the gripper only on the first change to true
    @param isActivated: the boolean that is sended from the controller
    @return: the actual state of the gripper
    """
    global prevCommand, gripperState
    if isActivated and not prevCommand:  # passes only the first true signal of the stream
        gripperState = not gripperState
        # GPIO.output(gripper_pin, GPIO.HIGH) if (gripperState) else GPIO.output(gripper_pin, GPIO.LOW)
        print(gripperState)
    prevCommand = isActivated  # updating for the next iteration
    return gripperState
