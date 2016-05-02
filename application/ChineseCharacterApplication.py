# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui

from algorithm.HistogrammPiksDetector import HistogrammPiksDetector
from picture_generation.ChineseCharacterGenerator import ChineseCharacterGenerator
from utils.utils import *
from algorithm.ImageNoiser import ImageNoiser
from metrics.Metrics import Metrics


class Panel:
    def __init__(self, app, refresh_func, offset=0,):
        self.offset = offset
        self.app = app
        self.noise_num = 0  # no noise
        self.refresh_func = refresh_func

    def init_ui(self):
        self.cur_x, self.cur_y = self.offset_from_side(), self.app.small_offset
        self.init_upper_panel()
        self.init_pictures()
        self.init_down_panel()

        self.set_chinese_sign_picture_random()

    def offset_from_side(self):
        if self.offset > 0:
            print self.offset
        return self.app.left_offset + self.offset

    def init_upper_panel(self):
        self.init_first_line()
        self.init_second_line()

    def to_new_line(self, last_obj):
        self.cur_x, self.cur_y = self.offset_from_side(), self.app.update_y(self.cur_y, last_obj)

    def update_x(self, prev_obj):
        self.cur_x = self.app.update_x(self.cur_x, prev_obj)

    def update_x_fix(self, distance):
        self.cur_x = self.app.update_fix(self.cur_x, self.app.pic_size)

    def init_first_line(self):
        self.left_chinese_sign_button = self.create_button(u'<', self.set_chinese_sign_picture_left)
        self.update_x(self.left_chinese_sign_button)
        self.font_text = self.create_font(u"Шрифт: Имя шрифта.ttf")
        self.update_x(self.font_text)
        self.right_chinese_sign_button = self.create_button(u'>', self.set_chinese_sign_picture_right)
        self.to_new_line(self.left_chinese_sign_button)

    def init_second_line(self):
        self.left_noise_button = self.create_button(u'<', self.set_left_noise)
        self.update_x(self.left_noise_button)
        self.noise_text = self.create_font(u"Шум: 0")
        self.update_x(self.noise_text)
        self.right_noise_button = self.create_button(u'>', self.set_right_noise)
        self.update_x(self.right_noise_button)
        self.without_noise = self.create_button(u"Без шума", self.setting_no_noise_picture)
        self.update_x(self.without_noise)
        self.comfort_positions = (self.cur_x, self.cur_y)
        self.to_new_line(self.without_noise)

    def init_pictures(self):
        self.pic = self.create_picture(self.app.pic_size, self.app.pic_size)
        self.update_x_fix(self.app.pic_size)
        self.pic_right = self.create_picture(self.app.pic_size, self.app.pic_size)
        self.cur_x, self.cur_y = self.offset_from_side(), self.app.update_fix(self.cur_y, self.app.pic_size)
        self.pic_bottom = self.create_picture(self.app.pic_size, self.app.pic_size)
        self.cur_x, self.cur_y = self.offset_from_side(), self.app.update_fix(self.cur_y, self.app.pic_size)

    def init_down_panel(self):
        self.random_button = self.create_button(u'Случайный иероглиф', self.set_chinese_sign_picture_random)
        self.update_x(self.random_button)
        self.char_description = self.create_font(u"Иероглиф: картинка")
        self.to_new_line(self.random_button)

    def create_button(self, text, func):
        return self.create_button_at(text, func, self.cur_x, self.cur_y)

    def create_button_at(self, text, func, position_x, position_y):
        button = QtGui.QPushButton(text, self.app)
        button.clicked.connect(func)
        button.resize(button.sizeHint())
        button.move(position_x, position_y)
        return button

    def create_font(self, text):
        return self.create_font_at(text, self.cur_x, self.cur_y + self.app.text_offset)

    def create_font_at(self, text, position_x, position_y):
        font_text = QtGui.QLabel(text, self.app)
        font_text.resize(font_text.sizeHint())
        font_text.move(position_x, position_y)
        return font_text

    def set_object_fixed_size(self, obj, width, height):
        obj.setFixedHeight(height)
        obj.setFixedWidth(width)

    def create_picture(self, width, height):
        return self.create_picture_at(self.cur_x, self.cur_y, width, height)

    def create_picture_at(self, position_x, position_y, width, height):
        pic = QtGui.QLabel(self.app)
        pic.move(position_x, position_y)
        pic.resize(width, height)
        return pic

    def set_chinese_sign_picture_random(self):
        picture = ChineseCharacterGenerator.random(self.app.picture_actual_size)
        while picture.isBlank():
            picture = ChineseCharacterGenerator.random(self.app.picture_actual_size)
        self.sign_picture = picture
        self.refresh_setting_to_new_picture()

    def set_picture(self, picture, noise_num=0):
        self.sign_picture = picture
        self.refresh_setting_to_new_picture()
        self.noise_num = noise_num
        self.refresh_setting_to_noise_picture()

    def set_chinese_sign_picture_left(self):
        self.sign_picture = ChineseCharacterGenerator.prevChar(self.sign_picture)
        while self.sign_picture.isBlank():
            self.sign_picture = ChineseCharacterGenerator.prevChar(self.sign_picture)
        self.refresh_setting_to_new_picture()

    def set_chinese_sign_picture_right(self):
        self.sign_picture = ChineseCharacterGenerator.nextChar(self.sign_picture)
        while self.sign_picture.isBlank():
            self.sign_picture = ChineseCharacterGenerator.nextChar(self.sign_picture)
        self.refresh_setting_to_new_picture()

    def refresh_setting_to_new_picture(self):
        # self.algorithm_picture = AlgorithmWrapper(copy.deepcopy(self.sign_picture))
        cv_image = PILtoCV(self.sign_picture.pilImageColor)
        pil_image = CVtoPIL(cv_image)
        self.pic.setPixmap(PILtoQPixmap(pil_image).scaled(self.app.pic_size, self.app.pic_size))
        self.set_right_picture()
        self.font_text.setText(u"Шрифт: " + self.sign_picture.fontName)
        self.char_description.setText(u"Иероглиф: " + self.sign_picture.sign)
        self.refresh_setting_to_noise_picture()
        self.refresh_func()
        # self.text.setText(report)

    def refresh_setting_to_noise_picture(self):
        image = ImageNoiser.NoiseNum(self.sign_picture.pilImageColor, self.noise_num)
        self.noise_text.setText(u"Шум: " + str(self.noise_num))
        self.pic.setPixmap(PILtoQPixmap(image).scaled(self.app.pic_size, self.app.pic_size))
        self.set_right_picture(image)
        self.refresh_func()

    def setting_no_noise_picture(self):
        self.noise_num = 0
        self.set_chinese_sign_picture_right()
        self.set_chinese_sign_picture_left()

    def set_right_picture(self, image=None):
        # sk_image = self.algorithm_picture.skeleton_image()
        # sk_image = PILtoQPixmap(sk_image)
        if not image:
            image = self.sign_picture.pilImageColor
        cv_image = PILtoCV(image)
        self.horizontal_lines, self.vertical_lines, horiz_histogram, vertical_histogram = HistogrammPiksDetector.getLinesOnPicture(
            cv_image)
        pil_image = CVtoPIL(horiz_histogram)
        bottom_image = CVtoPIL(vertical_histogram)
        self.pic_right.setPixmap(PILtoQPixmap(pil_image).scaled(self.app.pic_size, self.app.pic_size))
        self.pic_bottom.setPixmap(PILtoQPixmap(bottom_image).scaled(self.app.pic_size, self.app.pic_size))

    def set_right_noise(self):
        self.noise_num += 1
        if self.noise_num > ImageNoiser.pic_number:
            self.noise_num = 0
            self.setting_no_noise_picture()
        else:
            self.refresh_setting_to_noise_picture()

    def set_left_noise(self):
        self.noise_num -= 1
        self.noise_num = self.noise_num % ImageNoiser.pic_number
        if self.noise_num == 0:
            self.setting_no_noise_picture()
        else:
            self.refresh_setting_to_noise_picture()


class PanelInteracting:
    def __init__(self, app, left, right):
        self.app = app
        self.left = left
        self.right = right
        self.set_picture_like_other()
        self.set_metrics_panel()

    def set_metrics_panel(self):
        self.metrics_1 = self.left.create_font(u'Расстояние Левенштейна: 02 bla bla bla bla bla bla bla bla bla bla bla ')
        self.left.update_x(self.metrics_1)
        self.metrics_2 = self.right.create_font(u'Расстояние Левенштейна-Дамерау: 02 bla bla bla bla bla bla bla bla ')
        self.right.update_x(self.metrics_2)
        self.metrics()


    def set_picture_like_other(self):
        self.set_like_another(self.left, u'Как справа', self.button_set_like_right)
        self.set_like_another(self.right, u'Как слева', self.button_set_like_left)

    def set_like_another(self, panel, text, func):
        x, y = panel.comfort_positions[0], panel.comfort_positions[1]
        panel.like_other = panel.create_button_at(text, func, x, y)


    def button_set_like_right(self):
        self.button_set_like(self.left, self.right)

    def button_set_like_left(self):
        self.button_set_like(self.right, self.left)

    def button_set_like(self, cur_panel, wish_panel):
        cur_panel.set_picture(wish_panel.sign_picture, wish_panel.noise_num)


    def metrics(self):
        horiz_distance = Metrics.levenstein_distance(self.left.horizontal_lines, self.right.horizontal_lines)
        vertical_distance = Metrics.levenstein_distance(self.left.vertical_lines, self.right.vertical_lines)
        total_distance = horiz_distance + vertical_distance
        self.metrics_1.setText(u'Расстояние Левенштейна: ' + unicode(total_distance) + u" Гориз: "
                               + unicode(horiz_distance) + u" Верт: " + unicode(vertical_distance))
        horiz_distance = Metrics.dameray_levenstein_distance(self.left.horizontal_lines, self.right.horizontal_lines)
        vertical_distance = Metrics.dameray_levenstein_distance(self.left.vertical_lines, self.right.vertical_lines)
        total_distance = horiz_distance + vertical_distance
        self.metrics_2.setText(u'Расстояние Левенштейна-Дамерау: ' + unicode(total_distance) + u" Гориз: "
                               + unicode(horiz_distance) + u" Верт: " + unicode(vertical_distance))



class ChineseCharacterApplication(QtGui.QMainWindow):
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
    redRGB = (255, 0, 77)

    def __init__(self):
        super(ChineseCharacterApplication, self).__init__()
        self.left_offset = 20
        self.picture_actual_size = 30
        self.pic_size = 200
        self.width = 450 * 2
        self.height = 600
        self.small_offset = 10
        self.text_offset = self.small_offset * 0.7

        self.left_panel = Panel(app=self, offset=0, refresh_func=self.refresh_func)
        self.left_panel.init_ui()

        self.right_panel = Panel(app=self, offset=self.width / 2, refresh_func=self.refresh_func)
        self.right_panel.init_ui()

        self.panel_interacting = PanelInteracting(self, self.left_panel, self.right_panel)
        self.set_window_properties()

    def refresh_func(self):
        if hasattr(self, 'panel_interacting'):
            self.panel_interacting.metrics()
        pass

    def update_x(self, x, prev_obj):
        x += prev_obj.sizeHint().width() + self.small_offset
        return x

    def update_fix(self, value, fix):
        value += fix + self.small_offset
        return value

    def update_y(self, y, prev_obj):
        y += prev_obj.sizeHint().height() + self.small_offset
        return y

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
