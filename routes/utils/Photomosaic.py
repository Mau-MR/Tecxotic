#Companies that choose to stitch the images into a photomosaic autonomously are tasked with creating 
#software to “stitch” the images together. Companies may manually pilot their vehicle to any location to 
#take the eight individual images, but the program must “stitch” the images into a photomosaic. 
#Companies that successfully “stitch” the images together autonomously will receive 20 points. 
#Successfully “stitching” the images together autonomously is defined as no input from company 
#members other than taking the images.

import cv2
import time

images={}

def takePhoto(currPhoto, cap):
    leido, frame = cap.read()
            
    photoName = "photo" + str(currPhoto) + ".jpg"
    
    if leido:
        
        cv2.imwrite(photoName, frame)
        time.sleep(2)
        print("Photo taken correctly")
    else:
        print("Error accessing the camera")


def photomosaic():
        
    for i in range(8): # 8 images
        images[i]=cv2.imread(f"photo{i+1}.jpg") #  # of Images
        print("photoName: ", f"photo{i+1}.jpg")
        #Resize
        images[i]=cv2.resize(images[i],(317,360))
        #print("kiti")
           
    #Stack 
    stack1=cv2.hconcat([images[0],images[1],images[2],images[3]])
    stack2=cv2.hconcat([images[4],images[5],images[6],images[7]])
    stack3=cv2.vconcat([stack1,stack2])

    ###########
    cv2.imwrite('photomosaic.jpg',stack3)


