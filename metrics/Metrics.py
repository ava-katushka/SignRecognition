__author__ = 'ava-katushka'
import numpy as np

class Metrics:
    @classmethod
    def count_distance(cls, x_lines, y_lines):
        x_str = cls.binarize(x_lines)
        y_str = cls.binarize(y_lines)
        return cls._levenstein_distance(x_str, y_str)

    @classmethod
    def levenstein_distance(cls, x_lines, y_lines):
        x_str = cls.binarize(x_lines)
        y_str = cls.binarize(y_lines)
        return cls._levenstein_distance(x_str, y_str)

    @classmethod
    def dameray_levenstein_distance(cls, x_lines, y_lines, weights=None):
        x_str = cls.binarize(x_lines)
        y_str = cls.binarize(y_lines)
        return cls._dameray_levenstein_distance(x_str, y_str, weights)


    @classmethod
    def dameray_levenstein_distance_hist(cls, hist1, hist2, weights=None):
        horizontal_dist = cls._dameray_levenstein_distance(hist1[0], hist2[0], weights=weights)
        vertical_dist = cls._dameray_levenstein_distance(hist1[1], hist2[1],  weights=weights)
        return (horizontal_dist, vertical_dist)

    @classmethod
    def binarize(cls, lines, size=30):
        array = [0] * size
        for line in lines:
            for i in range(line.start, line.end + 1):
                array[i] = 1
        return array


    @classmethod
    def _levenstein_distance(cls, x_str, y_str, size=30):
        array = np.zeros((size + 1, size + 1))
        for j in range(0, size + 1):
            array[0][j] = j
        for i in range(0, size + 1):
            array[i][0] = i
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                up = array[i][j - 1]
                left = array[i - 1][j]
                diag = array[i - 1][j - 1]
                alike_price = 1
                if x_str[i - 1] == y_str[j - 1]:
                    alike_price = 0
                array[i][j] = min(up + 1, left + 1, diag + alike_price)
        return array[size][size]

    #weights[0] - price deleting
    #weights[1] - price adding
    #weights[2] - price replacing
    #weights[3] - price transposition
    @classmethod
    def _dameray_levenstein_distance(cls, x_str, y_str,weights=None, size=30):
        if weights is None:
            weights = (1., 1., 1., 1.)
        n = size + 1
        array = np.zeros((n, n))
        for j in range(0, size + 1):
            array[0][j] = j
        for i in range(0, size + 1):
            array[i][0] = i
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                up = array[i][j - 1]
                left = array[i - 1][j]
                diag = array[i - 1][j - 1]
                diag_2 = array[i - 2][j - 2]
                alike_price = weights[2]
                if x_str[i - 1] == y_str[j - 1]:
                    alike_price = 0
                array[i][j] = min(up + weights[0], left + weights[1], diag + alike_price)
                if i > 1 and j > 1 and x_str[i - 1] == y_str[j - 2] and x_str[i - 2] == y_str[j - 1]:
                    array[i][j] = min(array[i][j], diag_2 + weights[3])
        return array[size][size]





