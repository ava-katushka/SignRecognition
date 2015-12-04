__author__ = 'ava-katushka'
import Skeletonization
from Skeletonization import *
from Algorithms import *
from LineFeatures import *
from PIL import Image

class AlgorithmWrapper:
    def __init__(self, sign_picture):
        self.sign_picture = sign_picture

    def center_of_mass(self):
        pixels = self.sign_picture.pilImageGrey.load()
        return centerOfMass(pixels, self.sign_picture.width, self.sign_picture.height)

    def skeleton_image(self):
        templateImageSkeletonization = TemplateImageSkeletonization(self.sign_picture.pilImageBlackAndWhite)
        self.skelet_image  = templateImageSkeletonization.skeletonization()
        self.line_features = LineFeatures(self.skelet_image)
        return self.skelet_image








