__author__ = 'ava-katushka'
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from PyQt4.QtGui import QImage, QPixmap


def PILtoQPixmap(pil_image):
    imageQt = ImageQt(pil_image)
    qimage = QImage(imageQt)
    return QPixmap(qimage)

class SignPicture:

    def __init__(self, sign, font, size, fontName):
        self.sign = sign
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.fontName = fontName
        self.pilImageGrey = Image.new("L", size, "white")
        ImageDraw.Draw(self.pilImageGrey).text((00,00), sign, fill='black', font=font)
        self.pilImageColor = Image.new("RGB", size, "white")
        ImageDraw.Draw(self.pilImageColor).text((00,00), sign, fill='black', font=font)
        self.pilImageBlackAndWhite = Image.new("1", size, "white")
        ImageDraw.Draw(self.pilImageBlackAndWhite).text((00,00), sign, fill='black', font=font)


    def isBlank(self):
        pixels = self.pilImageGrey.load()
        for i in range(0, self.width):
            for j in range (0, self.height):
                if pixels[i, j] != 255:
                    return False
        return True

    def draw_ellipse_on(self, point, color=128):
        image = self.pilImageColor
        draw = ImageDraw.Draw(image)
        r = 1
        leftCorner = (point[0] - r, point[1] - r)
        rightCorner = (point[0] + r, point[1] + r)
        draw.ellipse([leftCorner, rightCorner], fill=None, outline=color)
        del draw

    def getPixelsBlackAndWhite(self):
        return self.pilImageBlackAndWhite.load()

    def centerOfMass(self):
        pixels = self.pilImageGrey.load()
        mass = 0
        imoment = 0
        jmoment = 0
        for i in range(0, self.size[0]):
            for j in range (0, self.size[1]):
                inverted = 255 - pixels[i, j]
                imoment += i * inverted
                jmoment += j * inverted
                mass += inverted
        centerOfMass = [imoment / mass, jmoment / mass]
        #print centerOfMass
        return centerOfMass