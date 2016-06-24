from utils.utils import PILtoCV

__author__ = 'ava-katushka'
from algorithm.LineDetector import get_symbol_description
from picture_generation.ChineseCharacterGenerator import ChineseCharacterGenerator
import os
from utils.Timing import timing


class DatabaseMaker:
    def __init__(self):
        # 1000 signes takes 30 seconds (actually 7000 - because of fonts and blanks)
        # 10000 signes takes 433 seconds (actually - 69211)
        self.CHARACTERS_NUM = 1000
        self.picture_descriptioner = get_symbol_description  # HistogrammPiksDetector.getBinarizedLines
        self._SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
        self.database_file = os.path.join(self._SCRIPT_ROOT, "picture_symbol_database3.txt")  # "picture_database.txt"
        self.reminder_num = 1000
        self.features_size = 30
        self.heading = "Id,SignOrd,Font,SymbolDescription\n"
        self.allowed_characters = ['l', 'c', 'r', 'lc', 'cr', 'lcr']

    def check(self, desc):
        first, second = desc.split(" ")
        letters_to_check = first + second.replace("u", "l").replace("m", "c").replace("d", "r")
        arr = letters_to_check.split(";")
        for letter in arr:
            if letter and not letter in self.allowed_characters:
                print letters_to_check + ":'" + letter + "'"
                return False
        return True

    def write_line(self, file, i, sign, font, desc):
        if (self.check(desc)):
            file.write(str(i) + "," + str(ord(sign)) + "," + font + "," + desc + "\n")
            return True
        else:
            return False

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
        k = 1
        with open(self.database_file, "w+") as file:
            file.write(self.heading)
            for i, sign in enumerate(all):
                image = sign.pilImageColor
                cv_image = PILtoCV(image)
                desc = self.picture_descriptioner(cv_image, sign.fontName)
                if sign.fontName != 'WCL-07.ttf' and sign.fontName != 'wts11.ttf' and self.write_line(file, k,
                                                                                                      sign.sign,
                                                                                                      sign.fontName,
                                                                                                      desc):
                    k = k + 1
                if k % self.reminder_num == 0:
                    print "Already written:", k
        print "Finally written", k


if __name__ == '__main__':
    dbmaker = DatabaseMaker()
    dbmaker.create_database()
