__author__ = 'ava-katushka'
#Line features are end of lines and cross of lines
class LineFeatures:
    W = 255  # white pixel
    B = 0  # black pixel

    def __init__(self, skeleton_image):
        self.skeleton_image = skeleton_image
        self.ends_of_line = []
        self.cross_of_line = []
        self.calculate_features()

    def get3x3region(self, x, y):
        region = []
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                region.append(self.skeleton_image.getpixel((i,j)))
        return region

    def discover_region(self, region, x, y):
        center = region[4]
        #the center of 3x3 image is not black:
        #  so it could not be the end of line
        if center != LineFeatures.B:
            return
        else:
            black_points_num = region.count(LineFeatures.B)
            if black_points_num == 2:
                self.ends_of_line.append((x,y))
            elif black_points_num == 4:
                self.cross_of_line.append((x,y))

    #Line features are end of lines and cross of lines
    def calculate_features(self):
        for i in xrange(1, self.skeleton_image.size[0] - 1):
            for j in xrange(1, self.skeleton_image.size[1] - 1):
                region = self.get3x3region(i, j)
                self.discover_region(region, i, j)




