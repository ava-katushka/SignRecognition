__author__ = 'ava-katushka'
from collections import OrderedDict
import copy
# rotate region 3x3 represented by 9-dimention array
# right by 90 degree
def rotate(region):
    new = [None] * 9
    for i in xrange(len(region)):
        new_i = (i % 3) * 3 + (2 - i // 3)
        new[new_i] = region[i]
    return new


class TemplateImageSkeletonization:
    # basic templates for deletion:
    # 1 means white, 0 means black, -1 means does not matter
    # 3x3 template represented by 9-dimentional array
    W = 255  # white pixel
    B = 0  # black pixel
    G = -1  # grey (doesn't matter pixel)
    basic_templates = [
        [G, W, W, B, B, W, G, B, G],  # 1
        [G, B, G, B, B, W, G, W, W],  # 2
        [G, B, G, W, B, B, W, W, G],  # 3
        [W, W, G, W, B, B, G, B, G],  # 4
        [W, W, W, B, B, B, G, B, G],  # 5
        [G, B, W, B, B, W, G, B, W],  # 6
        [W, B, G, W, B, B, W, B, G],  # 7
        [G, B, G, B, B, B, W, W, W],  # 8
    ]
    noise_templates = [
        [W, W, W, W, B, W, W, W, W],  # 1
        [W, W, W, W, B, W, B, B, B],  # 2
        [W, W, W, W, B, W, B, B, W],  # 3
        [W, W, W, W, B, W, W, B, B],  # 4
    ]

    # generate more noise templates by rotation
    new_noise_templates = []
    for t in noise_templates[1:]:
        new_template = t
        for i in xrange(3):
            new_template = rotate(new_template)
            if not new_template in new_noise_templates:
                new_noise_templates.append(new_template)

    noise_templates += new_noise_templates

    def __init__(self, image):
        # image is list of lists
        # if 1, pixel is white, if 0, pixel is black
        self.image = copy.deepcopy(image)
        self.width = image.size[0]
        self.height = image.size[1]

    def skeletonization(self):
         pixels_to_delete = 1
         # repeat while where is something to delete
         iterations = 0
         while pixels_to_delete != 0:
            iterations += 1
            pixels_to_delete = self.delete_by_template(TemplateImageSkeletonization.basic_templates)
            #delete noise pixels
            if pixels_to_delete:
                self.delete_by_template(TemplateImageSkeletonization.noise_templates)
         return self.image

    def delete_by_template(self, templates):
        deleted_pixels = 0
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                if self.image.getpixel((i, j)) == TemplateImageSkeletonization.B and self.deletable(i, j, templates):
                    self.delete_pixel(i, j)
                    deleted_pixels += 1
        return deleted_pixels

    def deletable(self, x, y, templates):
        region3x3 = self.get3x3region(x, y)
        return self.check_if_center_deletable(region3x3, templates)

    def get3x3region(self, x, y):
        region = []
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                try:
                    region.append(self.image.getpixel((i,j)))
                except:
                    print (i,j)
        return region

    # checks if center of 3x3 region is possible to delete via skeletonisation
    def check_if_center_deletable(self, region, templates):
        for tmp in templates:
            if self.match_template(region, tmp):
                return True
        return False

    def match_template(self, obj, tmp):
        for x, t in zip(obj, tmp):
            if t == TemplateImageSkeletonization.G:
                continue  # Grey color means we don't care
            elif x != t:
                return False
        return True

    def delete_pixel(self, i, j):
        self.image.putpixel((i,j), TemplateImageSkeletonization.W)


if __name__ == "__main__":
    pass


