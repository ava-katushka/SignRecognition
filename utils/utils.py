__author__ = 'ava-katushka'
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from PyQt4.QtGui import QImage, QPixmap

# PIL to OpenCV using the new wrapper
from PIL import Image
import cv2
import numpy as np

#Converts picture from PIL image formal to cv(opencv) format
def PILtoCV(pil_img):
    cv_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
    return cv_img

#Converts picture from PIL image formal to QPixmap format
def PILtoQPixmap(pil_image):
    imageQt = ImageQt(pil_image)
    qimage = QImage(imageQt)
    return QPixmap(qimage)


#Converts picture from cv image to PIL format
def CVtoPIL(cv_img):
    pil_im = Image.fromarray(cv_img)
    return pil_im


def binarize_cv_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #(thresh, img) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return img

def blank_cv_image(height, width):
    white = 255
    blank_image = np.zeros((height,width,3), np.uint8)
    blank_image[:] = (white, white, white)
    return blank_image
