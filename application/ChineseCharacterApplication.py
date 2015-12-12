# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui
import PyQt4
import sys
from PIL import Image, ImageDraw, ImageFont
from picture_generation.ChineseCharacterGenerator import ChineseCharacterGenerator
from algorithm.AlgorithmWrapper import AlgorithmWrapper
from utils.utils import *
import copy


class ChineseCharacterApplication(QtGui.QMainWindow):
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
    redRGB = (255, 0, 77)

    def __init__(self):
        super(ChineseCharacterApplication, self).__init__()
        self.left_offset = 20
        self.height_offset = 50
        self.picture_actual_size = 30
        self.pic_size = 200
        self.width = self.left_offset * 4 + self.pic_size * 2
        self.height = self.height_offset * 3 + self.pic_size
        self.small_offset = 10
        self.button_height_offset = 30
        self.init_ui()

    def init_ui(self):
        self.create_picture()
        self.create_picture_right()
        self.create_open_file_button()
        self.create_left_button()
        self.create_font_name_text()
        self.create_right_button()
        self.set_button_to_random_picture()
        self.create_char_description_text()

        self.set_chinese_sign_picture_random()
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

    def create_left_button(self):
        self.left_chinese_sign_button = QtGui.QPushButton(u'<', self)
        self.left_chinese_sign_button.clicked.connect(self.set_chinese_sign_picture_left)
        self.left_chinese_sign_button.resize(self.left_chinese_sign_button.sizeHint())
        self.left_chinese_sign_button.move(self.left_offset  + self.open_file_button.sizeHint().width() +
                                           self.small_offset, self.small_offset)

    def create_font_name_text(self):
        self.font_text = QtGui.QLabel(u"Шрифт: Имя шрифта.ttf", self)
        self.font_text.resize(self.font_text.sizeHint())
        self.font_text.move(self.left_offset + self.open_file_button.sizeHint().width() + self.left_chinese_sign_button.sizeHint().width()
                            + self.small_offset * 2, self.small_offset * 1.7)

    def create_right_button(self):
        self.right_chinese_sign_button = QtGui.QPushButton(u'>', self)
        self.right_chinese_sign_button.clicked.connect(self.set_chinese_sign_picture_right)
        self.right_chinese_sign_button.resize(self.right_chinese_sign_button.sizeHint())
        self.right_chinese_sign_button.move(self.left_offset + self.open_file_button.sizeHint().width() +
                                           self.left_chinese_sign_button.sizeHint().width()
                                           + self.font_text.sizeHint().width() + self.small_offset * 3, self.small_offset)

    def set_button_to_random_picture(self):
        self.random_button = QtGui.QPushButton(u'Случайный иероглиф', self)
        self.random_button.clicked.connect(self.set_chinese_sign_picture_random)
        self.random_button.resize(self.random_button.sizeHint())
        self.random_button.move(self.left_offset, self.height_offset + self.pic_size + self.small_offset)

    def create_char_description_text(self):
        self.char_description = QtGui.QLabel(u"Иероглиф: картинка", self)
        self.char_description.resize(self.char_description.sizeHint())
        self.char_description.move(self.left_offset + self.random_button.sizeHint().width() +
                            + self.small_offset, self.height_offset + self.pic_size + self.small_offset * 1.7)

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
        picture = ChineseCharacterGenerator.random(self.picture_actual_size)
        while picture.isBlank():
            picture = ChineseCharacterGenerator.random(self.picture_actual_size)
        self.sign_picture = picture
        self.refresh_setting_to_new_picture()

    def set_chinese_sign_picture_left(self):
        self.sign_picture = ChineseCharacterGenerator.prevChar(self.sign_picture)
        self.refresh_setting_to_new_picture()

    def set_chinese_sign_picture_right(self):
        self.sign_picture = ChineseCharacterGenerator.nextChar(self.sign_picture)
        self.refresh_setting_to_new_picture()

    def refresh_setting_to_new_picture(self):
        self.algorithm_picture = AlgorithmWrapper(copy.deepcopy(self.sign_picture))
        self.pic.setPixmap(PILtoQPixmap(self.sign_picture.pilImageColor).scaled(self.pic_size, self.pic_size))
        self.set_right_picture()
        self.font_text.setText(u"Шрифт: " + self.sign_picture.fontName)
        self.char_description.setText(u"Иероглиф: " + self.sign_picture.sign)

    def set_right_picture(self):
        sk_image = self.algorithm_picture.skeleton_image()
        sk_image = PILtoQPixmap(sk_image)
        self.pic_right.setPixmap(sk_image.scaled(self.pic_size, self.pic_size))

    def set_picture_with_feature1(self):
        for point in self.algorithm_picture.line_features.ends_of_line:
            self.sign_picture.draw_ellipse_on(point, color=10)
        pixmap = PILtoQPixmap(self.sign_picture.pilImageColor)
        self.pic.setPixmap(pixmap.scaled(self.pic_size, self.pic_size))

    def set_picture_with_feature2(self):
        for point in self.algorithm_picture.line_features.cross_of_line:
            self.sign_picture.draw_ellipse_on(point, color=225)
        pixmap = PILtoQPixmap(self.sign_picture.pilImageColor)
        self.pic.setPixmap(pixmap.scaled(self.pic_size, self.pic_size))


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
