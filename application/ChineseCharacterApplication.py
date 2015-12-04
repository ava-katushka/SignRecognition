# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui
import sys
from PIL import Image, ImageDraw, ImageFont
from picture_generation.ChineseCharacterGenerator import ChineseCharacterGenerator
from algorithm.AlgorithmWrapper import AlgorithmWrapper
from utils.utils import *


class ChineseCharacterApplication(QtGui.QMainWindow):
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
    redRGB = (255, 0, 77)

    def __init__(self):
        super(ChineseCharacterApplication, self).__init__()
        self.left_offset = 20
        self.height_offset = 50
        self.pic_size = 200
        self.width = self.left_offset * 3 + self.pic_size * 2
        self.height = self.height_offset * 3 + self.pic_size
        self.small_offset = 10
        self.button_height_offset = 30
        self.init_ui()

    def init_ui(self):
        self.create_picture()
        self.create_picture_right()
        self.create_open_file_button()
        self.set_chinese_sign_picture_random()
        self.set_button_to_random_picture()
        self.set_button_to_feature1()
        self.set_button_to_feature2()
        self.set_window_properties()

    def create_picture(self):
        self.pic = QtGui.QLabel(self)
        self.pic.move(self.left_offset, self.height_offset)
        self.pic.resize(self.pic_size, self.pic_size)

    def create_picture_right(self):
        self.pic_right = QtGui.QLabel(self)
        self.pic_right.move(self.left_offset + self.pic_size + self.left_offset, self.height_offset)
        self.pic_right.resize(self.pic_size, self.pic_size)

    def create_open_file_button(self):
        self.open_file_button = QtGui.QPushButton(u'Выбрать из файла', self)
        self.open_file_button.clicked.connect(self.show_open_file_dialog)
        self.open_file_button.resize(self.open_file_button.sizeHint())
        self.open_file_button.move(self.left_offset, self.small_offset)

    def set_button_to_random_picture(self):
        self.random_button = QtGui.QPushButton(u'Случайный иероглиф', self)
        self.random_button.clicked.connect(self.set_chinese_sign_picture_random)
        self.random_button.resize(self.random_button.sizeHint())
        self.random_button.move(self.left_offset, self.height_offset + self.pic_size + self.small_offset)

    def set_button_to_feature1(self):
        self.feature1_button = QtGui.QPushButton(u'Концы линий', self)
        self.feature1_button.clicked.connect(self.set_picture_with_feature1)
        self.feature1_button.resize(self.feature1_button.sizeHint())
        self.feature1_button.move(self.left_offset,
                                self.height_offset + self.pic_size + self.small_offset + self.button_height_offset)

    def set_button_to_feature2(self):
        self.feature2_button = QtGui.QPushButton(u'Пересечения линий', self)
        self.feature2_button.clicked.connect(self.set_picture_with_feature2)
        self.feature2_button.resize(self.feature2_button.sizeHint())
        self.feature2_button.move(self.left_offset + self.feature1_button.sizeHint().width()  + self.small_offset,
                                self.height_offset + self.pic_size + self.small_offset + self.button_height_offset)

    def set_chinize_sign_picture(self):
        self.pic = QtGui.QLabel(self)
        self.pic.move(self.left_offset, self.height_offset)
        self.pic.resize(self.pic_size, self.pic_size)
        self.pic.setPixmap(
            QtGui.QPixmap(unicode(ChineseCharacterApplication._SCRIPT_ROOT) + u"/picture_examples/клякса1.jpg"))

    def set_chinese_sign_picture_random(self):
        picture = ChineseCharacterGenerator.random()
        while picture.isBlank():
            picture = ChineseCharacterGenerator.random()
        self.sign_picture = picture
        self.algorithm_picture = AlgorithmWrapper(picture)
        self.pic.setPixmap(picture.toQPixmap())
        self.set_right_picture()

    def set_right_picture(self):
        sk_image = self.algorithm_picture.skeleton_image()
        sk_image = PILtoQPixmap(sk_image)
        self.pic_right.setPixmap(sk_image)

    def set_picture_with_feature1(self):
        for point in self.algorithm_picture.line_features.ends_of_line:
            self.sign_picture.draw_ellipse_on(point, color=10)
        self.pic.setPixmap(self.sign_picture.toQPixmap())

    def set_picture_with_feature2(self):
        for point in self.algorithm_picture.line_features.cross_of_line:
            self.sign_picture.draw_ellipse_on(point, color=225)
        self.pic.setPixmap(self.sign_picture.toQPixmap())


    def set_window_properties(self):
        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle(u'Выделение признаков на китайских иероглифах')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_open_file_dialog(self):
        fileName = QtGui.QFileDialog.getOpenFileName(parent=self, caption=u"Выбрать иероглиф из файла",
                                                     directory=ChineseCharacterApplication._SCRIPT_ROOT,
                                                     filter="Images (*.png *.bmp *.jpg)");
        if (fileName):
            self.pic.setPixmap(QtGui.QPixmap(unicode(fileName)))
            QtGui.QPixmap()
