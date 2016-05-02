from algorithm.HistogrammPiksDetector import HistogrammPiksDetector
from metrics.Metrics import Metrics
from utils.utils import PILtoCV

__author__ = 'ava-katushka'


class PictureMetrics:
    @classmethod
    def get_lines_picture(cls, sign, median_num=17):
        image = sign.pilImageColor
        cv_image = PILtoCV(image)
        horizontal_lines, vertical_lines, horiz_histogram, vertical_histogram = HistogrammPiksDetector.getLinesOnPicture(
            cv_image, median_num)
        return horizontal_lines, vertical_lines

    @classmethod
    def dameray_levenstein_distance_sum(cls, sign1, sign2, median_num=17, weights=None):
        h_1, v_1 = cls.get_lines_picture(sign1, median_num)
        h_2, v_2 = cls.get_lines_picture(sign2, median_num)
        h_distance = Metrics.dameray_levenstein_distance(h_1, h_2, weights=weights)
        v_distance = Metrics.dameray_levenstein_distance(v_1, v_2, weights=weights)
        return h_distance + v_distance

    @classmethod
    def dameray_levenstein_distance_h(cls, sign1, sign2):
        h_1, v_1 = cls.get_lines_picture(sign1)
        h_2, v_2 = cls.get_lines_picture(sign2)
        h_distance = Metrics.dameray_levenstein_distance(h_1, h_2)
        return h_distance

    @classmethod
    def dameray_levenstein_distance_v(cls, sign1, sign2):
        h_1, v_1 = cls.get_lines_picture(sign1)
        h_2, v_2 = cls.get_lines_picture(sign2)
        v_distance = Metrics.dameray_levenstein_distance(v_1, v_2)
        return v_distance


