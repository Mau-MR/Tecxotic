import cv2
import numpy as np
WIDTH = HEIGHT = 0
  
  
def getTarget(mask=None, frame=None):
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
            return (int(x_center),int( y_center ))
            
    except:
        pass
    return -1,-1
def putCenter(frame):
    global WIDTH, HEIGHT
    x_center = int(WIDTH/2)
    y_center = int(HEIGHT/2)
    frame = cv2.circle(frame, (x_center, y_center), 20, (0,255,0), 5)
    return (x_center, y_center)

def calculate(target_position, target_input):
    x_diff = target_position[0] - target_input[0]
    y_diff = target_position[1] - target_input[1]
    return x_diff, y_diff
def run(vid):
    global  WIDTH, HEIGHT
    ret, frame = vid.read()
    cv2.resize(frame,(320,240))
    WIDTH = frame.shape[1]
    HEIGHT = frame.shape[0]
    # print(f"width: {WIDTH} height: {HEIGHT}")
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (40, 110, 0), (70, 255,200))
    kernel = np.ones((7,7), np.uint8)
    mask = cv2.erode(mask, kernel) 
    # cv2.imshow('mask', mask)   #see mask view
    target_input = getTarget(mask, frame)
    target_position = putCenter(frame)
    frame = cv2.circle(frame, target_input, 2, (0,0,255), 2)
    if target_input[0] != -1:
        x_diff, y_diff = calculate(target_position, target_input)
    else:
        x_diff, y_diff = 0,0
    # print(f"move x: {x_diff}  move y: {y_diff}")
    
    cv2.imshow('target', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()
        cv2.destroyAllWindows()
    return  x_diff, y_diff
    
  
