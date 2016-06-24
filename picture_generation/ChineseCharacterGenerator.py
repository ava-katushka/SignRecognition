# -*- coding: utf-8 -*-
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
import os
import random
from picture_generation.SignPicture import SignPicture
import pickle


# taken from http://stackoverflow.com/questions/1366068/whats-the-complete-range-for-chinese-characters-in-unicode
# Unicode currently has 74605 CJK characters. CJK characters not only includes characters used by Chinese, but also Japanese Kanji, Korean Hanja, and Vietnamese Chu Nom. Some CJK characters are not Chinese characters.
#
# 1) 20941 characters from the CJK Unified Ideographs block.
#
# Code points U+4E00 to U+9FCC.
#
# U+4E00 - U+62FF
# U+6300 - U+77FF
# U+7800 - U+8CFF
# U+8D00 - U+9FCC
# 2) 6582 characters from the CJKUI Ext A block.
#
# Code points U+3400 to U+4DB5. Unicode 3.0 (1999).
#
# 3) 42711 characters from the CJKUI Ext B block.
#
# Code points U+20000 to U+2A6D6. Unicode 3.1 (2001).
#
# U+20000 - U+215FF
# U+21600 - U+230FF
# U+23100 - U+245FF
# U+24600 - U+260FF
# U+26100 - U+275FF
# U+27600 - U+290FF
# U+29100 - U+2A6DF
# 3) 4149 characters from the CJKUI Ext C block.
#
# Code points U+2A700 to U+2B734. Unicode 5.2 (2009).
#
# 4) 222 characters from the CJKUI Ext D block.
#
# Code points U+2B740 to U+2B81D. Unicode 6.0 (2010).
#
# 5) CJKUI Ext E block.
#
# Coming soon
#
# If the above is not spaghetti enough, take a look at known issues. Have fun =)

class ChineseCharacterGenerator:
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
    font_directory = _SCRIPT_ROOT + "/fonts/"
    all_directory = _SCRIPT_ROOT + "/all/"
    ##"chinese.msyh.ttf","ufonts.com_microsoft-yahei.ttf" TODO: find normal yahel
    fonts = ["Hiragino Sans GB W3.otf", "KaiTi_GB2312.ttf", "FangSong_GB2312.ttf", "kaiti.ttf",
             "fangsong.ttf", "wts11.ttf", "WCL-07.ttf", "simhei.ttf", "simsun.ttc"]
    size = 200
    image_size = (size, size)
    image_format = "L"
    #signes_codes = [[u"\u3400", u"\u4db5"], [u"\u4e00", u"\u9fd6"]]
    #simplified chinese
    signes_codes = [[u"\u4e00", u"\u9fff"]]

    @classmethod
    def _randomFontName(cl):
        fontNum = random.randint(0, len(cl.fonts) - 1)
        fontName = cl.font_directory + cl.fonts[fontNum]
        return fontName


    @classmethod
    def sign_range(cls):
        return cls.signes_codes[0]

    @classmethod
    def _getNextFont(cl, fontname, j=1):
        i = cl.fonts.index(fontname)
        next = (i + j) % len(cl.fonts)
        return cl.fonts[next]

    @classmethod
    # returns random Chinese character in range of signes_codes
    def _randomChar(cl):
        fullrange = 0
        for range in cl.signes_codes:
            start = ord(range[0])
            end = ord(range[1])
            fullrange += end - start
        randNum = random.randint(0, fullrange)
        fullrange = 0
        for range in cl.signes_codes:
            start = ord(range[0])
            end = ord(range[1])
            if fullrange <= randNum <= fullrange + end - start:
                return unichr(randNum - fullrange + start)
            fullrange += end - start

    @classmethod
    def random(cl, size):
        fontName = cl._randomFontName()
        ttf = ImageFont.truetype(fontName, size=size)
        sign = cl._randomChar()
        shortFontName = fontName.split("/")[-1]
        return SignPicture(sign, ttf, (size, size), shortFontName)

    @classmethod
    def charInAllFonts(cl, char, size):
        result = []
        for font in cl.fonts:
            fontName = cl.font_directory + font
            ttf = ImageFont.truetype(fontName, size=size)
            picture = SignPicture(char, ttf, (size, size), font)
            if not picture.isBlank():
                result.append(picture)
        return result

    @classmethod
    def pickle_all_part(cl, part, num):
        with open("all/all" + str(num) + ".txt", "wb") as file:
            pickle.dump(part, file)

    #All simplified chinese in all Fonts
    #Very long operation, pickled result is availiable viam ChineseCharactorGenerator.all()
    @classmethod
    def computeAll(cl, size):
        result = {}
        num = 0
        for range in cl.signes_codes:
            start = ord(range[0])
            end = ord(range[1])
            for i in xrange(start, end):
                char = unichr(i)
                result[char] = cl.charInAllFonts(char, size)
                if i % 1000 == 0:
                    num += 1
                    print "{} characters already".format(i)
                    cl.pickle_all_part(result, num)
                    result = {}
        return result

    @classmethod
    def all(cl, size=None):
        result = {}
        num = 1
        onlyfiles = [f for f in os.listdir(cl.all_directory) if os.path.isfile(os.path.join(cl.all_directory, f))]
        onlyfiles = [f for f in onlyfiles if "all" in f]
        for fileName in onlyfiles:
            print fileName
            with open(cl.all_directory + fileName, "r") as file:
                part = pickle.load(file)
                result.update(part)
                if size and len(result) > size:
                    break
            print "Already loaded: {}".format(num)
            num += 1
        return result

    @classmethod
    def _charIteration(cl, signPicture, i):
        fontName = cl._getNextFont(signPicture.fontName, i)
        ttf = ImageFont.truetype(cl.font_directory + fontName, size=signPicture.width)
        sign = signPicture.sign
        return SignPicture(sign, ttf, signPicture.size, fontName)

    @classmethod
    def nextChar(cl, signPicture):
        return cl._charIteration(signPicture, 1)

    @classmethod
    def prevChar(cl, signPicture):
        return cl._charIteration(signPicture, -1)


if __name__ == '__main__':
    # image = ChineseCharacterGenerator.random(30)
    # pixels = image.pilImageGrey.load()
    # image.pilImageGrey.show()
    #ChineseCharacterGenerator.computeAll(30)
    # nums = defaultdict(lambda : 0)
    all = ChineseCharacterGenerator.all()
    # for char_fonts in all.values():
    #     nums[len(char_fonts)] += 1
    # for key, value in nums.items():
    #     print "{} times occurs {} characters".format(key, value)


