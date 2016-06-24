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


def is_black_or_grey(pixel):
    return pixel[0] < 200 and pixel[1] < 200 and pixel[2] < 200


def is_black_or_grey_one(pixel):
    return pixel < 200


def count_max_lines(img):
    # x_points = np.zeros(img.shape[0], dtype=np.int8)
    # y_points = np.zeros(img.shape[1], dtype=np.int8)
    # for i in xrange(img.shape[0]):
    #     for j in xrange(img.shape[1]):
    #         if is_black(img[i, j]):
    #             x_points[i] += 1
    #             y_points[j] += 1
    # return x_points, y_points
    return count_continius_lines_and_sides(img)


def count_continius_lines(img):
    x_points = np.zeros(img.shape[0], dtype=np.int8)
    y_points = np.zeros(img.shape[1], dtype=np.int8)

    for i in xrange(img.shape[0]):
        black_length = 0
        for j in xrange(img.shape[1]):
            if is_black(img[i, j]):
                black_length += 1
            else:
                if black_length >= 6:
                    x_points[i] += black_length
                black_length = 0

    for j in xrange(img.shape[1]):
        black_length = 0
        for i in xrange(img.shape[0]):
            if is_black(img[i, j]):
                black_length += 1
            else:
                if black_length >= 6:
                    y_points[j] += black_length
                black_length = 0
    return x_points, y_points


def get_type(start, end, threshold=6, center=15):
    step = threshold / 2
    if end < center + step:
        return 'l,'
    if start > center - step:
        return 'r,'
    if start <= center - step and end >= center + step:
        result = ''
        if start < center - threshold:
            result += 'l'
        result += 'c'
        if end > center + threshold:
            result += 'r'
        result += ','
        return result


# 01234
# L-C-R
def get_type_in_bits(start, end, bits, threshold=6, center=15):
    step = threshold / 2
    if end < center + step:
        bits[0] = True
    if start > center - step:
        bits[4] = True
    if start <= center - step and end >= center + step:
        if start < center - threshold:
            bits[0] = True
            bits[1] = True
        bits[2] = True
        if end > center + threshold:
            bits[3] = True
            bits[4] = True
    return bits


def to_h(res):
    res = res.replace('l', 'u')
    res = res.replace('c', 'm')
    res = res.replace('r', 'd')
    return res


def concatenate(result, prev):
    if prev.replace(',', '') in result.replace(',', ''):
        return result
    if result.replace(',', '') in prev.replace(',', ''):
        return prev
    return result + prev


def unite_str(st):
    result = ''
    prev = ''
    for s in st:
        if s != '' and prev == '':
            prev += s
            continue
        if s != '' and prev != '':
            if (s == 'l,' and prev == 'r,') or (s == 'r,' and prev == 'l,'):
                result += prev + ';'
                prev = s
            else:
                prev = concatenate(prev, s)
            continue
        if s == '' and prev != '':
            result += prev + ';'
            result = result.replace(',;', ';')
            prev = ''
    if prev != '':
        result += prev + ';'
        result = result.replace(',;', ';')
    result = result.replace('r,c;', 'cr;')
    result = result.replace('l,c;', 'lc;')
    result = result.replace('r,c,l;', 'lcr;')
    result = result.replace('c,l;', 'lc;')
    result = result.replace('cr,l;', 'lcr;')
    result = result.replace('r,lc;', 'lcr;')
    result = result.replace('l,cr;', 'lcr;')
    result = result.replace('clcr;', 'lcr;')
    result = result.replace('l,c,r;', 'lcr;')
    return result


def unite_str_streight(st):
    if not st:
        return ""
    prev = st[0]
    if prev[:-1]:
        result = prev[:-1] + ";"
    else:
        result = ""
    for letter in st[2:]:
        if letter[:-1] and letter != prev:
            result += letter[:-1] + ";"
            prev = letter
    return result


def unite_string(st, font):
    if font == "simhei.ttf":
        return unite_str_streight(st)
    return unite_str(st)


def get_threshold_and_center(font):
    h_threshold, v_threshold = 6, 6
    h_center, v_center = 15, 15
    if font == 'KaiTi_GB2312.ttf':
        h_threshold = 6
        v_threshold = 6
    if font == 'fangsong.ttf':
        h_threshold = 8
        v_threshold = 8
        h_center = 16
    if font == 'wts11.ttf':
        h_threshold = 6
        v_threshold = 8
    if font == 'WCL-07.ttf':
        h_threshold = 8
        v_threshold = 8
    if font == 'simhei.ttf':
        h_threshold = 8
        v_threshold = 10
    if font == 'simsun.ttf':
        h_threshold = 10
        v_threshold = 10
    if font == 'kaiti.ttf':
        h_threshold = 6
        v_threshold = 7
        h_center = 16
    if font == "Hiragino Sans GB W3.otf":
        h_threshold = 10
        v_threshold = 10
        h_center = 16

    return h_threshold, v_threshold, h_center, v_center


symbol_dict = {(1, 0, 0, 0, 0): "l;", (1, 1, 1, 0, 0): "lc;", (1, 1, 1, 1, 1): "lcr;", (0, 0, 1, 1, 1): "cr;",
               (0, 0, 0, 0, 1): "r;",
               (1, 0, 0, 0, 1): "l;r;", (0, 0, 1, 0, 0): "c;", (1, 0, 1, 0, 0): "l;c;", (1, 1, 1, 0, 1): "lc;r;",
               (1, 0, 1, 1, 1): "l;cr;",
               (1, 0, 1, 0, 1): "l;c;r;", (0, 0, 1, 0, 1): "r;c;"}


def to_string(bits, font=""):
    result = symbol_dict[tuple(bits)]
    if font == "fangsong.ttf" or font == "kaiti.ttf":
        result = result.replace("r;c;", "cr;")
    return result


def get_threshold_and_center_by_raw_image(img):
    h_center, v_center = img.shape[0] / 2, img.shape[1] / 2
    h_threshold, v_threshold = 0, 0
    for i in range(img.shape[0]):
        black_length = 0
        for j in range(img.shape[1]):
            if is_black_or_grey_one(img[i, j]):
                black_length += 1
            else:
                h_threshold = max(h_threshold, black_length)
                black_length = 0
        h_threshold = max(h_threshold, black_length)
    h_threshold /= 3
    for j in range(img.shape[1]):
        black_length = 0
        for i in range(img.shape[0]):
            if is_black_or_grey_one(img[i, j]):
                black_length += 1
            else:
                v_threshold = max(v_threshold, black_length)
                black_length = 0
        v_threshold = max(v_threshold, black_length)
    v_threshold /= 3
    return h_threshold, v_threshold, h_center, v_center


def get_symbol_lines(img, threshold, center, font="", is_black_pixel=is_black_or_grey):
    bits = [False, False, False, False, False]
    result = ""
    for i in range(img.shape[0]):
        black_length = 0
        black_start = 0
        was_black = False
        for j in range(img.shape[1]):
            if is_black_pixel(img[i, j]):
                black_length += 1
            else:
                if black_length >= threshold:
                    was_black = True
                    bits = get_type_in_bits(black_start, j, bits, threshold, center)
                black_length = 0
                black_start = j + 1
        if black_length >= threshold:
            was_black = True
            bits = get_type_in_bits(black_start, img.shape[1], bits, threshold, center)
        if not was_black and True in bits:
            result += to_string(bits, font)
            bits = [False, False, False, False, False]

    if True in bits:
        result += to_string(bits, font)
    return result


def get_symbol_description_unknown(img):
    h_threshold, v_threshold, h_center, v_center = get_threshold_and_center_by_raw_image(img)
    h_lines = get_symbol_lines(img, h_threshold, h_center, is_black_pixel=is_black_or_grey_one)
    v_lines = get_symbol_lines(img.transpose(), v_threshold, v_center, is_black_pixel=is_black_or_grey_one)
    v_lines = to_h(v_lines)
    return h_lines + " " + v_lines


def get_symbol_description(img, font):
    h_threshold, v_threshold, h_center, v_center = get_threshold_and_center(font)
    h_lines = get_symbol_lines(img,  h_threshold, h_center, font)
    v_lines = get_symbol_lines(img.transpose((1, 0, 2)), v_threshold, v_center, font)
    v_lines = to_h(v_lines)
    return h_lines + " " + v_lines


def get_lines_points(img, font):
    h_threshold, v_threshold, h_center, v_center = get_threshold_and_center(font)
    x_points = np.zeros(img.shape[0], dtype=np.int8)
    y_points = np.zeros(img.shape[1], dtype=np.int8)
    for i in xrange(img.shape[0]):
        black_length = 0
        for j in xrange(img.shape[1]):
            if is_black_or_grey(img[i, j]):
                black_length += 1
            else:
                if black_length >= h_threshold:
                    x_points[i] += black_length
                black_length = 0
        if black_length >= h_threshold:
            x_points[i] += black_length

    for j in xrange(img.shape[1]):
        black_length = 0
        for i in xrange(img.shape[0]):
            if is_black_or_grey(img[i, j]):
                black_length += 1
            else:
                if black_length >= v_threshold:
                    y_points[j] += black_length
        if black_length >= v_threshold:
            y_points[j] += black_length
    return x_points, y_points


def count_continius_lines_and_sides(img, font):
    h_threshold, v_threshold, h_center, v_center = get_threshold_and_center(font)
    x_points = np.zeros(img.shape[0], dtype=np.int8)
    y_points = np.zeros(img.shape[1], dtype=np.int8)
    x_points_str = [''] * img.shape[0]
    y_points_str = [''] * img.shape[1]

    for i in xrange(img.shape[0]):
        black_length = 0
        black_start = 0
        for j in xrange(img.shape[1]):
            if is_black_or_grey(img[i, j]):
                black_length += 1
            else:
                if black_length >= h_threshold:
                    x_points[i] += black_length
                    x_points_str[i] += get_type(black_start, j, h_threshold, h_center)
                black_length = 0
                black_start = j + 1
        if black_length >= h_threshold:
            x_points[i] += black_length
            x_points_str[i] += get_type(black_start, j, h_threshold, h_center)
    # print "----------"
    # print "Horizontal:"
    # for st in x_points_str:
    #     if st:
    #         print st
    # print (unite_string(x_points_str, font))

    for j in xrange(img.shape[1]):
        black_length = 0
        black_start = 0
        for i in xrange(img.shape[0]):
            if is_black_or_grey(img[i, j]):
                black_length += 1
            else:
                if black_length >= v_threshold:
                    y_points[j] += black_length
                    y_points_str[j] += get_type(black_start, i, v_threshold, v_center)
                black_length = 0
                black_start = i + 1
        if black_length >= v_threshold:
            y_points[j] += black_length
            y_points_str[j] += get_type(black_start, i, v_threshold, v_center)

    # print "----------"
    # print "Vertical:"
    # for st in y_points_str:
    #     if st:
    #         print to_h(st)
    # print (to_h(unite_string(y_points_str, font)))

    return x_points, y_points


def getSymbols(img, font):
    h_threshold, v_threshold, h_center, v_center = get_threshold_and_center(font)
    x_points_str = [''] * img.shape[0]
    y_points_str = [''] * img.shape[1]
    result = ""

    for i in xrange(img.shape[0]):
        black_length = 0
        black_start = 0
        for j in xrange(img.shape[1]):
            if is_black_or_grey(img[i, j]):
                black_length += 1
            else:
                if black_length >= h_threshold:
                    x_points_str[i] += get_type(black_start, j, h_threshold, h_center)
                black_length = 0
                black_start = j + 1
        if black_length >= h_threshold:
            x_points_str[i] += get_type(black_start, j, h_threshold, h_center)
    result += (unite_str(x_points_str))

    for j in xrange(img.shape[1]):
        black_length = 0
        black_start = 0
        for i in xrange(img.shape[0]):
            if is_black_or_grey(img[i, j]):
                black_length += 1
            else:
                if black_length >= v_threshold:
                    y_points_str[j] += get_type(black_start, i, v_threshold, v_center)
                black_length = 0
                black_start = i + 1
        if black_length >= v_threshold:
            y_points_str[j] += get_type(black_start, i, v_threshold, v_center)

    result += " " + (to_h(unite_str(y_points_str)))
    return result


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


def draw_max_lines(img, x_points, y_points, color_x=(255, 255, 0), color_y=(255, 0, 255)):
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
                report += "Number {} Certainty: {:.2f} Variance {:.2f} \n".format(i, float(certainty[i]) / 26,
                                                                                  variance[i])
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
        histogram_x = np.zeros(img.shape[0])
        histogram_y = np.zeros(img.shape[1])
        sum_x = np.zeros(img.shape[0])
        sum_y = np.zeros(img.shape[1])
        noise_img_return = ImageNoiserCV.Noise(img)
        for z in range(noise_pictures):
            noise_img = noise_img_return  # ImageNoiser.Noise(img)
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
        variance_x = (x_points - average_x) ** 2
        variance_y = (y_points - average_y) ** 2
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
                draw_line_y(img, i, (255, 255 - int(255 * y), 255))

        return img, report, noise_img_return


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
