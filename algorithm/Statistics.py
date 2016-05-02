from algorithm.LineDetector import LineDetector, ImageNoiser
from picture_generation.ChineseCharacterGenerator import ChineseCharacterGenerator
from utils.utils import PILtoCV

__author__ = 'ava-katushka'


def writePoints(file, x_points, y_points):
    for i in range(len(x_points)):
        file.write(str(x_points[i]) + ", ")
    for j in range(len(y_points) - 1):
        file.write(str(y_points[j]) + ", ")
    file.write(str(y_points[-1]) + "\n")


with open('line_detection_statistics.csv', 'w+') as file:
    file.write("Id, AllNum, Noise, ")
    for i in range(30):
        file.write("h" + str(i) + ", ")
    for j in range(29):
        file.write("v" + str(j) + ", ")
    file.write("v29\n")

    all = ChineseCharacterGenerator.all()

    i = 0
    all_num = 0
    magic_num = 9
    for character, inAllFonts in all.items()[:2000]:
        for signPicture in inAllFonts:
            cv_image = PILtoCV(signPicture.pilImageColor)
            x_points, y_points = LineDetector.getLinesOnPicture(cv_image)
            file.write(str(i) + ", " + str(all_num) + ",no, ")
            writePoints(file, x_points, y_points)
            i += 1
            for j in xrange(magic_num):
                image = ImageNoiser.Noise(cv_image)
                x_points, y_points = LineDetector.getLinesOnPicture(image)
                file.write(str(i) + ", " + str(all_num) + ",yes, ")
                writePoints(file, x_points, y_points)
                i += 1
            all_num += 1

