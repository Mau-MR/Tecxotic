import cv2
from Constants import *
import json

WIDTH = HEIGHT = 0
  
def calcPercentage(msk): 
    height, width = msk.shape[:2] 
    num_pixels = height * width 
    count_white = cv2.countNonZero(msk) 
    percent_white = (count_white/num_pixels) * 100 
    percent_white = round(percent_white,2) 
    return(percent_white) 
def getTargetInfo(mask, frame, size, percentage ):
    try:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = sorted(contours, key=cv2.contourArea, reverse=True)
        contour = contour[0]  #largest contour found
        area = cv2.contourArea(contour)
        if area > size[0] and area < size[1]:
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Target", (x, y), cv2.FONT_HERSHEY_SIMPLEX,  1.0, (0, 255, 0))
            
            x_center = x + ( w/2 )
            y_center = y + ( h/2 )
            
            calculated_per = calcPercentage(mask[y:y+h, x:x+w])
            if calculated_per > percentage[0] and calculated_per < percentage[1]:
                return int(x_center), int( y_center ), (x, y, w, h)
            else:
                return -1,-1, (-1,-1,-1,-1)
    except:
        pass
    return -1,-1, (-1,-1,-1,-1)
def putCenter(frame):
    global WIDTH, HEIGHT
    x_center = int(WIDTH/2) 
    y_center = int(HEIGHT/2) 
    frame = cv2.circle(frame, (x_center, y_center), 2, (0,255,0), 5)
    return (x_center, y_center)

def calculateDistanceFromCenter(target_position, target_input):
    x_diff = target_position[0] - target_input[0]
    y_diff = target_position[1] - target_input[1]
    return -x_diff, y_diff
def getValueRange():
    values = json.loads(open(JSON_AI1_FILE, "r").read())
    #values = json.loads(open("Agent1.json", "r").read())
    try:
        return (values['first_low'], values['second_low'],values['third_low'], 0), (values['first_high'],values['second_high'],values['third_high'],255), (values['size_min'], values['size_max']), (values['percentage_min'], values['percentage_max'])
    except Exception as e:
        print("Error in Agent1.py"+str(e))
        values.close()
    return (-1,-1,-1),(-1,-1,-1),(-1,-1),(-1,-1)
"""
capture_connected = False
cap = None
def connectVideo():
    global capture_connected, cap
    if cap is None or not cap.isOpened():
        capture_connected = False
    while capture_connected == False:
        try:
            #cap = cv2.VideoCapture("http://"+IP_ADDRESS+":"+str(PORT_CAM1)+"/stream.mjpg")
            cap = cv2.VideoCapture(0)
            capture_connected = True
        except Exception as e:
            print("Error in Agent1.py: "+str(e))
            capture_connected = False
    return cap
"""


def processDetection(cap, showFrame):
    while True:
        global  WIDTH, HEIGHT
        try:
            ret, frame = cap.read() 
            WIDTH = frame.shape[1]
            HEIGHT = frame.shape[0]
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            range_low, range_high, size_value, percentage_value = getValueRange()
            mask = cv2.inRange(hsv, range_low, range_high)
            
            target_info = getTargetInfo(mask, frame, size_value, percentage_value)
            target_input = target_info[0:2]
            target_square = target_info[2:]
            target_position = putCenter(frame)
            cv2.circle(frame, target_input, 2, (0,0,255), 2)
            if target_input[0] != -1:
                x_diff, y_diff = calculateDistanceFromCenter(target_position, target_input)
            else:
                x_diff, y_diff, target_square = 0,0, (-1,-1,-1,-1)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()
            if not showFrame:
                return  x_diff, y_diff
            else:
                (flag, encodedImage) = cv2.imencode(".jpg", frame)
                if not flag:
                    continue
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

        except Exception as e:
            print("Error in Agent1.py"+str(e))
            return  0, 0, -1
