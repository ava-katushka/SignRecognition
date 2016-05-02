# -*- coding: utf-8 -*-
__author__ = 'ava-katushka'

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


class CompareCharacterApplication(QtGui.QMainWindow):
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))

    def __init__(self):
        super(CompareCharacterApplication, self).__init__()
        self.left_offset = 20
        self.height_offset = 50
        self.picture_actual_size = 30
        self.width = 800
        self.height = 500
        self.small_offset = 10
        self.button_height_offset = 30
        self.picture_window_start = 100
        self.button_offset = self.small_offset * 0.7
        self.compare_window_start = 400
        self.middle = self.width / 2
        self.picture_size = (self.middle - self.left_offset * 2.5) / 2
        self.init_ui()

    def init_ui(self):
        self.create_high_panel()
        self.set_window_properties()


    def set_window_properties(self):
        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle(u'Compare Chinese Characters')
        self.show()

    def create_high_panel(self):
        self.create_headline()
        self.create_cluster_iteration()
        self.create_pictures()

    def create_headline(self):
        self.set_text(u"Total clusters: 12     Total Characters: 536", self.left_offset, self.small_offset)

    def create_cluster_iteration(self):
        self.create_cluster_description(self.empty_func, self.empty_func)
        self.create_cluster_description(self.empty_func, self.empty_func, left_offset=self.middle)

    def create_cluster_description(self, left_button, right_button, left_offset=None):
        if not left_offset:
            left_offset = self.left_offset
        height_offset_button = self.small_offset * 3
        height_offset_text = height_offset_button + self.button_offset
        left_offset += self.set_text(u"Cluster: ", left_offset, height_offset_text).width()  + self.small_offset
        left_offset += self.set_button(u"<", left_button, left_offset, height_offset_button).width() + self.small_offset
        left_offset += self.set_text(u"5", left_offset, height_offset_text).width() + self.small_offset
        left_offset += self.set_button(u">", right_button, left_offset, height_offset_button).width() + self.small_offset
        left_offset += self.set_text(u"Characters: 78", left_offset, height_offset_text).width() + self.small_offset

    def create_pictures(self):
        height_offset = self.picture_window_start
        left_offset = self.left_offset
        for i in range(4):
            left_offset += self.create_picture(self.picture_size, left_offset, height_offset).width()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_text(self, text, position_x, position_y):
        qLabel = QtGui.QLabel(text, self)
        qLabel.resize(qLabel.sizeHint())
        qLabel.move(position_x, position_y)
        return qLabel

    def set_button(self, text, func, position_x, position_y):
        button = QtGui.QPushButton(text, self)
        button.clicked.connect(func)
        button.resize(button.sizeHint())
        button.move(position_x, position_y)
        return button

    def create_picture(self, size, position_x, position_y):
        picture = QtGui.QLabel(self)
        picture.move(position_x, position_y)
        picture.resize(size, size)
        picture.setPixmap(
            QtGui.QPixmap(unicode(CompareCharacterApplication._SCRIPT_ROOT) + u"extra/picture_examples/клякса1.jpg"))
        print "Hello"
        return picture

    def empty_func(self):
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = CompareCharacterApplication()
    sys.exit(app.exec_())