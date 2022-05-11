# In[1]
#-----------------------------------------------------------
#Program    :Ray_Sebastian_91044_Aufgabe_1.py
#Written by :Sebastian Ray
#Date       :02.04.2022
#Description:Read an image. Cut out a new Image using key combinations (mouse) an then process it further
#-----------------------------------------------------------
#pip install numpy
import numpy as np
import cv2 as cv

#get informations about OpenCV:
#https://docs.opencv.org/4.x/d7/dfc/group__highgui.html

#declare variable
windowName = "searchWally"
imgLoad = "Wally.png"
imgSave = "newWally"
imgHigh = 400                                       #high of the new image
imgWidth = 800                                      #width of the new image
polyCoordinates = []                                #Stores the coordinates of a polygon
ctr = 0

print("Press 's' to save the picture.\nPress 'q' to exit the program.")

cv.namedWindow(windowName)                          #creates a window that can be used as a placeholder for images

img = cv.imread(imgLoad)                            #loads an image from an specified file. Second Argument is an flag 
cv.rectangle(img,(520,70),(780,320),(255,0,0),4)    #draw a rectangle. (top-left)(bottom-right)(COLOR),thickness)

#mouse callback function
def draw_circle(event,x,y,flags,param):             #(event,x-coordinate,y-coordiante,flags,optional)
    if event == cv.EVENT_LBUTTONUP:                 #mouse events. 
        cv.circle(img,(x,y),10,(0,0,255),3)         #draw a circle.(img where drawn,centre,radius,color,thickness,?,?)
        if len(polyCoordinates) < 4:
            print("x=",x," y=",y)
            polyCoordinates.append([x,y])
        else:
            print("You already have 4 Points, press s to save the image!")

cv.setMouseCallback(windowName,draw_circle)         #set mouse handler for specified wondow (windows Name,callback function for mouse event)


while(1):
    cv.imshow(windowName,img)                       #display an image in a new Window. Image shown in original size
    key = cv.waitKey(20) & 0xFF                     #waits for an key event (115=s) or an delay in millisecond (ms)
    #save image
    if key == 115:                                  #save image
        if len(polyCoordinates) < 4:
            print("ERROR: You have to choose 4 Point, but only",len(polyCoordinates),"were given...")
        else:
            topL = [polyCoordinates[0][0],polyCoordinates[0][1]]    #list
            topR = [polyCoordinates[1][0],polyCoordinates[1][1]]
            botR = [polyCoordinates[2][0],polyCoordinates[2][1]]
            botL = [polyCoordinates[3][0],polyCoordinates[3][1]]

            mat1=np.float32([topL,topR,botR,botL])                                  #Ur-Coordinates
            mat2=np.float32([[0,0],[imgWidth,0],[imgWidth,imgHigh],[0,imgHigh]])    #New-Coordinates

            #warpPerspectivew = Transforms the source image (change viefwpoint) using the specified matrix (image,3x3 Matrix,size)
            #getPerspectiveTransform = Calculates a perspective transform from 4 pairs (source coordiantes,target coordinates)
            #https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gaf73673a7e8e18ec6963e3774e6a94b87
            imgNew=cv.warpPerspective(img,cv.getPerspectiveTransform(mat1,mat2),(imgWidth,imgHigh))
            cv.imshow("Transformed Image",imgNew)
            cv.imwrite(imgSave+str(ctr)+'.png',imgNew)              #saves an image to a specified file(filename,image)
            
            polyCoordinates=[]
            ctr=ctr+1
    elif key == 113:                                #program termination
        break                            


cv.destroyAllWindows()                              #destroys all the windows we created

# %%
