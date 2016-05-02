__author__ = 'ava-katushka'
import copy
import random
import cv2
import pandas as pd
import os


class ImageNoiser:
    width = 30
    height = 30
    pic_size = width * height
    color_num = 3
    pic_number = 100

    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
    random_works_df = pd.read_csv(os.path.join(_SCRIPT_ROOT, "random_works.csv"))
    random_color_df = pd.read_csv(os.path.join(_SCRIPT_ROOT, "random_color.csv"))

    @classmethod
    def random_works(cls):
        num = random.randint(0, 99)
        return num <= 1

    @classmethod
    def random_works_static(cls,ind):
        return cls.random_works_df['random_works'][ind]

    @classmethod
    def random_color(cls):
        return random.randint(0, 255)

    @classmethod
    def random_color_static(cls, ind):
        return cls.random_color_df['random_color'][ind]

    @classmethod
    def random_pixel(cls):
        return (cls.random_color(), cls.random_color(), cls.random_color())

    @classmethod
    def random_pixel_static(cls, ind):
        return (cls.random_color_static(ind), cls.random_color_static(ind + 1), cls.random_color_static(ind + 2))

    @classmethod
    def Noise(cls, pil_image):
        image = copy.deepcopy(pil_image)
        for j in xrange(ImageNoiser.height):
            for i in xrange(ImageNoiser.width):
                if cls.random_works():
                    image.putpixel((i, j), cls.random_pixel())
        return image

    @classmethod
    def NoiseNum(cls, pil_image, num):
        if num == 0:
            return pil_image
        image = copy.deepcopy(pil_image)
        offset = cls.pic_size * cls.color_num * (num - 1)
        ind = offset
        ind_pixel = offset
        for j in xrange(ImageNoiser.height):
            for i in xrange(ImageNoiser.width):
                if cls.random_works_static(ind):
                    image.putpixel((i, j), cls.random_pixel_static(ind_pixel))
                ind += 1
                ind_pixel += 3
        return image

    @classmethod
    def create_noise_doc(cls):
        doc_size = cls.pic_size * cls.color_num * cls.pic_number
        random_works_set = [cls.random_works() for x in xrange(doc_size)]
        df_randow_works = pd.DataFrame(data=random_works_set, columns=['random_works'])
        df_randow_works.to_csv('random_works.csv')

        random_color_set = [cls.random_color() for x in xrange(doc_size)]
        df_randow_color = pd.DataFrame(data=random_color_set, columns=['random_color'])
        df_randow_color.to_csv('random_color.csv')


class ImageNoiserCV:
    @classmethod
    def Noise(cls, cv_image):
        image = copy.deepcopy(cv_image)
        width = image.shape[0]
        height = image.shape[1]
        for j in xrange(height):
            for i in xrange(width):
                if cls.random_works():
                    image[i, j] = cls.random_pixel()
        image = cls.binarize_random(image)
        return image

    @classmethod
    def binarize_random(cls, img, frame=100):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        delta = random.randint(0, frame * 2)
        (thresh, img_bw) = cv2.threshold(gray, 28 + delta, 255, cv2.THRESH_BINARY)  # | cv2.THRESH_OTSU)
        img = cv2.cvtColor(img_bw, cv2.COLOR_GRAY2RGB)
        return img


if __name__ == "__main__":
    print ImageNoiser.create_noise_doc()
