#-----------------------------------------------------------
#Program    :Ray_Sebastian_91044_Aufgabe_4.py
#Written by :Sebastian Ray
#Date       :05.06.2022
#Description:Heatmap generation and pattern matching
#Questions:
#
#
#
#-----------------------------------------------------------
from cv2 import waitKey
import numpy as np
import cv2 as cv
import time
import pdb                  #Breakpoints
from tkinter import *
from tkinter import filedialog

from pandas import cut


headMapWithWallyImage = "HeadMapWithWallyImage"
searchWallyImage = "SearchWallyImage"
headMapImage = "HeadMapImage"


def loadNewPicture():
    #Opens a new directory
    imgLoad = filedialog.askopenfilename(initialdir="/04_BildVer/Praktikum/Aufgabenblatt3", title="Select A File", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
    cv.namedWindow(headMapWithWallyImage)                          #creates and show a window that can be used as a placeholder for images
    img1 = cv.imread(imgLoad, flags=cv.IMREAD_UNCHANGED)#loads an image from an specified file. Second Argument is an flag
    print("New image loaded!")    
    return img1


def headMapMethod(searchWally,template):
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    methods = eval(methods[1])

    #Converts an image from one color space to another. Insert Alpha-Channel
    searchWally=cv.cvtColor(searchWally,cv.COLOR_RGBA2RGB)
    #template Höhe/Breite des templates bestimmen
    height0,width0,_=searchWally.shape[:3]
    height,width,_ = template.shape[:3]

    #create Mask
    templ = template[:,:,0:3]
    alpha = template[:,:,3]     #takes only the alpha channel

    #https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
    compare = cv.matchTemplate(searchWally,templ,methods)               #Compares a template against overlapped image regions
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(compare)          #Finds the global minimum and maximum in an array
    top_left = max_loc
    compare = cv.resize(compare,(width0,height0),interpolation=cv.INTER_AREA)
    
    #Normalize (thanks to karsten). Changes the intensity level. Better Contrast
    #https://www.delftstack.com/de/howto/python/opencv-normalize/
    compareIntensity=None
    compareIntensity=cv.normalize(compare,compareIntensity,alpha=0,beta=255,norm_type=cv.NORM_MINMAX,dtype=cv.CV_8U)
    cv.imshow(headMapImage,compareIntensity)

    compareIntensity=cv.cvtColor(compareIntensity,cv.COLOR_GRAY2RGB)
    # I want to put logo on top-left corner, So I create a ROI (Region of Interest)
    roi=compareIntensity[top_left[1]:top_left[1]+height,top_left[0]:top_left[0]+width]
    
    mask_inv = cv.bitwise_not(alpha)
    # Now black-out the area of logo in ROI
    compareIntensity_bg = cv.bitwise_and(roi,roi,mask=mask_inv)
    # Take only region of logo from logo image.
    compareIntensity_fg = cv.bitwise_and(templ,templ,mask=alpha)
    # Put logo in ROI and modify the main image
    dst =cv.add(compareIntensity_bg,compareIntensity_fg)

    compareIntensity[top_left[1]:top_left[1]+height,top_left[0]:top_left[0]+width]=dst
    
    cv.imshow(searchWallyImage,searchWally)
    cv.imshow(headMapWithWallyImage,compareIntensity)



searchWally = loadNewPicture()
template = loadNewPicture()
headMapMethod(searchWally,template)


while True:
    key = cv.waitKey(20) & 0xFF
    
    #program termination
    if key == 113:
        print("\n-------- Programm is terminated --------\n")
        break
    
    #load picture
    elif key == 110:
        #load picture
        searchWally = loadNewPicture()
        template = loadNewPicture()
        headMapMethod(searchWally,template)

cv.destroyAllWindows()
