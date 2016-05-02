from algorithm.ImageNoiser import ImageNoiserCV
from utils.utils import binarize_cv_image

__author__ = 'ava-katushka'
# The algorithm to detect lines on the picture.
# Uses Hough Line Transform
# https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html?highlight=hough%20transform
import cv2
import os
import numpy as np
BLACK = (0, 0, 0)



def resizing_transform(point, factor):
    return point * factor + factor / 2


def is_black(pixel):
    return pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0


def count_max_lines(img):
    x_points = np.zeros(img.shape[0])
    y_points = np.zeros(img.shape[1])
    for i in xrange(img.shape[0]):
        for j in xrange(img.shape[1]):
            if is_black(img[i, j]):
                x_points[i] += 1
                y_points[j] += 1
    return x_points, y_points


def put_image_max_lines(x_points, y_points, histogram_x, histogram_y):
    x_lines, y_lines = [0] * len(x_points), [0] * len(y_points)
    threshold_x = sorted(x_points)[-5]
    for i in range(len(x_points)):
        x = x_points[i]
        if x >= threshold_x:
            histogram_x[i] += 1
            x_lines[i] += 1

    threshold_y = sorted(y_points)[-5]
    for j in range(len(y_points)):
        y = y_points[j]
        if y >= threshold_y:
            histogram_y[j] += 1
            y_lines[j] += 1

    return x_lines, y_lines


def draw_max_lines(img, x_points, y_points,  color_x=(255, 255, 0), color_y=(255, 0, 255)):
    threshold_x = sorted(x_points)[-5]

    for i in range(len(x_points)):
        x = x_points[i]
        if x >= threshold_x:
            draw_line_x(img, i, color_x)


    threshold_y = sorted(y_points)[-5]
    for j in range(len(y_points)):
        y = y_points[j]
        if y >= threshold_y:
            draw_line_y(img, j, color_y)

    print "x points: " + str(x_points)
    print "------"
    print "y points: " + str(y_points)
    print "------"



def draw_line_y(img, y, color=(0, 0, 255)):
    for i in xrange(img.shape[0]):
        if not is_black(img[i, y]):
            img[i, y] = color


def draw_line_x(img, x, color=(0, 0, 255)):
    for i in xrange(img.shape[1]):
        if not is_black(img[x, i]):
            img[x, i] = color


class LineDetector:
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))

    @classmethod
    def DrawLines(cls, img):
        img = binarize_cv_image(img)
        x_points, y_points = count_max_lines(img)
        draw_max_lines(img, x_points, y_points)

        return img

    @classmethod
    def form_report(cls, certainty, variance, threshold=5):
        report = ""
        min_value = sorted(certainty)[-threshold]
        for i in xrange(len(certainty)):
            if certainty[i] >= min_value:
                report += "Number {} Certainty: {:.2f} Variance {:.2f} \n".format(i, float(certainty[i])/26, variance[i])
        return report

    @classmethod
    def normalize_by_max_value(cls, v):
        max_v = max(v)
        for i in xrange(len(v)):
            v[i] = float(v[i]) / max_v


    @classmethod
    def getLinesOnPicture(cls, img):
        img = binarize_cv_image(img)
        x_points, y_points = count_max_lines(img)
        return x_points, y_points

    @classmethod
    def DrawLinesWithNoise(cls, img):
        img = binarize_cv_image(img)
        noise_pictures = 1
        histogram_x = np.zeros( img.shape[0])
        histogram_y = np.zeros( img.shape[1])
        sum_x = np.zeros( img.shape[0])
        sum_y = np.zeros(  img.shape[1])
        noise_img_return = ImageNoiserCV.Noise(img)
        for z in range(noise_pictures):
            noise_img = noise_img_return#ImageNoiser.Noise(img)
            noise_img = binarize_cv_image(noise_img)
            x_points, y_points = count_max_lines(noise_img)
            sum_x += x_points
            sum_y += y_points
            put_image_max_lines(x_points, y_points, histogram_x, histogram_y)
        histogram_x = np.array(histogram_x) / float(noise_pictures)
        histogram_y = np.array(histogram_y) / float(noise_pictures)
        average_x = sum_x / float(noise_pictures)
        average_y = sum_y / float(noise_pictures)
        print "Histogramm x: " + str(histogram_x)
        print "-----"
        print "Histogramm y: " + str(histogram_y)
        print "-----"
        print "Average x: " + str(average_x)
        print "-----"
        print "Average y: " + str(average_y)
        print "-----"

        x_points, y_points = count_max_lines(img)
        x_points, y_points = np.array(x_points), np.array(y_points)
        variance_x = (x_points - average_x)**2
        variance_y = (y_points - average_y)**2
        report = ""
        report += "Horizontal lines: \n"
        report += cls.form_report(x_points, variance_x)
        report += "Vertical lines: \n"
        report += cls.form_report(y_points, variance_y)
        print "Variance x: " + str(variance_x)
        print "-----"
        print "Variance y: " + str(variance_y)
        print "-----"
        img = noise_img_return

        for i in xrange(len(histogram_x)):
            x = histogram_x[i]
            if x > 0:
                draw_line_x(img, i, (255, 255, 255 - int(255 * x)))

        for i in xrange(len(histogram_y)):
            y = histogram_y[i]
            if y > 0:
                draw_line_y(img, i, (255,  255 - int(255 * y), 255))



        return img,report, noise_img_return


    # @classmethod
    # def DrawHoughLines(cls, img):
    #     # to graycolor
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     # to binary image
    #     (thresh, img_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #     # invert image
    #     img_inv = 255 - img_bw
    #     back_img = cv2.cvtColor(img_bw, cv2.COLOR_GRAY2RGB)
    #     # the algorithm
    #     lines = cv2.HoughLines(img_inv, 2, np.pi / 2, 15)
    #     print lines
    #     print '-----'
    #     factor = 6
    #     # resized_image = cv2.resize(img,None,fx=factor, fy=factor, interpolation = cv2.INTER_CUBIC)
    #     print img.shape
    #     x_max, y_max = img.shape[0] * 20, img.shape[1] * 20
    #
    #     if lines.any():
    #         for rho, theta in lines[0]:
    #             a = np.cos(theta)
    #             b = np.sin(theta)
    #             x0 = int(a * rho)
    #             y0 = int(b * rho)
    #             x1 = int(x0 + x_max * (-b))
    #             y1 = int(y0 + y_max * (a))
    #             x2 = int(x0 - x_max * (-b))
    #             y2 = int(y0 - y_max * (a))
    #
    #             if abs(theta - 1.57) <= 0.1:
    #                 draw_horizontal_line(back_img, y0)
    #                 # cv2.line(back_img, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #             else:
    #                 draw_vertical_line(back_img, x0)
    #                 # cv2.line(back_img, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #     else:
    #         print "Sorry, no lines"
    #         # cv2.imshow("image", img)
    #
    #         return back_img
