# -*- coding: utf-8 -*-
import random

import sys
import os
curFilePath = os.path.dirname(os.path.realpath(__file__))
curDirPath = os.path.dirname( curFilePath )
sys.path.append(curDirPath)
print sys.path

from picture_generation.SignPicture import SignPictureSimple

__author__ = 'ava-katushka'
import os

from PyQt4 import QtGui

from utils.utils import *
from utils.Timing import timing
import pickle


class SignInfo:
    def __init__(self, id, num, font):
        self.id = int(id)
        self.num = int(num)
        self.font = font


class PictureOnDistance:
    def __init__(self, id, vert_dist, horiz_dist):
        self.id = id
        self.vert_dist = vert_dist
        self.horiz_dist = horiz_dist

    def metrics(self):
        return self.vert_dist + self.horiz_dist


class Database_Work:
    @timing
    def load_picture_database(self):
        self.pictures = []
        with open(self.database_file, "r") as file:
            # Id,SignOrd,Font,HorizontalDescription,VerticalDescription
            # 0,32768,Hiragino Sans GB W3.otf,[0; 0; 0; 1; 1; 0; 1;
            file.readline()
            for line in file:
                array = line.split(",")
                id = array[0]
                num = array[1]
                font = array[2]
                self.pictures.append(SignInfo(id, num, font))

    @timing
    def load_metrics_database(self):
        with open(self.metrics_file, "r") as file:
            file.readline()
            id = 0
            for line in file:
                array = line.split(",")
                pic_on_dist = []
                for i in xrange(len(array) - 1):
                    values = eval(array[i].replace(";", ","))
                    pic_dist = PictureOnDistance(int(values[0]), int(values[1]), int(values[2]))
                    pic_on_dist.append(pic_dist)
                self.picture_on_distance[id] = pic_on_dist
                id += 1



    def __init__(self):
        tmp = [1,2,3]
        result = str(tmp) + u'<- result'
        print result

        self._SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
        self.database_file = os.path.join(self._SCRIPT_ROOT, "picture_database.txt")
        self.metrics_file = os.path.join(self._SCRIPT_ROOT, "metrics_database2.txt")
        self.metrics_dump_file = os.path.join(self._SCRIPT_ROOT, "metrics_database_dump.txt")
        self.picture_on_distance = {}
        self.load_picture_database()
        self.load_metrics_database()


class Panel:
    def __init__(self, app, refresh_func, offset=0, ):
        self.offset = offset
        self.app = app
        self.noise_num = 0  # no noise
        self.refresh_func = refresh_func
        self.right_start = self.app.left_offset * 2 + self.app.pic_size
        self.db_work = Database_Work()

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
        self.cur_x = self.app.update_fix(self.cur_x, distance)

    def init_first_line(self):
        self.font_text = self.create_font(u"Шрифт: Имя шрифта.ttf")
        self.cur_x = self.right_start + self.app.left_offset
        self.right_font_text = self.create_font(u"Шрифт: Имя шрифта.ttf")
        self.to_new_line(self.right_font_text)

    def init_second_line(self):
        self.num_text = self.create_font(u"Иероглиф: вот Номер: 12345")
        self.cur_x = self.right_start + self.app.left_offset
        self.right_num_text = self.create_font(u"Иероглиф: вот Номер: 12345")
        self.to_new_line(self.right_num_text)

    def init_pictures(self):
        self.pic = self.create_picture(self.app.pic_size, self.app.pic_size)
        self.update_x_fix(self.app.pic_size + self.app.left_offset)
        self.pic_right = self.create_picture(self.app.pic_size, self.app.pic_size)
        self.cur_x, self.cur_y = self.offset_from_side(), self.app.update_fix(self.cur_y, self.app.pic_size)

    def init_down_panel(self):
        self.random_button = self.create_button(u'Случайный иероглиф', self.set_chinese_sign_picture_random)
        self.update_x(self.random_button)
        self.init_right_down()
        self.cur_x = self.right_start
        self.distance_details = self.create_font(u'Горизонтально: 10, Вертикально: 15')
        self.to_new_line(self.random_button)

    def init_right_down(self):
        self.cur_x = self.right_start
        self.left_distance_button = self.create_button(u'<', self.set_chinese_sign_picture_left)
        self.update_x(self.left_distance_button)
        self.distance_text = self.create_font(u"Расстояние: 25")
        self.update_x(self.distance_text)
        self.right_distance_button = self.create_button(u'>', self.set_chinese_sign_picture_right)
        self.to_new_line(self.left_distance_button)

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

    def create_statics(self, id, myself_num):
        pic_set = self.db_work.picture_on_distance[id]

        all_hieroglyph_set = set([])
        myself_positions = []
        myself_text = u''

        group_start = 0

        for i in range( 0, len(pic_set) ):
            cur_picture = pic_set[i]
            picture_info = self.db_work.pictures[cur_picture.id]

            if picture_info.num == myself_num:
                myself_positions.append( i )
            if cur_picture.metrics() != pic_set[group_start].metrics():
                myself_text += str( pic_set[group_start].metrics() ) + u':' + str( group_start ) + u'-' + str(i - 1) + u'#' + str( len( all_hieroglyph_set ) ) + u' from ' + str( i ) + u'\r\n'
                group_start = i

            all_hieroglyph_set.add( picture_info.num )

        myself_text += str( pic_set[group_start].metrics() ) + u':' + str( group_start ) + u'-' + str(len( pic_set ) - 1) + u'#' + str( len( all_hieroglyph_set ) ) + u' from ' + str( len( pic_set ) ) + u'\r\n'
        myself_text = u'My self positions: ' + str( myself_positions ) + u'\r\n' + myself_text

        return myself_text


    def set_chinese_sign_picture_random(self):
        num = random.randint(0, len(self.db_work.pictures) )
        picture = self.db_work.pictures[num]
        self.id = picture.id
        self.sign_picture = SignPictureSimple(unichr(picture.num), picture.font)
        self.refresh_setting_to_new_picture()


        msg = QtGui.QMessageBox()
        msg.setText( u'stat' )
        msg.setDetailedText( self.create_statics( self.id, picture.num ) )
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msg.exec_()

    def set_picture(self, picture, noise_num=0):
        self.sign_picture = picture
        self.refresh_setting_to_new_picture()

    def set_chinese_sign_picture_left(self):
        self.distance_ind -= 1

        self.set_right_picture()

    def set_chinese_sign_picture_right(self):
        self.distance_ind += 1
        self.set_right_picture()

    def refresh_setting_to_new_picture(self):
        self.pic.setPixmap(PILtoQPixmap(self.sign_picture.pilImageColor).scaled(self.app.pic_size, self.app.pic_size))
        self.distance_ind = 0
        self.set_right_picture()
        sign_info = self.db_work.pictures[self.id]
        self.font_text.setText(u"Шрифт: " + sign_info.font)
        self.num_text.setText( u"Иероглиф: " + unichr(sign_info.num) + u' Номер:' + str(sign_info.num))

        self.refresh_func()

    def get_picture_on_distance(self, id, distance):
        pic_set = self.db_work.picture_on_distance[id]
        return pic_set[self.distance_ind % len(pic_set)]

    def set_right_picture(self, image=None):
        distance_picture = self.get_picture_on_distance(self.id, self.distance_ind)
        picture_info = self.db_work.pictures[distance_picture.id]
        self.right_picture = SignPictureSimple(unichr(picture_info.num), picture_info.font)
        self.pic_right.setPixmap(
            PILtoQPixmap(self.right_picture.pilImageColor).scaled(self.app.pic_size, self.app.pic_size))
        self.distance_text.setText(u'Расстояние: ' + unicode(distance_picture.metrics()))
        self.distance_details.setText(u'Вертикально:' + unicode(distance_picture.vert_dist) + u' Горизонтально:' +
                                      unicode(distance_picture.horiz_dist))
        sign_info = picture_info
        self.right_font_text.setText(u"Шрифт: " + sign_info.font)
        self.right_num_text.setText( u"Иероглиф: " + unichr(sign_info.num) + u' Номер:' + str(sign_info.num))


class MetricsAnalysingApplication(QtGui.QMainWindow):
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
    redRGB = (255, 0, 77)

    def __init__(self):
        super(MetricsAnalysingApplication, self).__init__()
        self.left_offset = 20
        self.picture_actual_size = 30
        self.pic_size = 200
        self.width = 500
        self.height = 350
        self.small_offset = 10
        self.text_offset = self.small_offset * 0.7

        self.panel = Panel(app=self, offset=0, refresh_func=self.refresh_func)
        self.panel.init_ui()

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
        self.setWindowTitle(u'Оценка качества метрики')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MetricsAnalysingApplication()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
