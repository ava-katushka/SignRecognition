# -*- coding: utf-8 -*-
import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

from utils.Timing import timing
from metrics.PictureMetrics import PictureMetrics
from picture_generation.FontFamily import FontFamily

__author__ = 'ava-katushka'


def random_but_not_this(i, n):
    rand = random.randint(0, n - 1)
    while rand == i:
        rand = random.randint(0, n - 1)
    return rand


class Testing:
    # 1000 pairs of chars inside 4 font families: Kaity, FangSong, Wtc, Simhei
    # count alikeness of same characters due to Levenstein-Dameray
    #     Эксперимент:
    # Шрифты разбиты на 4 класса по семейству шрифтов:
    # 1) "KaiTi_GB2312.ttf", "kaiti.ttf"
    # 2) "FangSong_GB2312.ttf", "fangsong.ttf"
    # 3) "wts11.ttf", "WCL-07.ttf"
    # 4) "simhei.ttf","Hiragino Sans GB W3.otf"
    #
    # Для каждого класса взято 1000 иероглифов и посчитана
    # метрика Левенштейна-Дамерау между парами
    # одинаковых иероглифов.
    # Метрика Левенштейна-Дамерау считается отдельно для
    # горизонтальных и вертикальных линий, результаты затем
    # складываются.
    #
    # На диаграмме видно, что центр распределения
    #  расстояния находится в 7-8.
    @classmethod
    def experiment1(cls):
        metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_sum(x, y)
        fontFamilies = FontFamily.get_all_families()
        alikes = []
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(1000)
            for pair_of_signes in signes:
                distance = metrics(pair_of_signes[0], pair_of_signes[1])
                alikes.append(distance)
        plt.hist(alikes)
        plt.show()

    # Эксперимент:
    # Шрифты разбиты на 4 класса по семейству шрифтов:
    # 1) "KaiTi_GB2312.ttf", "kaiti.ttf"
    # 2) "FangSong_GB2312.ttf", "fangsong.ttf"
    # 3) "wts11.ttf", "WCL-07.ttf"
    # 4) "simhei.ttf","Hiragino Sans GB W3.otf"
    #
    # Для каждого класса взято 1000 иероглифов и посчитана горизонтальная
    # метрика Левенштейна-Дамерау между парами
    # одинаковых иероглифов.
    # Метрика Левенштейна-Дамерау считается только для горизонтальных линий.
    #
    # На диаграмме видно, что центр распределения
    #  расстояния находится в 4-5.

    @classmethod
    def experiment2(cls):
        metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_h(x, y)
        fontFamilies = FontFamily.get_all_families()
        alikes = []
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(1000)
            for pair_of_signes in signes:
                distance = metrics(pair_of_signes[0], pair_of_signes[1])
                alikes.append(distance)
        plt.hist(alikes)
        plt.show()

    # Эксперимент:
    # Шрифты разбиты на 4 класса по семейству шрифтов:
    # 1) "KaiTi_GB2312.ttf", "kaiti.ttf"
    # 2) "FangSong_GB2312.ttf", "fangsong.ttf"
    # 3) "wts11.ttf", "WCL-07.ttf"
    # 4) "simhei.ttf","Hiragino Sans GB W3.otf"
    #
    # Для каждого класса взято 1000 иероглифов и посчитана вертикальная
    # метрика Левенштейна-Дамерау между парами
    # одинаковых иероглифов.
    # Метрика Левенштейна-Дамерау считается только для вертикальных линий.
    #
    # На диаграмме видно, что центр распределения
    #  расстояния находится в 3-4.

    @classmethod
    def experiment3(cls):
        metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_v(x, y)
        fontFamilies = FontFamily.get_all_families()
        alikes = []
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(1000)
            for pair_of_signes in signes:
                distance = metrics(pair_of_signes[0], pair_of_signes[1])
                alikes.append(distance)
        plt.hist(alikes)
        plt.show()

    # Эксперимент:
    # Шрифты разбиты на 4 класса по семейству шрифтов:
    # 1) "KaiTi_GB2312.ttf", "kaiti.ttf"
    # 2) "FangSong_GB2312.ttf", "fangsong.ttf"
    # 3) "wts11.ttf", "WCL-07.ttf"
    # 4) "simhei.ttf","Hiragino Sans GB W3.otf"
    #
    # Для каждого класса взято 1000 иероглифов и посчитана горизонталтная
    # метрика Левенштейна-Дамерау между парами разных иероглифов одинаковых шрифтов.
    # Метрика Левенштейна-Дамерау считается только для горизонтальных линий.
    #
    # Другой иероглиф - случайный иероглиф из множества.
    @classmethod
    def experiment4(cls):
        metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_h(x, y)
        fontFamilies = FontFamily.get_all_families()
        differences = []
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(1000)
            for i, sign_array in enumerate(signes):
                for j, sign in enumerate(sign_array):
                    ind = random_but_not_this(j, len(signes))
                    distance = metrics(sign, signes[ind][j])
                    differences.append(distance)

        plt.hist(differences)
        plt.show()

    # Эксперимент:
    # Шрифты разбиты на 4 класса по семейству шрифтов:
    # 1) "KaiTi_GB2312.ttf", "kaiti.ttf"
    # 2) "FangSong_GB2312.ttf", "fangsong.ttf"
    # 3) "wts11.ttf", "WCL-07.ttf"
    # 4) "simhei.ttf","Hiragino Sans GB W3.otf"
    #
    # Для каждого класса взято 1000 иероглифов и посчитана горизонталтная
    # метрика Левенштейна-Дамерау между парами разных иероглифов одинаковых шрифтов.
    # Метрика Левенштейна-Дамерау считается только для горизонтальных линий.
    #
    # Другой иероглиф - следующий иероглиф из множества. Т.е i + 1 для i. Шрифт - тот же.
    # Диаграмма более смещена к началу, чем со случайными иероглифом.
    #  Наверно, следующие друг за другом иероглифы чаще похожи.
    @classmethod
    def experiment5(cls):
        metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_h(x, y)
        fontFamilies = FontFamily.get_all_families()
        differences = []
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(1000)
            for i, sign_array in enumerate(signes):
                for j, sign in enumerate(sign_array):
                    ind = (i + 1) % len(signes)
                    distance = metrics(sign, signes[ind][j])
                    differences.append(distance)

        plt.hist(differences)
        plt.show()

    #
    # Эксперимент:
    # Шрифты разбиты на 4 класса по семейству шрифтов:
    # 1) "KaiTi_GB2312.ttf", "kaiti.ttf"
    # 2) "FangSong_GB2312.ttf", "fangsong.ttf"
    # 3) "wts11.ttf", "WCL-07.ttf"
    # 4) "simhei.ttf","Hiragino Sans GB W3.otf"
    #
    # Для каждого класса взято 1000 иероглифов и посчитана вертикальная
    # метрика Левенштейна-Дамерау между парами разных иероглифов одинаковых шрифтов.
    # Метрика Левенштейна-Дамерау считается только для вертикальных  линий.
    #
    # Другой иероглиф - случайный иероглиф из множества.
    @classmethod
    def experiment6(cls):
        metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_v(x, y)
        fontFamilies = FontFamily.get_all_families()
        differences = []
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(1000)
            for i, sign_array in enumerate(signes):
                for j, sign in enumerate(sign_array):
                    ind = random_but_not_this(j, len(signes))
                    distance = metrics(sign, signes[ind][j])
                    differences.append(distance)

        plt.hist(differences)
        plt.show()

    # Эксперимент:
    # Шрифты разбиты на 4 класса по семейству шрифтов:
    # 1) "KaiTi_GB2312.ttf", "kaiti.ttf"
    # 2) "FangSong_GB2312.ttf", "fangsong.ttf"
    # 3) "wts11.ttf", "WCL-07.ttf"
    # 4) "simhei.ttf","Hiragino Sans GB W3.otf"
    #
    # Для каждого класса взято 1000 иероглифов и посчитана
    # метрика Левенштейна-Дамерау между парами
    # разных иероглифов одного шрифта.
    # Метрика Левенштейна-Дамерау считается отдельно для
    # горизонтальных и вертикальных линий, результаты затем
    # складываются.
    #
    # Другой иероглиф - случайный иероглиф из множества.
    @classmethod
    def experiment7(cls):
        metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_sum(x, y)
        fontFamilies = FontFamily.get_all_families()
        differences = []
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(1000)
            for i, sign_array in enumerate(signes):
                for j, sign in enumerate(sign_array):
                    ind = random_but_not_this(j, len(signes))
                    distance = metrics(sign, signes[ind][j])
                    differences.append(distance)

        plt.hist(differences)
        plt.show()

    # Эксперимент:
    # Поэксперементируем с медианной линией для отсечения признаков.
    # Используется, как и раньше, 4 класса шрифтов, но только по 200 иероглифов в каждом классе (для быстроты)
    # Раннее в экспериментах медианная линия = 10 по счету элемент с конца (массив сортирован по возрастанию)
    # Теперь пробуем медианную линию от 0 до 30 и считаем расстояние между  массивами одинаковых иероглифов.

    @classmethod
    @timing
    def experiment8(cls):
        alike_distances = []
        for median_num in range(0, 30):
            metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_sum(x, y, median_num=median_num)
            fontFamilies = FontFamily.get_all_families()
            alike_distance = 0
            for fontFamily in fontFamilies:
                print "--new font family---"
                signes = fontFamily.get_signes(20)
                for pair_of_signes in signes:
                    distance = metrics(pair_of_signes[0], pair_of_signes[1])
                    alike_distance += distance
            alike_distances.append(alike_distance)

        plt.plot(range(0, 30), alike_distances, 'ro')
        plt.show()

    @classmethod
    @timing
    def experiment8(cls):
        alike_distances = []
        for median_num in range(0, 30):
            metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_sum(x, y, median_num=median_num)
            fontFamilies = FontFamily.get_all_families()
            alike_distance = 0
            for fontFamily in fontFamilies:
                print "--new font family---"
                signes = fontFamily.get_signes(50)
                for pair_of_signes in signes:
                    distance = metrics(pair_of_signes[0], pair_of_signes[1])
                    alike_distance += distance
            alike_distances.append(alike_distance)

        plt.plot(range(0, 30), alike_distances, 'ro')
        plt.show()

    # Эксперимент:
    # Поэксперементируем с медианной линией для отсечения признаков.
    # Используется, как и раньше, 4 класса шрифтов, но только по 50 иероглифов в каждом классе (для быстроты)
    # Раннее в экспериментах медианная линия = 10 по счету элемент с конца (массив сортирован по возрастанию)
    # Теперь пробуем медианную линию от 0 до 30 и считаем расстояние между массивами разных иероглифов.

    @classmethod
    @timing
    def experiment9(cls):
        diff_distances = []
        for median_num in range(0, 30):
            metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_sum(x, y, median_num=median_num)
            fontFamilies = FontFamily.get_all_families()
            diff_distance = 0
            for fontFamily in fontFamilies:
                print "--new font family---"
                signes = fontFamily.get_signes(50)
                for pair_of_signes in signes:
                    for j, sign in enumerate(pair_of_signes):
                        ind = random_but_not_this(j, len(signes))
                        distance = metrics(sign, signes[ind][j])
                        diff_distance += distance

            diff_distances.append(diff_distance)

        plt.plot(range(0, 30), diff_distances, 'ro')
        plt.show()

    # Объединение экспериментов 8 и 9. Найдем самую большую разницу по медиане
    #  между расстоянием между одинаковыми классами, и разными.
    @classmethod
    @timing
    def experiment10(cls):
        alike_distances = []
        for median_num in range(0, 30):
            metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_sum(x, y, median_num=median_num)
            fontFamilies = FontFamily.get_all_families()
            alike_distance = 0
            for fontFamily in fontFamilies:
                print "--new font family---"
                signes = fontFamily.get_signes(30)
                for pair_of_signes in signes:
                    distance = metrics(pair_of_signes[0], pair_of_signes[1])
                    alike_distance += distance
            alike_distances.append(alike_distance)
        diff_distances = []
        for median_num in range(0, 30):
            metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_sum(x, y, median_num=median_num)
            fontFamilies = FontFamily.get_all_families()
            diff_distance = 0
            for fontFamily in fontFamilies:
                print "--new font family---"
                signes = fontFamily.get_signes(15)
                for pair_of_signes in signes:
                    for j, sign in enumerate(pair_of_signes):
                        ind = random_but_not_this(j, len(signes))
                        distance = metrics(sign, signes[ind][j])
                        diff_distance += distance

            diff_distances.append(diff_distance)
        substaction = []
        for alike, diff in zip(alike_distances, diff_distances):
            substaction.append(diff - alike)
        plt.plot(range(0, 30), substaction, 'ro')
        plt.show()

    # Минимизирует расстояние между одинаковыми иероглифами и разницу между разными иероглифами
    @classmethod
    @timing
    def optimize_weights(cls, weights, num_of_signes=100):
        print weights
        metrics = lambda x, y: PictureMetrics.dameray_levenstein_distance_sum(x, y, weights=weights)
        fontFamilies = FontFamily.get_all_families()
        alike_distance = 0
        alike_num = 0
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(num_of_signes)
            for pair_of_signes in signes:
                distance = metrics(pair_of_signes[0], pair_of_signes[1])
                alike_distance += distance
                alike_num += 1
        print "alike distance=", alike_distance
        #print "alike num=", alike_num
        diff_distance = 0
        diff_num = 0
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(num_of_signes / 2)
            for pair_of_signes in signes:
                for j, sign in enumerate(pair_of_signes):
                    ind = random_but_not_this(j, len(signes))
                    distance = metrics(sign, signes[ind][j])
                    diff_distance += max(25 - distance, 0)
                    diff_num += 1
        print "diff distance=", diff_distance
        #print "diff num=", diff_num
        result = alike_distance + diff_distance
        print "total=", result
        return result

    # Эксперимент: попытаемся найти хорошие веса для расстояния Левенштейна-Дамерау
    # Запустим минимизацию функцию суммы между парами одинаковых и неодинаковых иероглифов (10 знаков)

    @classmethod
    @timing
    def experiment_weights(cls):
        #x0 = np.random.rand(1, 4)
        x0 = np.array([1., 1., 1., 1.])
        method='nelder-mead'
        maxiter = 50
        xtol = 10
        res = minimize(Testing.optimize_weights, x0, method=method, options={'maxiter': maxiter, 'disp': True,
                                                                             'xtol': xtol})
        print res.x


class Penalty:
    @classmethod
    def count_penalty(cls, metrics):
        fontFamilies = FontFamily.get_all_families()
        penalty = 0
        alikes = []
        print "----getting signes from family----"
        for fontFamily in fontFamilies:
            signes = fontFamily.get_signes(1000)
            family_penalty = 0
            family_penalty_alike = 0
            sum_alike = 0
            sum_dif = 0
            family_penalty_different = 0
            diffs = []
            alikes = []
            for i, sign_set in enumerate(signes):
                for j, sign in enumerate(sign_set):
                    for k, sign2 in enumerate(sign_set[j + 1:]):
                        alike = metrics(sign, sign2)
                        family_penalty_alike += alike
                        sum_alike += 1
                        alikes.append(alike)

                    if i < len(signes) and i != (len(signes) - i) % len(signes):
                        diff = metrics(sign, signes[-i][j])
                        family_penalty_different += max(18 - diff, 0)
                        sum_dif += 1
                        diffs.append(diff)
            dif_to_alike = sum_dif / float(sum_alike)
            family_penalty = family_penalty_alike * dif_to_alike + family_penalty_different
            print "Family penalty alike:", family_penalty_alike, "sum_alike", sum_alike
            print "Family penalty different:", family_penalty_different, "sum_dif", sum_dif
            print "Family penalty total:", family_penalty
            penalty += family_penalty
        plt.hist(alikes)
        plt.show()
        print "Total penalty: ", penalty


if __name__ == "__main__":
    Testing.experiment_weights()
