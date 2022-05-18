#-----------------------------------------------------------
#Program    :Ray_Sebastian_91044_Aufgabe_3.py
#Written by :Sebastian Ray
#Date       :13.05.2022
#Description:
#Questions:
#
#
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
    imgLoad = filedialog.askopenfilename(initialdir="/04_BildVer/Praktikum/Aufgabenblatt3", title="Select A File", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
    cv.namedWindow(windowName)                          #creates and show a window that can be used as a placeholder for images
    img1 = cv.imread(imgLoad, flags=cv.IMREAD_UNCHANGED)#loads an image from an specified file. Second Argument is an flag
    print("New image loaded!")    
    img = rescaleFrame(img1,1)
    return img
    

img = loadNewPicture()
img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
template = loadNewPicture()
rows,cols,_=template.shape
# print(">",img.shape)
# print(">",template.shape)


def moveImgOverPicture(event,x,y,flags,param):             #(event,x-coordinate,y-coordiante,flags,optional)
    if event == cv.EVENT_MOUSEMOVE:                        #mouse events. 
        imgCopy = img.copy()
        
        # I want to put logo on top-left corner, So I create a ROI (Region of Interest)
        roi = imgCopy[y:(rows+y), x:(cols+x)]       

        # Now create a mask of logo and create its inverse mask also
        mask=template[...,3]
        #_, mask = cv.threshold(templateGray, 0, 255, cv.THRESH_TRIANGLE)#mask=template[...,3]
        mask_inv = cv.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        img1_bg = cv.bitwise_and(roi,roi,mask=mask_inv)
        # Take only region of logo from logo image.
        img2_fg = cv.bitwise_and(template,template,mask=mask)
        # Put logo in ROI and modify the main image
        dst =cv.add(img1_bg,img2_fg)
        
        imgCopy[y:(rows+y), x:(cols+x)] = dst

        res = cv.matchTemplate(roi,template,cv.TM_SQDIFF_NORMED)    
        imgCopy = cv.putText(imgCopy,str(res),(10,40),cv.FONT_HERSHEY_COMPLEX,1,(0,0,0),2,cv.LINE_AA)
        cv.imshow(windowName, imgCopy)
        


cv.setMouseCallback(windowName,moveImgOverPicture)         #set mouse handler for specified wondow (windows Name,callback function for mouse event)

print("\n-------- Start Programm --------")
print("_________________________________")
print("|\t'q' exit program\t|\n|_______________________________|")


while(1):
    #cv.imshow(windowName,img)                       #display an image in a new Window. Image shown in original size
    key = cv.waitKey(20) & 0xFF

    #program termination
    if key == 113:                                
        print("\n-------- Programm is terminated --------\n")
        break 


cv.destroyAllWindows()                              #destroys all the windows we created
