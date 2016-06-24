# -*- coding: utf-8 -*-
from algorithm.LineDetector import count_max_lines, count_continius_lines_and_sides, draw_line_x, draw_line_y, \
    get_lines_points
from utils.utils import binarize_cv_image, blank_cv_image
import numpy as np
import copy

__author__ = 'ava-katushka'

_RED = (255, 0, 0)
_YELLOW = (0, 255, 0)


class Line:
    def __init__(self, start, end, max_points, max_position):
        Line._check_line_position(start)
        Line._check_line_position(end)
        self.start = start
        self.end = end
        Line._check_line_points(max_points)
        self.max_points = max_points
        Line._check_line_position(max_position)
        self.max_position = max_position

    def thickness(self):
        return abs(self.end - self.start)

    def __unicode__(self):
        return 'Start: {0}, End: {1}. Thickness: {2}'.format(self.start, self.end, abs(self.end - self.start + 1))

    @classmethod
    def _check_line_position(cls, pos):
        if not 0 <= pos <= 30:
            raise ValueError('Invalid position')

    @classmethod
    def _check_line_points(cls, points):
        if not 0 <= points <= 30:
            raise ValueError('Invalid points num')


class HistogrammPiksDetector:
    @classmethod
    def horizontalHistogram(cls, points, lines, median):
        size = len(points)
        hist = blank_cv_image(size, size)
        for ind, p in enumerate(points):
            hist[ind:ind + 1, 0: p] = (0, 0, 0)
        for i in range(0, int(median)):
            draw_line_y(hist, i, _RED)
        for line in lines:
            for j in range(line.start, line.end + 1):
                draw_line_x(hist, j, _YELLOW)
        return hist

    @classmethod
    def verticalHistogram(cls, points, lines, median):
        size = len(points)
        hist = blank_cv_image(size, size)
        for ind, p in enumerate(points):
            hist[0: p, ind:ind + 1] = (0, 0, 0)
        for i in range(0, int(median)):
            draw_line_x(hist, i, _RED)
        for line in lines:
            for j in range(line.start, line.end + 1):
                draw_line_y(hist, j, _YELLOW)
        return hist

    @classmethod
    def getLinesOnPicture(cls, img, median_num=17, font=""):
        cls.median_num = median_num
        img = binarize_cv_image(img)
        #x_points, y_points = count_max_lines(img)
        x_points, y_points = count_continius_lines_and_sides(img,font)
        horizontal_lines, horizontal_median = HistogrammPiksDetector.getPiksLines(x_points)
        vertical_lines, vertical_median = HistogrammPiksDetector.getPiksLines(y_points)
        # print u"Горизонтальные линии:"
        # for line in horizontal_lines:
        #     print unicode(line)
        horiz_histogram = cls.horizontalHistogram(x_points, horizontal_lines, horizontal_median)
        vertical_histogram = cls.verticalHistogram(y_points, vertical_lines, vertical_median)
        return horizontal_lines, vertical_lines, horiz_histogram, vertical_histogram

    @classmethod
    def getBinarizedLines(cls, img, median_num=17):
        cls.median_num = median_num
        img = binarize_cv_image(img)
        x_points, y_points = count_max_lines(img)
        horizontal_lines = HistogrammPiksDetector.getPiksLinesBinarized(x_points)
        vertical_lines = HistogrammPiksDetector.getPiksLinesBinarized(y_points)
        return horizontal_lines, vertical_lines


    @classmethod
    def getHistogramLines(cls, img, median_num=17):
        cls.median_num = median_num
        img = binarize_cv_image(img)
        x_points, y_points = count_max_lines(img)
        return x_points, y_points

    @classmethod
    def getPiksLinesBinarized(cls, points):
        hist = copy.deepcopy(points)
        copy_hist = copy.deepcopy(hist)
        median = sorted(copy_hist)[-cls.median_num]
        hist = map(lambda x: 1 if x > median else 0, hist)
        return hist

    @classmethod
    def getPiksLines(cls, points):
        hist = copy.deepcopy(points)
        copy_hist = copy.deepcopy(hist)
        median = sorted(copy_hist)[-cls.median_num]

        hist = map(lambda x: x if x > median else 0, hist)
        lines = []
        in_line = False
        start = None
        end = None
        max = 0
        max_positon = 0
        for i, x in enumerate(hist):
            if x > 0 and not in_line:
                in_line = True
                start = i
                max = x
                max_positon = i
            if in_line and x > max:
                max = x
                max_positon = i
            if x == 0 and in_line:
                end = i - 1
                lines.append(Line(start, end, max, max_positon))
                in_line = False
                max = 0
        return lines, median
