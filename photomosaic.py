#Companies that choose to stitch the images into a photomosaic autonomously are tasked with creating 
#software to “stitch” the images together. Companies may manually pilot their vehicle to any location to 
#take the eight individual images, but the program must “stitch” the images into a photomosaic. 
#Companies that successfully “stitch” the images together autonomously will receive 20 points. 
#Successfully “stitching” the images together autonomously is defined as no input from company 
#members other than taking the images.

import cv2
import glob
import os
import time
import pickle #to storage values and reuse them
import shutil
    
cap = cv2.VideoCapture(0,  cv2.CAP_DSHOW) #camera number

#directory = r"C:\Users\anton\OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey\Universidad TEC21\TECXOTIC\Software\Photomosaic\photos"
#mainDirectory = r"C:\Users\anton\OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey\Universidad TEC21\TECXOTIC\Software\Photomosaic"

directory = r"\photos"
#mainDirectory = "../photos/"
backwards = r".."

ext = "jpg"
images={}
currPhoto = 0 #index of the current photo
pickleFile = 'currentPhoto.pk' # name of the pickle file




def takePhoto(currPhoto):
    leido, frame = cap.read()
            
    photoName = "photo" + str(currPhoto+1) + "." + ext
    
    if leido and currPhoto<8:
        
        cv2.imwrite(photoName, frame)
        time.sleep(2)
        print("Photo taken correctly")

    else:
        print("Error accessing the camera")
    
    


def resizeAndStack():
        
    for i in range(8): # 8 images
        images[i]=cv2.imread(f"photo{i+1}.jpg") #  # of Images
        print("photoName: ", f"photo{i+1}.jpg")
        #Resize
        images[i]=cv2.resize(images[i],(200,200))
        print("kiti")
           
    #Stack 
    stack1=cv2.hconcat([images[0],images[1],images[2],images[3]])
    stack2=cv2.hconcat([images[4],images[5],images[6],images[7]])
    stack3=cv2.vconcat([stack1,stack2])

    #os.chdir(mainDirectory)

    ###########
    os.chdir(backwards)
    ##########



    cv2.imwrite('photomosaic.jpg',stack3)
    cv2.waitKey(0)
    cv2.destroyAllWindows
    
    
def main():
    # starts at main directory
    global currPhoto

    ###### UNPICKLING IF FILE EXISTS######
    try:
        infile = open(pickleFile,'rb')
        currPhoto = pickle.load(infile)
        infile.close()

    except:
        currPhoto = 0
        print('First time running the program')
    #####################################

    ##############
    if currPhoto>=8:
        currPhoto = 0
        
    takePhoto(currPhoto)
    currPhoto += 1

    ###########
    os.chdir(backwards)
    ##########

    ###### PICKLING currPhoto ######
    outfile = open (pickleFile, 'wb')
    pickle.dump(currPhoto,outfile)
    outfile.close()
    ################################

    if currPhoto<8:
        return True

    else:
        currPhoto = 0
        
        os.chdir(os.getcwd() + directory)
        resizeAndStack()

        ################# DELETE ALL THE PHOTOS INSIDE "photos" #######################################################
        '''os.chdir(directory)
        
        for i in range(8):
            os.remove("photo" + str(i+1) + "." + ext)'''
        ###############################################################################################################

        ################ DELETE THE PHOTOS DIRECTORY WITH IT'S FILES, THEN CREATING IT AGAIN EMPTY ####################
        shutil.rmtree(os.getcwd() + directory) 
        os.mkdir(os.getcwd() + directory)
        ###############################################################################################################
    cap.release()

