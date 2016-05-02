# -*- coding: utf-8 -*-
__author__ = 'ava-katushka'
import cv2
import numpy as np
import os

_SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
name = "k.jpg"
img = cv2.imread(name)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 5
maxLineGap = 5
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite("lines" + name,img)