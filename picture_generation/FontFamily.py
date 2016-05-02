from PIL import ImageFont

from picture_generation.SignPicture import SignPicture

__author__ = 'ava-katushka'
import os
import random


class FontFamily:
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
    font_directory = _SCRIPT_ROOT + "/fonts/"

    def __init__(self, fonts):
        self.fonts = fonts
        # simplified chinese
        self.signes_codes = [u"\u4e00", u"\u9fff"]
        self.pic_size = 30

    def get_sign(self, font, sign):
        font_name_full = os.path.join(FontFamily.font_directory, font)
        ttf = ImageFont.truetype(font_name_full, size=self.pic_size)
        return SignPicture(sign, ttf, (self.pic_size, self.pic_size), font)

    def get_signes(self, n=1000):
        result = []
        start = ord(self.signes_codes[0])
        end = ord(self.signes_codes[1])
        for i in range(start, end):
            picture_buf = []
            none_is_blank = True
            for font in self.fonts:
                picture = self.get_sign(font, unichr(i))
                if not picture.isBlank():
                    picture_buf.append(picture)
                else:
                    none_is_blank = False
                    break
            if none_is_blank:
                result.append(picture_buf)
            if len(result) >= n:
                break;
        return result

    def get_signes_random(self, n=1000):
        result = []
        start = ord(self.signes_codes[0])
        end = ord(self.signes_codes[1])
        while len(result) < n:
            picture_buf = []
            none_is_blank = True
            i = random.randint(start, end)
            for font in self.fonts:
                picture = self.get_sign(font, unichr(i))
                if not picture.isBlank():
                    picture_buf.append(picture)
                else:
                    none_is_blank = False
                    break
            if none_is_blank:
                result.append(picture_buf)
        return result

    @classmethod
    def get_all_families(cls):
        return [FontFamilyKaity(), FontFamilyFangsong(), FontFamilyWTC(), FontFamilySimsun()]


class FontFamilyKaity(FontFamily):
    def __init__(self):
        FontFamily.__init__(self, ["KaiTi_GB2312.ttf", "kaiti.ttf"])


class FontFamilyFangsong(FontFamily):
    def __init__(self):
        FontFamily.__init__(self, ["FangSong_GB2312.ttf", "fangsong.ttf"])


class FontFamilyWTC(FontFamily):
    def __init__(self):
        FontFamily.__init__(self, ["wts11.ttf", "WCL-07.ttf"])


class FontFamilySimsun(FontFamily):
    def __init__(self):
        FontFamily.__init__(self, ["simhei.ttf", "Hiragino Sans GB W3.otf"])
