#-----------------------------------------------------------
#Program    :Ray_Sebastian_91044_Aufgabe_2.py
#Written by :Sebastian Ray
#Date       :21.04.2022
#Description:Read an image. Cut out a new Image using key combinations (mouse) and convert to RGBA (A=alpha)
#Questions:
#- Line  93: wieso ändert nur der erste Wert meine Bild-Transparenz in Graustufen? Müssten sich hier nich auch andere Farben auftun?
#- Line 103: Wieso funktioniert das? Wieso wird nur bei 3 ausgeblendet und bei 0-2 die farbe geändert?
#
#-----------------------------------------------------------
#pip install numpy
from cv2 import waitKey
import numpy as np
import cv2 as cv
import time
import pdb                  #Breakpoints
from tkinter import *
from tkinter import filedialog

from pandas import cut


#declare variable
windowName = "cutOuthWally"
imgSave = "newCutWally"
polyCoordinates = np.array([[0,0]])                         #Stores the coordinates of a polygon
polyCoordinates = np.delete(polyCoordinates,0,axis=0)       #workaround -> No Idea how to create an empty array
ctr = 0


def rescaleFrame(frame, scale=0.50):                                    #Adjust the size of an image
    """Changes the size of an images"""
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)    #resize the image


def loadNewPicture():
    #Opens a new directory
    imgLoad = filedialog.askopenfilename(initialdir="/04_BildVer/Praktikum/Aufgabenblatt2", title="Select A File", filetypes=(("png files", "*.png"),("jpg files", "*.jpg")))
    print("New image loaded!")    
    cv.namedWindow(windowName)                          #creates a window that can be used as a placeholder for images
    img1 = cv.imread(imgLoad)                           #loads an image from an specified file. Second Argument is an flag 
    img = rescaleFrame(img1,1)
    return img


img = loadNewPicture()


#mouse callback function
def draw_circle(event,x,y,flags,param):             #(event,x-coordinate,y-coordiante,flags,optional)
    global polyCoordinates
    if event == cv.EVENT_LBUTTONUP:                 #mouse events. 
        cv.circle(img,(x,y),3,(0,0,255),-1)         #draw a circle.(img where drawn,centre,radius,color,thickness)
        
        if len(polyCoordinates) < 40:
            print("x=",x," y=",y)
            polyCoordinates = np.append(polyCoordinates,[[x,y]], axis=0)    #Puts the points into an array
            if len(polyCoordinates) < 2:
                None
            else:
                cv.line(img,polyCoordinates[-2],(x,y),(0,0,255),thickness=2)    #Draws the lines between the points
        else:
            print("Stop, dont't overdo it. 20 Points are enough!!!")


cv.setMouseCallback(windowName,draw_circle)         #set mouse handler for specified wondow (windows Name,callback function for mouse event)


print("\n-------- Start Programm --------")
print("_________________________________")
print("|\t's' save picture\t|\n|\t'n' load new picture\t|\n|\t'q' exit program\t|\n|_______________________________|")


while(1):
    cv.imshow(windowName,img)                       #display an image in a new Window. Image shown in original size
    key = cv.waitKey(20) & 0xFF                     #waits for an key event (115=s) or an delay in millisecond (ms)
    #load picture
    if key == 110:
        img = loadNewPicture()
    #save image
    elif key == 115:                                  #save image
        if len(polyCoordinates) < 3:
            print("ERROR: You have to choose 3 Point, but only",len(polyCoordinates),"were given...")
        else:
            cv.line(img,polyCoordinates[0],polyCoordinates[-1],(0,0,255),thickness=2)   #Draws the last stroke. Last point to first point

            mask = np.zeros(img.shape[:2], dtype='uint8')       #Blank Black Picture
            #cv.imshow('mask',mask)                             #shows a blank black Image
            print("=> Mask shape: ",mask.shape)
            print("-->", polyCoordinates)
            cv.fillPoly(mask, [polyCoordinates], (255,0,0,0))                       #Fills the area bounded by the polygon (Image,PolygonArray,color)
            #cv.imshow('fillPoly',cv.fillPoly(mask, [polyCoordinates], (150,0,0)))  #shows the polygon in greyscale
            
            #Unnecessary. Only for interim output----------------------------------------------------------------------------------
            cutout = cv.bitwise_and(img,img,mask = mask)        #Return the cutout. Original Window size and position
            #cv.imshow('cutout',cutout)                         #shows the cutout in the original Image size. Without Alpha-Channel
            print("=> RGB shape: ",cutout.shape)
            #----------------------------------------------------------------------------------------------------------------------

            rgba = cv.cvtColor(cutout, cv.COLOR_RGB2RGBA)       #Converts an image from one color space to another. Insert Alpha-Channel
            rgba[:,:,3]=mask                                    #Copies everything from right to left (rgba[0:464,0:887,3]=mask)
            #cv.imshow('rgba',rgba)                             #shows the cutout in the original Image size. With the Alpha-Channel
            print("=> RGBA shape: ",rgba.shape)

            rect = cv.boundingRect(polyCoordinates)             #returns (x,y,w,h). Calculation of the new window size
            cropped = rgba[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]   #Crop the image to smaller image

            cv.imshow("Cropped Image" , cropped)
            cv.imwrite(imgSave+str(ctr)+'.png',cropped)         #saves an image to a specified file(filename,image)

            print("Image is cut out and saved...")

            polyCoordinates=np.array([[0,0]])                       #clears the array content
            polyCoordinates = np.delete(polyCoordinates,0,axis=0)   #workaround -> No Idea how to create an empty array

            ctr=ctr+1
    #program termination
    elif key == 113:                                
        print("\n-------- Programm is terminated --------\n")
        break    


cv.destroyAllWindows()                              #destroys all the windows we created
