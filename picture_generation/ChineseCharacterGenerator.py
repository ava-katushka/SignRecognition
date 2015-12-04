# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os
import random
from SignPicture import SignPicture

#taken from http://stackoverflow.com/questions/1366068/whats-the-complete-range-for-chinese-characters-in-unicode
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
    fonts = ["simsun.ttc"]
    size = 200
    image_size = (size, size)
    image_format = "L"
    signes_codes = [[u"\u3400", u"\u4db5"], [u"\u4e00", u"\u9fd6"]]

    @classmethod
    def _randomFontName(cl):
        fontNum = random.randint(0, len(cl.fonts) - 1)
        fontName = cl.font_directory + cl.fonts[fontNum]
        return fontName

    @classmethod
    #returns random Chinese character in range of signes_codes
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
    def random(cl):
        fontName = cl._randomFontName()
        ttf=ImageFont.truetype(fontName, size=cl.size)
        sign = cl._randomChar()
        return SignPicture(sign, ttf, cl.image_size)


if __name__ == '__main__':
    image = ChineseCharacterGenerator.random()
    pixels = image.pilImageGrey.load()
    print pixels[0, 0]
    image.pilImageGrey.show()
