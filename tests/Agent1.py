from ast import While
import cv2
import numpy as np
WIDTH = HEIGHT = 0
  
  
def getTargetInfo(mask=None, frame=None):
    try:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = sorted(contours, key=cv2.contourArea, reverse=True)
        contour = contour[0]  #largest contour found
        area = cv2.contourArea(contour)
        if(area > 1000):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Target", (x, y), cv2.FONT_HERSHEY_SIMPLEX,  1.0, (0, 255, 0))
            # print(f"{x}, {y}, {w}, {h}")
            x_center = x + ( w/2 )
            y_center = y + ( h/2 )
            return int(x_center), int( y_center ), x, y, w, h
    except:
        pass
    return -1,-1
def putCenter(frame):
    global WIDTH, HEIGHT
    x_center = int(WIDTH/2)
    y_center = int(HEIGHT/2)
    frame = cv2.circle(frame, (x_center, y_center), 20, (0,255,0), 5)
    return (x_center, y_center)

def calculateDistanceFromCenter(target_position, target_input):
    x_diff = target_position[0] - target_input[0]
    y_diff = target_position[1] - target_input[1]
    return -x_diff, y_diff
def run(vid, mode=""):
    global  WIDTH, HEIGHT
    ret, frame = vid.read()
    WIDTH = frame.shape[1]
    HEIGHT = frame.shape[0]
    # print(f"width: {WIDTH} height: {HEIGHT}")
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (61, 90, 60), (111, 255,126))
    # kernel = np.ones((7,7), np.uint8)
    # mask = cv2.erode(mask, kernel)    
    cv2.imshow('mask', mask)                    #mask view
    target_info = getTargetInfo(mask, frame)
    target_input = target_info[0:2]
    target_square = target_info[2:]
    target_position = putCenter(frame)
    cv2.circle(frame, target_input, 2, (0,0,255), 2)
    if target_input[0] != -1:
        x_diff, y_diff = calculateDistanceFromCenter(target_position, target_input)
    else:
        x_diff, y_diff, target_square = -1,-1, (-1,-1,-1,-1)
    # print(f"move x: {x_diff}  move y: {y_diff}")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()
    if mode == "test":
        cv2.putText(frame, "x: "+str(x_diff), (30,30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 1, cv2.LINE_AA )
        cv2.putText(frame, "y: "+str(y_diff), (300,30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 1, cv2.LINE_AA )
        cv2.imshow('target', frame)
        return  frame, x_diff, y_diff, target_square
    else:
        cv2.imshow('target', frame)
        return  x_diff, y_diff, target_square
        
    
if __name__=='__main__':
    vid = cv2.VideoCapture("http://192.168.50.22:9001/stream.mjpg")
    while True:
        x_diff, y_diff, target_square = run(vid,"")
        print(f" x:{x_diff} y:{y_diff} square{target_square}")