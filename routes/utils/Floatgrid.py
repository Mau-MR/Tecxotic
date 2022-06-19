import cv2
import numpy as np
from dataclasses import dataclass
import math
GRID_Y = 24
GRID_X = 48
HEIGHT = 600
WIDTH = 1150
base_image = np.zeros((HEIGHT,WIDTH,3), np.uint8)
base_image.fill(255)
FLOAT_SPEED = 0
FLOAT_ANGLE = 0
FLOAT_TIME = 0


@dataclass
class square:
    y: int
    x: int
    size: int = 20
    image: object = None
    def __post_init__(self):
        self.image = cv2.rectangle(base_image, (self.x*self.size,self.y*self.size), (self.x*self.size+self.size,self.y*self.size+self.size), (0,0,0), 2)

grid = dict()
for y in range(GRID_Y):
    for x in range(GRID_X):
        grid[(y,x)] = square(y = y+3,x = x+6)
cv2.putText(base_image, 'N', (int(WIDTH/2),30), cv2.FONT_HERSHEY_SIMPLEX,  1, (0,0,0), 2, cv2.LINE_AA)
cv2.putText(base_image, 'E', (int(WIDTH-30),int(HEIGHT/2)), cv2.FONT_HERSHEY_SIMPLEX,  1, (0,0,0), 2, cv2.LINE_AA)
cv2.putText(base_image, 'S', (int(WIDTH/2),int(HEIGHT-30)), cv2.FONT_HERSHEY_SIMPLEX,  1, (0,0,0), 2, cv2.LINE_AA)
cv2.putText(base_image, 'W', (30,int(HEIGHT/2)), cv2.FONT_HERSHEY_SIMPLEX,  1, (0,0,0), 2, cv2.LINE_AA)
cv2.line(base_image, ( 120,550 ), ( 320,550 ),  (0,0,255) , 2)
cv2.putText(base_image, '20 km', ( 190 , int(HEIGHT-30) ), cv2.FONT_HERSHEY_SIMPLEX,  .5, (0,0,0), 2, cv2.LINE_AA)


def getCollision(x_clicked,y_clicked):
    for y in range(GRID_Y):
        for x in range(GRID_X):
            if y_clicked > grid[(y,x)].y*grid[(y,x)].size and y_clicked < grid[(y,x)].y*grid[(y,x)].size+grid[(y,x)].size and x_clicked > grid[(y,x)].x*grid[(y,x)].size and x_clicked < grid[(y,x)].x*grid[(y,x)].size+grid[(y,x)].size:   
                # print(f"x:{x} y:{y}")
                to_return = (grid[(y,x)].x*grid[(y,x)].size, grid[(y,x)].y*grid[(y,x)].size, grid[(y,x)].x*grid[(y,x)].size+grid[(y,x)].size, grid[(y,x)].y*grid[(y,x)].size+grid[(y,x)].size)
                return to_return

def main(speed, angle, time, x, y):
    x = x - 1
    y = 24 - y
    global FLOAT_SPEED
    global FLOAT_ANGLE
    global FLOAT_TIME
    global base_image
    FLOAT_SPEED = speed
    FLOAT_ANGLE = angle
    FLOAT_TIME = time
    points =  (grid[(y,x)].x*grid[(y,x)].size, grid[(y,x)].y*grid[(y,x)].size, grid[(y,x)].x*grid[(y,x)].size+grid[(y,x)].size, grid[(y,x)].y*grid[(y,x)].size+grid[(y,x)].size)
    cv2.rectangle(base_image, (points[0], points[1]), (points[2], points[3]), (0,0,0), -1)
    SPEED_M_S = FLOAT_SPEED
    ANGLE = FLOAT_ANGLE
    HOURS = FLOAT_TIME
    speed_km_h = (SPEED_M_S * 60 * 60) / 1000
    distance = HOURS * speed_km_h
    print(f"Distance: {distance}")
    init_x = int(points[0]+(points[2]-points[0])/2)
    init_y =  int(points[1]+(points[3]-points[1])/2)
    end_y = distance * math.cos(math.radians(180 - ANGLE))
    end_x = distance * math.sin(math.radians(180 - ANGLE))
    # end_y = 16.71
    # end_x = 72.39
    print(f"x={end_x} y={end_y}")
    end_x = init_x + int(end_x * 10)
    end_y = init_y + int(end_y * 10)
    points = getCollision(end_x, end_y)
    cv2.rectangle(base_image, (points[0], points[1]), (points[2], points[3]), (0,0,255), -1)
    cv2.line(base_image, ( init_x , init_y ), (end_x, end_y ),  (255,0,0) , 2)
    return base_image

#main(0.143, 103, 144,6,15)
