__author__ = 'ava-katushka'
import pandas as pd
import numpy as np


class StatisticCounter:
    @staticmethod
    def remove_unnecessary(array, rows=1, columns=3):
        # delete unnecessary rows
        array = array[rows:]
        # delete unnecessary columns
        array = np.transpose(array)
        array = array[columns:]
        return np.transpose(array)

    def count_variance_on_picture(self, start):
        picture_array = self.array[start: start + self.one_picture_images]
        return picture_array.var(0)**0.5

    def count_mean_picture_variance(self):
        end = self.array.shape[0]
        pictures_variance = []
        for i in range(0, end, self.one_picture_images):
            pic_var = self.count_variance_on_picture(i)
            pictures_variance.append(pic_var)
        pictures_variance = np.asarray(pictures_variance)
        return pictures_variance.mean(0)

    def count_picture_variance(self):
        return self.array.var(0)**0.5

    def __init__(self, csv_file='test.csv', one_picture_images=10):
        self.array = np.genfromtxt(csv_file, delimiter=',')
        self.array = self.remove_unnecessary(self.array)
        self.one_picture_images = one_picture_images

    def count_all_variance(self):
        self.mean_picture_variance = st.count_mean_picture_variance()
        self.picture_variance = st.count_picture_variance()

    def print_results_column_file(self, to_file='var_results.csv'):
        with open(to_file, 'w+') as file:
            file.write('Features,Variance Averange(on pictures),Variance\n')
            i = 1
            for x, y in zip(self.mean_picture_variance, self.picture_variance):
                file.write("{0},{1},{2}\n".format(i, x, y))
                i += 1

if __name__ == '__main__':
    st = StatisticCounter('line_detection_statistics.csv')
    st.count_all_variance()
    st.print_results_column_file()
