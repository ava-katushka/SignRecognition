__author__ = 'ava-katushka'
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from PyQt4.QtGui import QImage, QPixmap


def PILtoQPixmap(pil_image):
    imageQt = ImageQt(pil_image)
    qimage = QImage(imageQt)
    return QPixmap(qimage)