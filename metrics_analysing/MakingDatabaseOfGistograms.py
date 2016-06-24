from utils.utils import PILtoCV

__author__ = 'ava-katushka'
from algorithm.HistogrammPiksDetector import HistogrammPiksDetector
from picture_generation.ChineseCharacterGenerator import ChineseCharacterGenerator
import os
from utils.Timing import timing


class DatabaseMaker:
    def __init__(self):
        # 1000 signes takes 30 seconds (actually 7000 - because of fonts and blanks)
        # 10000 signes takes 433 seconds (actually - 69211)
        self.CHARACTERS_NUM = 10000
        self.picture_descriptioner = HistogrammPiksDetector.getHistogramLines #HistogrammPiksDetector.getBinarizedLines
        self._SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
        self.database_file = os.path.join(self._SCRIPT_ROOT, "picture_histogram_database.txt") #"picture_database.txt"
        self.reminder_num = 1000
        self.features_size = 30
        self.heading = self.make_heading()

    def make_heading(self):
        heading_array = []
        for i in range(self.features_size):
             heading_array.append("h" + str(i))
        for i in range(self.features_size):
             heading_array.append("v" + str(i))
        return "Id,SignOrd,Font," + ",".join(heading_array) + "\n"


    def write_line(self, file, i, sign, font, h_desc, v_desc):
        h_desc = self.description_to_str(h_desc)
        v_desc = self.description_to_str(v_desc)
        file.write(str(i) + "," + str(ord(sign)) + "," + font + "," + h_desc + "," + v_desc + "\n")

    def description_to_str(self, desc):
        return ",".join(map(str, desc))

    def all_to_characters(self, all):
        result = []
        for char, array in all.items():
            for sign in array:
                result.append(sign)
        return result

    @timing
    def create_database(self):
        all = ChineseCharacterGenerator.all(self.CHARACTERS_NUM)
        print "start len all", len(all)
        all = self.all_to_characters(all)
        print "unpacked len all", len(all)
        print "finish getting characters"
        with open(self.database_file, "w+") as file:
            file.write(self.heading);
            for i, sign in enumerate(all):
                image = sign.pilImageColor
                cv_image = PILtoCV(image)
                h_desc, v_desc = self.picture_descriptioner(cv_image)
                self.write_line(file, i,  sign.sign, sign.fontName, h_desc, v_desc)
                if i % self.reminder_num == 0:
                    print "Already written:", i
        print "Finally written", i


if __name__ == '__main__':
    dbmaker = DatabaseMaker()
    dbmaker.create_database()

