__author__ = 'ava-katushka'
from algorithm.image_metrics import ImageMetrics
from algorithm.AlgorithmWrapper import AlgorithmWrapper
from picture_generation.ChineseCharacterGenerator import ChineseCharacterGenerator
from picture_generation.SignPicture import SignPicture
import pickle
import os
import numpy as np

class CellFeatureExtractor:
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
    allSetFile = _SCRIPT_ROOT + "/allSetFeatures.txt"

    @classmethod
    def features(cls, signPicture, binary=True):
        alg_image = AlgorithmWrapper(signPicture)
        alg_image.skeleton_image()
        features_1 = ImageMetrics.construct_description(alg_image.line_features.ends_of_line)
        features_2 = ImageMetrics.construct_description(alg_image.line_features.cross_of_line)
        result = features_1 + features_2
        if (binary):
            result = map(lambda x: 1 if x > 0 else 0, result)
        return result


    @classmethod
    def computeFeaturesInAllSet(cls, binary=True):
        allSet = {}
        allSet["X"] = []
        allSet["y"] = []
        picNum = 0
        all = ChineseCharacterGenerator.all()
        for sign, pic_in_fonts in all.items():
            for pic in pic_in_fonts:
                sign_features = cls.features(pic)
                sign_features = np.array(sign_features)
                allSet["X"].append(sign_features)
                allSet["y"].append(sign)
                picNum += 1
                if picNum % 1000 == 0:
                    print "Already {} pictures".format(picNum)
        with open(cls.allSetFile, "wb") as file:
            pickle.dump(allSet, file)

    @classmethod
    def allFeatures(cls):
        with open(cls.allSetFile, "r") as file:
            allFeaturesSet = pickle.load(file)
            print "all features set loaded"
            return allFeaturesSet


if __name__ == "__main__":
    sign = ChineseCharacterGenerator.random(30)
    CellFeatureExtractor.computeFeaturesInAllSet()
    allFeatures = CellFeatureExtractor.allFeatures()
    print len(allFeatures["X"][0])
    print len(allFeatures["X"])
    print len(allFeatures["y"])


